import pika, json

def publish_order_created(order_data: dict):
    """Publish an event to RabbitMQ so Product Service can reduce stock."""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672)
    )
    channel = connection.channel()
    channel.queue_declare(queue='order_created', durable=True)  # durable = survives restart

    channel.basic_publish(
        exchange='',
        routing_key='order_created',
        body=json.dumps(order_data),
        properties=pika.BasicProperties(delivery_mode=2)  # persistent message
    )
    connection.close()
    print(f"[Order Service] Published to RabbitMQ → {order_data}")