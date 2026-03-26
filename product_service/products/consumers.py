import pika, json, os, django, sys

# Tell Django which settings to use before importing models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_service.settings')
django.setup()

from products.models import Product

def callback(ch, method, properties, body):
    """Called automatically when a message arrives in the queue."""
    data = json.loads(body)
    print(f"\n[Product Service] Order received → {data}")

    try:
        product = Product.objects.get(id=data['product_id'])
        product.stock -= data['quantity']
        product.save()
        print(f"[Product Service] Stock updated: '{product.name}' now has {product.stock} left")
        ch.basic_ack(delivery_tag=method.delivery_tag)   # tell RabbitMQ: message processed OK
    except Product.DoesNotExist:
        print(f"[Product Service] ERROR: Product {data['product_id']} not found")
        ch.basic_nack(delivery_tag=method.delivery_tag)  # tell RabbitMQ: message failed

def start_consumer():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672)
    )
    channel = connection.channel()
    channel.queue_declare(queue='order_created', durable=True)
    channel.basic_qos(prefetch_count=1)   # process one message at a time
    channel.basic_consume(queue='order_created', on_message_callback=callback)
    print("[Product Service] Listening for orders on queue 'order_created'...")
    channel.start_consuming()

if __name__ == '__main__':
    start_consumer()