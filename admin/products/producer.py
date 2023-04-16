import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq3")) # Service name 
ch = connection.channel()

def check_connection(con, ch):
    
    if not con.is_open:
        # Reconnect if the connection is closed
        print("CHANNEL IS CLOSED: RECONNECTING >>>>")
        connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq3"))
        ch = connection.channel()
    return ch

def publish(method, body):

    #  this try except block is because the it loses connection after a period of time 
    #  and it needs to establish a new connection in order to work correctly 
    #  I think this error ocurred because RabbitMQ is also a separate docker container and 
    #  the network probably is not set correctly 
    try:
        channel = check_connection(connection, ch)
        properties = pika.BasicProperties(method)
        channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)     

    except Exception  as e:
        print("EXCEPTION IN basic_publish METHOD : ", e)
        channel = check_connection(connection, ch)
        properties = pika.BasicProperties(method)
        channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)

    
    

if __name__ == "__main__":
    pass
    #connection.close()
