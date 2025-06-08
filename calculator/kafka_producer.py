from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
import json

# Primero tenemos la configuración de Kafka
KAFKA_BROKER = "localhost:9092"
TOPIC_REQUEST = "calculator_requests"

# Importante asegurarse de que el topic exista
admin_client = AdminClient({'bootstrap.servers': KAFKA_BROKER})
existing_topics = admin_client.list_topics().topics

if TOPIC_REQUEST not in existing_topics:
    print(f"Creando topic: {TOPIC_REQUEST}")
    admin_client.create_topics([NewTopic(TOPIC_REQUEST, num_partitions=1, replication_factor=1)])

# Configuramos el productor de Kafka
producer_conf = {'bootstrap.servers': KAFKA_BROKER}
producer = Producer(producer_conf)

# Y mandamos un mensaje de prueba (el mismo del enunciado)
request = {
    "id": "op1",
    "operation": "sum",
    "args": {
        "op1": 5.0,
        "op2": 10.4
    }
}

# Convertimos el mensaje a JSON y lo enviamos
producer.produce(TOPIC_REQUEST, json.dumps(request).encode('utf-8'))
producer.flush()

print(f"Solicitud enviada a Kafka: {request}")
