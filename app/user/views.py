from rest_framework import generics

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


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
