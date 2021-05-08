from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers

# https://github.com/encode/django-rest-framework/tree/master/rest_framework
# https://github.com/encode/django-rest-framework/blob/master/rest_framework/mixins.py
# https://github.com/encode/django-rest-framework/blob/master/rest_framework/serializers.py


class BaseRecipeAttrViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    """Base viewset for user owned recipe attributes"""

    # so that django knows what is the user ie. request.user
    authentication_classes = (TokenAuthentication,)
    # so that django knows whether the client is permitted
    # to view the items
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        # whatever we return here will be displayed in django api
        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        """Create a new tag"""
        # serializer save based on the model it points to
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""

    # so that django knows what to list
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in a database"""

    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # used for list()
        """Retrieve the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        # when retreive() is invoked
        if self.action == "retrieve":
            return serializers.RecipeDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        # perform_create(), is_valid are invoked in create()
        # save() must be called after is_valid() is called
        # since it needs access to validated_data
        # validated_data is only available after
        # is_valid() is invoked
        # user=self.request.user will be saved along
        # with all other validated_data
        # ie. validated_data = {**self.validated_data, **kwargs}
        # the extra arg passed in here will not pass thru
        # serializer validation !!
        # eg. user=self.request.user
        # can add any fields here regardless of
        # what is excluded from the serializer
        # ie. implementer can update, create using whatever
        # fields but not the client
        serializer.save(user=self.request.user)
