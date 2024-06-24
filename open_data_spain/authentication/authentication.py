# from django.db import models
# from django.core.cache import cache
# from django.contrib.auth import get_user_model
#
# from rest_framework import exceptions as rest_framework_exceptions
from rest_framework.authentication import BaseAuthentication
#
# from .models import APIKey
#
# from rest_framework import exceptions
#
#
# def get_api_key(request) -> str:
#     # Get the API key from the request
#     if not (token := request.META.get('HTTP_TOKEN')):
#         raise rest_framework_exceptions.AuthenticationFailed("No API key provided")
#
#     return token
#
#
# class TokenAuthentication(BaseAuthentication):
#     """
#     Simple token based authentication.
#
#     Clients should authenticate by passing the token key in the "Authorization"
#     HTTP header, prepended with the string "Token ".  For example:
#
#         Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
#     """
#
#     def authenticate(self, request):
#         api_key = get_api_key(request)
#
#         api_key_cache_key = f"api-keys:{api_key}"
#
#         # Get API from cache
#         if cache_result := cache.get(api_key_cache_key):
#             user = get_user_model().deserialize(cache_result)
#
#         else:
#
#             # Get API from database
#             try:
#                 api_key_obj = APIKey.objects.get(key=api_key)
#             except APIKey.DoesNotExist:
#                 raise exceptions.AuthenticationFailed("Invalid API key")
#
#             # Get User from api key
#             if not (user := get_user_model().objects.filter(id=api_key_obj.user_id).first()):
#                 raise exceptions.AuthenticationFailed("Invalid API key")
#
#             # Save API to cache
#             cache.set(api_key_cache_key, user.serialize(), timeout=CACHE_TIMEOUT)
#
#         return user, api_key
