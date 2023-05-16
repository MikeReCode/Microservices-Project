import json
import pika

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()


from products.models import Product

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq3")) # Service name 
channel = connection.channel()
channel.queue_declare(queue='admin')


def callback(ch, method, properties, body): # Modify queue dependence 
    print("received in adminn")
    id = json.loads(body)
    print(f'Product with ID = {id}')
    product = Product.objects.get(id=int(id))
 
    product.likes = product.likes + 1
    product.save()
    print("product likes incremented")

channel.basic_consume(queue='admin', on_message_callback=callback , auto_ack=True)

print("Started Consuming")
channel.start_consuming()
channel.close()