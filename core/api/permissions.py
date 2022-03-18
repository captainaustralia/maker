from rest_framework.permissions import BasePermission


class AuthorOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user == view.user)
