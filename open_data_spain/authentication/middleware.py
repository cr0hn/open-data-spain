from django.contrib.auth import get_user_model, authenticate

from rest_framework import exceptions as rest_framework_exceptions


def get_api_key(request) -> str:
    # Get the API key from the request
    if not (token := request.META.get('HTTP_TOKEN')):
        raise rest_framework_exceptions.AuthenticationFailed("No API key provided")

    return token


class AuthenticationAPIMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not request.path.startswith('/api/'):
            return request

        if request.user.is_authenticated:
            return request

        #
        # Use custom authentication backend
        #
        auth_user = authenticate(request)

        if not auth_user:
            raise rest_framework_exceptions.AuthenticationFailed("Invalid API key")

        request.user = auth_user

        return self.get_response(request)
