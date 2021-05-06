from django.contrib.auth import get_user_model, authenticate

# used when you want to output any messages
# pass through translation system in case in the future
# you want to support other languages
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


# https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        # point to this model
        model = get_user_model()
        # fields that you want to include in the serializer
        # retrieve these fields
        # make these fields accessible in api, either to read or write
        fields = ("email", "password", "name")
        # config extra settings
        # ensure password is write_only
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    # the viewset will invoke this to create
    # if serializer_class is specified in viewset
    def create(self, validated_data):
        # override create function
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get("email")
        password = attrs.get("password")

        # request that you want to authenticate
        user = authenticate(
            # access the context of the request like this
            # django viewset will store the request
            # under context when a request is made
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            # passing a 400 reponse
            raise serializers.ValidationError(msg, code="authentication")

        # set user in the attr
        attrs["user"] = user
        # must return attr for validate() method
        return attrs
