import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq3")) # Service name 
channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)

    channel.basic_publish(exchange='', routing_key='main',
                      body=json.dumps(body), properties=properties)
    

if __name__ == "__main__":
    pass
    #connection.close()
