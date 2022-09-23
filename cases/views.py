from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from django_filters import rest_framework
import requests
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from random import randint
from fund import settings
from . import payment
from .models import Case, Images, Categories
from .serializers import CaseSerializer, ImageSerializer, CategoriesSerializer


class PaymentView(ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        order_id = randint(0, 20000)
        salt = get_random_string(10)
        # request.data['order_id'] = order_id
        # request.data['salt'] = salt
        payment_sig_init = {
            'pg_order_id': str(order_id),
            'pg_merchant_id': str(settings.MERCHANT_ID),
            'pg_amount': str(request.data.get('amount')),
            'pg_description': str(request.data.get('description')),
            'pg_salt': str(salt),
            'pg_currency': 'KGS',
            'pg_sig': payment.create_sig(request, order_id, salt),
        }
        req = requests.post('https://api.paybox.money/init_payment.php', data=payment_sig_init)
        return Response(req)


class CaseModelViewSet(ModelViewSet):
    queryset = Case.objects.exclude(status=4)
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
