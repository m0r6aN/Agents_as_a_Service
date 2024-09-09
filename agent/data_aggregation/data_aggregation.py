import pika
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO)

class DataAggregationWorker:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_name = 'data_aggregation_queue'

    def connect(self):
        while not self.connection or self.connection.is_closed:
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=self.queue_name, durable=True)
                logging.info("Connected to RabbitMQ and channel created.")
            except pika.exceptions.AMQPConnectionError as e:
                logging.error(f"Connection failed, retrying in 5 seconds: {e}")
                time.sleep(5)

    def run(self):
        self.connect()

        # Define your message handling here
        def callback(ch, method, properties, body):
            logging.info(f"Received message: {body}")
            # Process the message here
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback)

        logging.info("Waiting for messages...")
        self.channel.start_consuming()

if __name__ == "__main__":
    worker = DataAggregationWorker()
    worker.run()
