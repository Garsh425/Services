import time
import pika
import psycopg2
import json
import logging

RABBITMQ_HOST = 'docker-rabbitmq-1'
QUEUE_NAME = 'task_queue'

logging.basicConfig(level=logging.INFO)

def db_connect():
    return psycopg2.connect(
        dbname="postgres",
        user="user",
        password="password",
        host="docker-db-1"
    )

def callback(ch, method, properties, body):
    data = json.loads(body)
    logging.info(f"Получено сообщение: {data}")

    conn = None
    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tickets (surname, name, middlename, phone, message)
            VALUES (%s, %s, %s, %s, %s)
        """, (data['surname'], data['name'], data['middlename'], data['phone'], data['message']))
        conn.commit()
        logging.info("Запись успешно выполнена.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Ошибка при записи в базу данных: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)
    finally:
        if conn:
            conn.close()

def main():
    credentials = pika.PlainCredentials('user', 'password')
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
            channel = connection.channel()
            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)
            channel.start_consuming()
            break
        except:
            time.sleep(10)

if __name__ == "__main__":
    main()