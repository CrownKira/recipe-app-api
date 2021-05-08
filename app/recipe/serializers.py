from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe

# serialize:
# - translates model into querydict (json representation)
# (ie. validated_data, exposed_data fields),
# - merges querydict back into model (ie. create, update)
#
# can take in:
# outer:
# instance, queryset (of instances), request.data (querydict ie. client input)
# nested:
#  many, read_only

# https://github.com/encode/django-rest-framework/blob/
# a0083f7f9867113a37a5096a06ee69344781075a/rest_framework/serializers.py#L968
# client can only modify db using whatever fields that are exposed
# (specified in meta::fields)
# the rest of the fields have to be handled by the
# implementer or Django eg. user field, created_at, etc


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        # only these fields are exposed to the client
        # client can only read and/or write to
        # these fields
        fields = ("id", "name")
        # if set to readonly => cannot write
        # ie. will be ignored when pass in the data
        # ie. will not be in the final validated_data field
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
    # queryset - The queryset used for model instance
    # lookups when validating the field input.
    # The queryset argument is only ever required for
    # writable relationship field, in which case it is used
    # for performing the model instance lookup, that maps from
    # the primitive user input, into a model instance.
    # eg. if user input is [1,2,3] and
    # Ingredient.objects.all() is [1,2,4,5,6]
    # then it will be invalid since there is no 3
    # will update by .add(queryset.filter(...))
    # ie. if user input not in the queryset
    # then it is invalid
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ingredient.objects.all()
    )
    # By default this field is read-write, although
    # you can change this behavior using the read_only flag.
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        # all the fields that will be exposed
        # to the client
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
    # readonly=True since nested serializer doesn't support update
    # workaround:
    # https://django.cowhite.com/blog/create-and-update-
    # django-rest-framework-nested-serializers/
    # By default nested serializers are read-only.
    # If you want to support write-operations to a nested serializer
    # field you'll need to create create() and/or update() methods
    # in order to explicitly specify how the child
    # relationships should be saved:
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
