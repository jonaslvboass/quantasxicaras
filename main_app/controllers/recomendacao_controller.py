import pika
import json
import uuid

def obter_recomendacoes(usuario_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    result = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue
    corr_id = str(uuid.uuid4())
    response = None
    def on_response(ch, method, props, body):
        nonlocal response
        if props.correlation_id == corr_id:
            response = json.loads(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=False)
    channel.basic_publish(
        exchange='',
        routing_key='recommendation_requests',
        properties=pika.BasicProperties(
            reply_to=callback_queue,
            correlation_id=corr_id,
        ),
        body=json.dumps({'user_id': usuario_id})
    )
    while response is None:
        connection.process_data_events(time_limit=1)
    channel.close()
    connection.close()
    return response['recommendation'] 