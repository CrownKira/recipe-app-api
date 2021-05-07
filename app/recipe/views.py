from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag

from recipe import serializers

# https://github.com/encode/django-rest-framework/tree/master/rest_framework


class TagViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    """Manage tags in the database"""

    # so that django knows what is the user ie. request.user
    authentication_classes = (TokenAuthentication,)
    # so that django knows whether the client is permitted
    # to view the items
    permission_classes = (IsAuthenticated,)
    # so that django knows what to list
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        # whatever we return here will be displayed in django api
        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)
