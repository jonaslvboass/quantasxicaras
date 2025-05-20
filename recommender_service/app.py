import pika
import json
from recommender import recommend_for_user

RABBITMQ_HOST = 'localhost'
REQUEST_QUEUE = 'recommendation_requests'
RESPONSE_QUEUE = 'recommendation_responses'

def on_request(ch, method, properties, body):
    data = json.loads(body)
    user_id = data.get('user_id')
    recommendation = recommend_for_user(user_id)
    response = json.dumps({'user_id': user_id, 'recommendation': recommendation})
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=response
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=REQUEST_QUEUE)
    channel.queue_declare(queue=RESPONSE_QUEUE)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=REQUEST_QUEUE, on_message_callback=on_request)
    print(' [*] Aguardando requisições de recomendação. Para sair pressione CTRL+C')
    channel.start_consuming() 