from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('case', viewset=views.CaseModelViewSet)
router.register('images', viewset=views.ImageViewSet)
router.register('category', viewset=views.CategoriesViewSet)


urlpatterns = [
    path('', include(router.urls))
]
