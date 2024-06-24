from django.conf import settings

from ..sdk.cache import build_user_cache_key_prefix


class TrackingUserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Get user
        if not request.user.is_authenticated:
            return response

        # Get url, user and timestamp
        path = request.path

        if not path.startswith('/api'):
            return response

        # Get timestamp
        #
        # Add tracking
        # timestamp = datetime.datetime.now().isoformat()

        #
        # Store counter Redis
        #

        # Get redis connection from cache
        redis_client = settings.REDIS_CONNECTION

        # Build cache key
        if cache_key := build_user_cache_key_prefix(request):

            # Increment counter
            redis_client.incr(cache_key, 1)

        return response
