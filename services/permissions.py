from rest_framework.permissions import BasePermission


class ReviewsPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class BasketPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

