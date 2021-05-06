from rest_framework import generics, authentication, permissions

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer

# django-rest-framework.org/api-guide/generic-views/


# Create your views here.
# createapiview:
# premade for us to allow us to easily create an obj
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    # only need to specify the serializer class
    # will invoke the create() method of this
    # serializer class
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = AuthTokenSerializer
    # set a render
    # so that we can view this endpoint using browser
    # with the browsable api
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    # RetrieveUpdateAPIView:
    # Used for read or update endpoints to represent a single model instance.
    # Provides get, put and patch method handlers.
    # this class points to a specific object
    """Manage the authenticated user"""

    serializer_class = UserSerializer
    # authentication: will attach user to the request
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # override get_object
    # get the model for the logged in user
    # Returns an object instance that should be used for detail views.
    # Defaults to using the lookup_field parameter to filter the base queryset.
    # May be overridden to provide more complex behavior,
    # such as object lookups based on more than one URL kwarg.
    def get_object(self):
        """Retrieve and return authenticated user"""
        # don't care about url parameter
        return self.request.user
