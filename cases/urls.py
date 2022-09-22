from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('cases', views.CaseModelViewSet)
router.register('images', views.ImageViewSet)
router.register('categories', views.CategoriesViewSet)


urlpatterns = []
urlpatterns += router.urls
