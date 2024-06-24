import redis
from django.conf import settings
from django.http import JsonResponse

from .sdk import get_plan_features, KEY_MAX_CONCURRENT_REQUESTS, KEY_MAX_REQUESTS_PER_MONTH


class APIBillingUserPlanMiddleware:
    """
    Este middleware comprueba los límites de la cuenta del usuario:
    - Número total de peticiones a la API
    - Concurrencia de peticiones a la API
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Solo aplicamos el middleware a las peticiones de la API
        if not request.path.startswith('/api'):
            return request

        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not authenticated'}, status=401)

        # Obtenemos los límites del plan
        try:
            feature = get_plan_features(request.user.plan_name)
        except Exception:
            return JsonResponse({'error': 'Invalid plan'}, status=400)

        cfg_max_requests_per_month = feature.get('max_requests_per_month', 0)
        cfg_max_concurrent_requests = feature.get('max_concurrent_requests', 0)

        # DB Keys
        key_max_concurrent_requests = KEY_MAX_CONCURRENT_REQUESTS.format(request.user.pk)
        key_max_requests_per_month = KEY_MAX_REQUESTS_PER_MONTH.format(request.user.pk)
        lock_key_concurrent_requests = f"lock-max-concurrent-requests:{request.user.pk}"

        # Comprobamos si no se ha superado el límite de peticiones por mes
        redis_client: redis.Redis = settings.REDIS_CONNECTION

        try:
            current_requests_per_month = int(redis_client.get(key_max_requests_per_month) or 0)
        except TypeError:
            current_requests_per_month = 0

        if current_requests_per_month >= cfg_max_requests_per_month:
            return JsonResponse({'error': 'Max requests per month reached'}, status=429)
        else:
            redis_client.incr(key_max_requests_per_month)

        # Comprobamos si se ha superado el límite de peticiones concurrentes
        try:
            current_concurrent_requests = int(redis_client.get(key_max_concurrent_requests) or 0)
        except TypeError:
            current_concurrent_requests = 0

        if current_concurrent_requests >= cfg_max_concurrent_requests:
            return JsonResponse({'error': 'Max concurrent requests reached'}, status=429)

        # Incrementamos el contador de peticiones concurrentes
        with redis_client.lock(lock_key_concurrent_requests, timeout=10):
            try:
                current_concurrent_requests = int(redis_client.get(key_max_concurrent_requests) or 0)
            except TypeError:
                current_concurrent_requests = 0

            # Expire in 5 seconds
            redis_client.set(key_max_concurrent_requests, current_concurrent_requests + 1, ex=5)

        # Ejecutamos la petición
        try:
            return self.get_response(request)

        finally:
            # Decrementamos el contador de peticiones concurrentes
            with redis_client.lock(lock_key_concurrent_requests, timeout=10):
                try:
                    current_concurrent_requests = int(redis_client.get(key_max_concurrent_requests))
                except TypeError:
                    current_concurrent_requests = 0

                redis_client.set(key_max_concurrent_requests, abs(current_concurrent_requests - 1), ex=10)
