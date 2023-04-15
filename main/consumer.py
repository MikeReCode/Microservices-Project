import pika
import json
from main_flask import Product
from main_flask import db, app


#app.app_context()
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq3")) # Service name 
channel = connection.channel()
channel.queue_declare(queue='main')



def callback(ch, method, properties, body):
    print("reciver in main")
    data = json.loads(body)
    print(data)
    print(properties)

    if properties.content_type == 'product_created':
        with app.app_context():
            product = Product(id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
            db.session.commit()
        print('Product Created')

    elif properties.content_type == 'product_updated':
        with app.app_context():
            product = db.session.get(Product, data['id'])
            product.title = data['title']
            product.image = data['image']
            db.session.commit()
        print('Product Updated')

    elif properties.content_type == 'product_deleted':
        with app.app_context():
            product = db.session.get(Product, data['id'])
            db.session.delete(product)
            db.session.commit()
        print('Product Deleted')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print("Started Consumming")
channel.start_consuming()
channel.close()