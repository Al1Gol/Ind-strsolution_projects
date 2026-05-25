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
            and (request.user.is_manager or request.user.is_staff)
            and request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]
        ):
            return True
        else:
            return False
        


# Рарешения новостей
class NewsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Checks if user has the specific permission string
        if request.method == "GET":
            return  request.user.has_perm('newsapp.view_news')
        elif request.method == "POST":
            return  request.user.has_perm('newsapp.add_news')
        elif request.method in ["PUT", "PATCH"]:
            return  request.user.has_perm('newsapp.change_news')
        elif request.method in ["DELETE"]:
            return  request.user.has_perm('newsapp.delete_news')
        
# Рарешения для медиа в новостях
class NewsMediaPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Checks if user has the specific permission string
        if request.method == "GET":
            return  request.user.has_perm('newsapp.view_media')
        elif request.method == "POST":
            return  request.user.has_perm('newsapp.add_media')
        elif request.method in ["PUT", "PATCH"]:
            return  request.user.has_perm('newsapp.change_media')
        elif request.method in ["DELETE"]:
            return  request.user.has_perm('newsapp.delete_media')


# Рарешения для договоров
class ContractsPermission(permissions.BasePermission):  
    def has_permission(self, request, view):
        # Checks if user has the specific permission string
        if request.method == "GET":
            return  request.user.has_perm('projectsapp.view_contracts')
        elif request.method == "POST":
            return  request.user.has_perm('projectsapp.add_contracts')
        elif request.method in ["PUT", "PATCH"]:
            return  request.user.has_perm('projectsapp.change_contracts')
        elif request.method in ["DELETE"]:
            return  request.user.has_perm('projectsapp.delete_contracts')
        

# Рарешения для проектов
class ProjectsPermission(permissions.BasePermission):  
    def has_permission(self, request, view):
        # Checks if user has the specific permission string
        if request.method == "GET":
            return  request.user.has_perm('projectsapp.view_projects')
        elif request.method == "POST":
            return  request.user.has_perm('projectsapp.add_projects')
        elif request.method in ["PUT", "PATCH"]:
            return  request.user.has_perm('projectsapp.change_projects')
        elif request.method in ["DELETE"]:
            return  request.user.has_perm('projectsapp.delete_projects')
        

# Рарешения для согласований
class AdjustPermission(permissions.BasePermission):  
    def has_permission(self, request, view):
        # Checks if user has the specific permission string
        if request.method == "GET":
            return  request.user.has_perm('projectsapp.view_adjust')
        elif request.method == "POST":
            return  request.user.has_perm('projectsapp.add_adjust')
        elif request.method in ["PUT", "PATCH"]:
            return  request.user.has_perm('projectsapp.change_adjust')
        elif request.method in ["DELETE"]:
            return  request.user.has_perm('projectsapp.delete_adjust')


# Рарешения для документов
class DocumentsPermission(permissions.BasePermission):  
    def has_permission(self, request, view):
        # Checks if user has the specific permission string
        if request.method == "GET":
            return  request.user.has_perm('projectsapp.view_documents')
        elif request.method == "POST":
            return  request.user.has_perm('projectsapp.add_documents')
        elif request.method in ["PUT", "PATCH"]:
            return  request.user.has_perm('projectsapp.change_documents')
        elif request.method in ["DELETE"]:
            return  request.user.has_perm('projectsapp.delete_documents')