from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from rest_framework import exceptions as rest_framework_exceptions

from .models import APIKey, KeyStatus
from .constants import CACHE_TIMEOUT


class APIAuthBackend(BaseBackend):

    def authenticate(self, request, **kwargs):

        #
        # Perform authentication
        #
        api_key = request.META.get('HTTP_TOKEN')

        if not api_key:
            if not (api_key_header := request.META.get('HTTP_AUTHORIZATION')):
                raise rest_framework_exceptions.AuthenticationFailed("No API key provided")

            try:
                api_key = api_key_header.split(' ')[1]
            except IndexError:
                raise rest_framework_exceptions.AuthenticationFailed("No API key provided")

        api_key_cache_key = f"api-keys:{api_key}"

        # Get API from cache
        if cache_result := cache.get(api_key_cache_key):
            user = get_user_model().deserialize(cache_result)

        else:

            # Get API from database
            try:
                api_key_obj = APIKey.objects.get(key=api_key)
            except APIKey.DoesNotExist:
                raise rest_framework_exceptions.AuthenticationFailed("Invalid API key")

            if api_key_obj.status != KeyStatus.ACTIVE:
                raise rest_framework_exceptions.AuthenticationFailed("API key is not active")

            # Get User from api key
            if not (user := get_user_model().objects.filter(id=api_key_obj.user_id)):
                raise rest_framework_exceptions.AuthenticationFailed("Invalid API key")

            # Save API to cache
            cache.set(api_key_cache_key, user.serialize(), timeout=CACHE_TIMEOUT)

        return user
