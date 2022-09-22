from rest_framework.viewsets import ModelViewSet

from .models import Case, Images
from .serializers import CaseSerializer, ImageSerializer


class CaseModelViewSet(ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer


