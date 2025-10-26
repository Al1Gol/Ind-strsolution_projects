from rest_framework import permissions


class ModerateAndAdminCreateUpdateDeleteOrAuthReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.is_authenticated
            and request.user
            and (request.user.is_staff or request.user.is_manager)
        ):
            return True

        elif (
            request.user.is_authenticated
            and request.user
            and request.method in ["POST", "PUT", "PATCH", "CREATE", "DELETE"]
            and request.user.is_manager
        ):
            return True
        return bool(
            request.user.is_authenticated and request.method in permissions.SAFE_METHODS
        )
    
class ModerateAndAdminUpdate(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.is_authenticated
            and request.user
            and (request.user.is_superuser or request.user.is_manager)
        ):
            return True
        else:
            return False
    


class AdminUserOrAuthReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.is_authenticated
            and request.user
            and (request.user.is_staff or request.user.is_manager)
        ):
            return True
        return bool(
            request.user.is_authenticated and request.method in permissions.SAFE_METHODS
        )

class PublicReadAndOnlyOwnerOrAdminUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Если запись публична - чтение доступно всем авторизованным пользователям
        if (
            request.user.is_authenticated
            and request.user.is_client
            and obj.public
            and request.method in ["GET"]
        ):
            return True
        # CREATE, UPDATE, DELETE доступны только владельцу, либо админу. А так же чтение, не зависимо от доступности записи.
        elif (
            request.user.is_authenticated
            and (request.user == obj.is_manager or request.user.is_staff)
            and request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]
        ):
            return True
        else:
            return False