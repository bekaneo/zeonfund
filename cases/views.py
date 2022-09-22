from rest_framework.viewsets import ModelViewSet

from .models import Case, Images, Categories
from .serializers import CaseSerializer, ImageSerializer, CategoriesSerializer


class CaseModelViewSet(ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer


class ImageViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer


class CategoriesViewSet(ModelViewSet):
    queryset = Categories
    serializer_class = CategoriesSerializer
