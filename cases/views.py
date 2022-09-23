from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from django_filters import rest_framework
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from random import randint

from .models import Case, Images, Categories
from .serializers import CaseSerializer, ImageSerializer, CategoriesSerializer
# curl --location --request POST 'https://api.paybox.money/init_payment.php' \
# --form 'pg_order_id=23' \
# --form 'pg_merchant_id={{paybox_merchant_id}}' \
# --form 'pg_amount=25' \
# --form 'pg_description=test' \
# --form 'pg_salt=molbulak' \
# --form 'pg_sig={{paybox_signature}}'
# # Пример подписи:
# 'init_payment.php;25;test;{{paybox_merchant_id}};23;molbulak;{{secret_key}}'
# 'pg_order_id' => '23',
#     'pg_merchant_id'=> $pg_merchant_id,
#     'pg_amount' => '25',
#     'pg_description' => 'test',
#     'pg_salt' => 'molbulak',
#     'pg_currency' => 'KZT',
# class PaymentView(ListCreateAPIView):
#     def create(self, request, *args, **kwargs):
#         pg_order_id = randint(10, 1000000),
#         pg_merchant_id = 535456,
#         pg_amount = request.data.get('amount'),
#         pg_description = request.data.get('description'),
#         pg_salt = get_random_string(20),
#         payment_sig_init = {
#             'pg_order_id': randint(10, 1000000),
#             'pg_merchant_id': 535456,
#             'pg_amount': request.data.get('amount'),
#             'pg_description': request.data.get('description'),
#             'pg_salt': get_random_string(20),
#             'pg_sig': ...
#         }

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
