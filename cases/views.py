from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Case, Images, Categories
from .serializers import CaseSerializer, ImageSerializer, CategoriesSerializer


class CaseModelViewSet(ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    @swagger_auto_schema(request_body=CaseSerializer)
    def create(self, request, *args, **kwargs):
        case_serializer = CaseSerializer(data=request.POST, context={'request': request})
        if case_serializer.is_valid(raise_exception=True):
            case = case_serializer.save()
            case_data = case_serializer.data

            images = []
            for image in request.FILES.getlist('image'):
                data = {'image': image}
                image_serializer = ImageSerializer(data=data, context={'case': case.id, 'request': request})
                if image_serializer.is_valid(raise_exception=True):
                    image_serializer.save()
                    images.append(image_serializer.data)

            data = {'product_data': case_data, 'image': images}
            return Response(data, status=status.HTTP_201_CREATED)


class ImageViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer


class CategoriesViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
