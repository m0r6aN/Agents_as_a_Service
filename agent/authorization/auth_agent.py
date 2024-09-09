import pika
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# RabbitMQ connection parameters
rabbitmq_host = 'localhost'
queue_name = 'auth_queue'

def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    return channel

def process_task(ch, method, properties, body):
    logging.info(f"Received task: {body}")

    # Simulate task processing (authentication logic would go here)
    logging.info("Processing authentication task...")

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_auth_agent():
    channel = connect_to_rabbitmq()
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=process_task)

    logging.info("Authentication Agent is waiting for tasks...")
    channel.start_consuming()

if __name__ == "__main__":
    start_auth_agent()
