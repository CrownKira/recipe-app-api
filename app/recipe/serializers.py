from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


# filter, update, create (FUC)
class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ("id", "name")
        # if set to readonly => cannot modify
        read_only_fields = ("id",)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ("id", "name")
        read_only_fields = ("id",)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""

    # list items with the primary key id
    # https://www.django-rest-framework.org/
    # api-guide/relations/#primarykeyrelatedfield
    # {
    # 'album_name': 'Undun',
    # 'artist': 'The Roots',
    # 'tracks': [
    #     89,
    #     90,
    #     91,
    #     ...
    # ]
    # }
    # many=True since it is one to many relationship
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "title",
            "ingredients",
            "tags",
            "time_minutes",
            "price",
            "link",
        )
        read_only_fields = ("id",)


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe detail"""

    # more detailed version compared to RecipeSerializer,
    # with depth incremented by 1 when retrieve an item
    # viewset will get_object() based on the url param
    # ie. the pk/id of the object

    # nest serializer inside each other
    # if a nested representation should be a list of items,
    # you should pass the many=True flag to the nested serializer.
    # ie. there will be a nested dict within the dict
    # eg. {tags:{...}, ingredients:{...}, etc}
    # field = CharField / PrimaryKeyRelatedField, TagSerializer
    # readonly: client cannot update the field when they put, patch, etc
    # when update instance, have to go thru serializer
    # readonly=True since nested serializer doesnt support update
    # workaround:
    # https://django.cowhite.com/blog/create-and-update-
    # django-rest-framework-nested-serializers/
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
