from django.utils.text import slugify

from .services import service_resolver


def build_user_cache_key_prefix(request, service_name: str = None) -> str | None:
    if not request:
        return None

    if hasattr(request, "user") and not request.user.is_authenticated:
        return None

    user_slug = slugify(request.user.email.replace("@", "-at-"))

    if not service_name:
        try:
            service_name = service_resolver(request.path)
        except ValueError:
            return None

    return f"counters:{user_slug}:{service_name}"


__all__ = ("build_user_cache_key_prefix",)
