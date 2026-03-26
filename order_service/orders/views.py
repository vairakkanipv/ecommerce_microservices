import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from .publisher import publish_order_created

PRODUCT_SERVICE_URL = "http://localhost:8001/api"

class OrderViewSet(viewsets.ModelViewSet):
    queryset         = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request):
        product_id = request.data.get('product_id')
        quantity   = int(request.data.get('quantity', 1))

        # ── Step 1: Ask Product Service if stock is available (REST call) ──
        try:
            resp         = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}/check_stock/")
            product_data = resp.json()
        except Exception:
            return Response({"error": "Product Service is down"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # ── Step 2: If not enough stock, fail the order ──
        if not product_data.get('available') or product_data['stock'] < quantity:
            order = Order.objects.create(product_id=product_id, quantity=quantity, status='failed')
            return Response({"error": "Not enough stock", "order_id": order.id}, status=status.HTTP_400_BAD_REQUEST)

        # ── Step 3: Stock is fine — confirm the order ──
        order = Order.objects.create(product_id=product_id, quantity=quantity, status='confirmed')

        # ── Step 4: Tell Product Service to reduce stock via RabbitMQ (async) ──
        publish_order_created({
            "order_id"   : order.id,
            "product_id" : product_id,
            "quantity"   : quantity
        })

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)