from rest_framework import viewsets, permissions
from .models import Promotion
from .serializers import PromotionSerializer

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.filter(is_active=True)
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]