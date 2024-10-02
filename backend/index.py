import time
import tornado.ioloop
import tornado.web
import pika
import json

RABBITMQ_HOST = 'docker-rabbitmq-1'
QUEUE_NAME = 'task_queue'

class MainHandler(tornado.web.RequestHandler):
    def options(self):
        self.set_status(204)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.finish()

    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")

        data = json.loads(self.request.body)
        self.send_to_rabbitmq(data)
        self.set_status(200)
        self.write({"status": "success", "message": "Data sent to RabbitMQ"})

    def send_to_rabbitmq(self, message):
        credentials = pika.PlainCredentials('user', 'password')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        channel = connection.channel()
        channel.basic_publish(
                exchange='',
                routing_key=QUEUE_NAME,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                )
            )
        connection.close()

def make_app():
    return tornado.web.Application([
        (r"/POST", MainHandler),
    ])

def make_queue():
    credentials = pika.PlainCredentials('user', 'password')
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            connection.close()
            break
        except:
            time.sleep(10)

if __name__ == "__main__":
    make_queue()
    app = make_app()
    app.listen(9090)
    print("Server is running on http://localhost:9090/POST")
    tornado.ioloop.IOLoop.current().start()