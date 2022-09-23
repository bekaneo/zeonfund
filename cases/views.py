from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Case, Images, Categories
from .serializers import CaseSerializer, ImageSerializer, CategoriesSerializer


class CaseModelViewSet(ModelViewSet):
    queryset = Case.objects.filter(status=1)
    serializer_class = CaseSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title']
    filterset_fields = ['category']

    @swagger_auto_schema(request_body=CaseSerializer)
    def create(self, request, *args, **kwargs):
        case_serializer = CaseSerializer(data=request.data, context={'request': request})
        if case_serializer.is_valid(raise_exception=True):
            case = case_serializer.save(user=request.user)
            case_data = case_serializer.data
            images = []

            for image in request.FILES.getlist('images'):
                data = {'image': image, 'case': case.id}
                image_serializer = ImageSerializer(data=data, context={'case': case, 'request': request})
                if image_serializer.is_valid(raise_exception=True):
                    image_serializer.save()
                    images.append(image_serializer.data)

            data = {'product_data': case_data, 'images': images}
            return Response(data, status=status.HTTP_201_CREATED)

        return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)


class ImageViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer


class CategoriesViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [filters.SearchFilter]
