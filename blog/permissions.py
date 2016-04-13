from rest_framework import permissions
from authentication.models import Account

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    This is a permission for author or people who can just read the object.
    Based on the class the system can distinct between author and just a user
    """

    def has_object_permission(self, request, view, obj):
        # reading for the post is always permitted
        # GET, HEAD, OPTION(SAFE_METHODS) are always permitted
        if request.method in permissions.SAFE_METHODS:
            return True

        #adminUser = User.objects.filter(username='jujbob')
        adminUser = Account.objects.filter(is_staff=True)
        if request.user in adminUser:
            return True

        # For updating and writing for author // return True or False
        return obj.author == request.user
