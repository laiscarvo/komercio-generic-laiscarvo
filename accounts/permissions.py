from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Account


class IsOwnerSeller(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Account) -> bool:

        return request.user == obj


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:

        return request.user.is_superuser
