from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import action
from rest_framework import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    #order service will call this url to check available stock
    @action(detail=True, methods=['get'])
    def check_stock(self, request,pk=None):
        product = self.get_object()
        return Response({
            'product_id': product.id,
            'name' : product.name,
            'stock' : product.stock,
            'available' : product.stock > 0
        })
    
