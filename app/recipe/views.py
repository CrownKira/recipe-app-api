from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
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

    # private function, by convention prepend _
    # qs: query string
    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        # list of strings split up by the comma
        # our_string = '1,2,3'
        # our_string_list = ['1', '2', '3']
        # for each item in the returned list, do the left
        # similar to map
        return [int(str_id) for str_id in qs.split(",")]

    # all functions in python are public
    def get_queryset(self):
        # used for list()
        """Retrieve the recipes for the authenticated user"""
        # http://localhost:8000/api/recipe/recipes/?ingredients=1
        tags = self.request.query_params.get("tags")
        ingredients = self.request.query_params.get("ingredients")
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            # __ (double underscore): filter on foreign key objects
            # tag > id
            # __in return all the tags where the id is in the tag_ids list
            queryset = queryset.filter(tags__id__in=tag_ids)

        if ingredients:
            # Field lookups
            # https://docs.djangoproject.com/en/3.2/ref/models
            # /querysets/#std:fieldlookup-exact
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        # when retreive() is invoked
        if self.action == "retrieve":
            return serializers.RecipeDetailSerializer
        elif self.action == "upload_image":
            return serializers.RecipeImageSerializer

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

    # when this url is accessed, this method will be invoked
    # this method is used to save the image passed in
    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe"""
        # get object based on the model and pk
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
