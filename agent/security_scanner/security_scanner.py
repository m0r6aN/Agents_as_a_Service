import pika

def security_scan():
    # Placeholder function for a security scan
    print("Performing security scan...")

def callback(ch, method, properties, body):
    try:
        print(f"Received {body}")
        security_scan()
    except Exception as e:
        print(f"Error: {e}")

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='security_scan', durable=True)

    channel.basic_consume(queue='security_scan', on_message_callback=callback, auto_ack=True)

    print('Waiting for tasks. To exit press CTRL+C')

    try:
        while True:
            channel.start_consuming()
    except KeyboardInterrupt:
        print("Received KeyboardInterrupt, shutting down...")
        # Stop consuming and close the channel and connection
        channel.stop_consuming()
        channel.close()
        connection.close()
    except Exception as e:
        print(f"Error: {e}")
        channel.stop_consuming()
        channel.close()
        connection.close()
except Exception as e:
    print(f"Error: {e}")