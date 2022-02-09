from rest_framework.permissions import BasePermission


class DoctorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('doctor.booking')
