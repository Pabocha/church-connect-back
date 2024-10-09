from rest_framework.permissions import BasePermission

class IsStaff(BasePermission):
    """
    Permission personnalisée pour vérifier si l'utilisateur est membre du personnel (is_staff).
    """

    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est authentifié et est membre du personnel
        return request.user and request.user.is_authenticated and request.user.is_staff
