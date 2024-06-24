from django.conf import settings
from django.contrib.auth import login
from django.core.cache import cache
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from .helpers import get_api_key
from .models import UserRoles, ODSUser, APIKey


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        api_key = get_api_key(request)

        return api_key == settings.MASTER_API_TOKEN


class IsMasterUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == UserRoles.ADMIN


class HasValidPlan(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only allow access if the current user is the 'manager' of the organization
        return request.user.role == UserRoles.ADMIN
