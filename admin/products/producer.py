import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq3")) # Service name 
channel = connection.channel()

def publish():

    channel.basic_publish(exchange='', routing_key='admin',
                      body='Hello ')
    

if __name__ == "__main__":
    publish()
    #connection.close()
