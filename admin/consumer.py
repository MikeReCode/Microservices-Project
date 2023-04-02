import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq3")) # Service name 
channel = connection.channel()
channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print("reciver in admin")
    print(body)

channel.basic_consume(queue='admin', on_message_callback=callback , auto_ack=True)

print("Started Consumming")
channel.start_consuming()
channel.close()