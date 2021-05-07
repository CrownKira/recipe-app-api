from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

# defaultrouter: auto gen url for viewset
# eg. /api/recipe/tags, api/recipe/tags/1, etc

router = DefaultRouter()
router.register("tags", views.TagViewSet)
router.register("ingredients", views.IngredientViewSet)

app_name = "recipe"

urlpatterns = [path("", include(router.urls))]
