import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq3")) # Service name 
channel = connection.channel()
channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print("reciver in main")
    print(body)

channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print("Started Consumming")
channel.start_consuming()
channel.close()