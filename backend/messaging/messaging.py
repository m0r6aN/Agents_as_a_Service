# messaging/messaging.py

import pika
import logging

class MessagingClient:
    def __init__(self, host='localhost'):
        self.connection_params = pika.ConnectionParameters(host)
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()
        self.logger = logging.getLogger('MessagingClient')

    def declare_exchange(self, exchange_name, exchange_type='direct'):
        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
        self.logger.debug(f"Declared exchange '{exchange_name}' of type '{exchange_type}'.")

    def bind_queue(self, queue_name, exchange_name, routing_key):
        self.channel.queue_declare(queue=queue_name)
        self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
        self.logger.debug(f"Bound queue '{queue_name}' to exchange '{exchange_name}' with routing key '{routing_key}'.")

    def send_message(self, exchange_name, routing_key, message, properties=None):
        # Set message properties if provided
        pika_properties = pika.BasicProperties()
        if properties:
            for key, value in properties.items():
                setattr(pika_properties, key, value)

        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=message,
            properties=pika_properties
        )
        self.logger.debug(f"Message sent to exchange '{exchange_name}' with routing key '{routing_key}': {message}")

    def receive_messages(self, queue_name, callback):
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.logger.debug(f"Started consuming from queue '{queue_name}'.")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        except Exception as e:
            self.logger.error(f"An error occurred while consuming messages: {e}")
            self.channel.stop_consuming()
        finally:
            self.connection.close()
