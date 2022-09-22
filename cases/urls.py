from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('cases', viewset=views.CaseModelViewSet)
router.register('images', viewset=views.ImageViewSet)
router.register('categories', viewset=views.CategoriesViewSet)


urlpatterns = []
urlpatterns += router.urls
