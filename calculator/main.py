import subprocess
import threading
import logging
import time
import json
from confluent_kafka import Consumer

# Primero la configuración de Kafka
KAFKA_BROKER = "localhost:9092"
TOPIC_RESPONSE = "calculator_responses"

# Inciamos las herramientas
def iniciar_kafka_consumer():
    logging.info("Iniciando consumidor de Kafka...")
    subprocess.run(["python", "calculator/kafka_consumer.py"])

def ejecutar_kafka_producer():
    logging.info("Enviando solicitud desde el productor Kafka...")
    subprocess.run(["python", "calculator/kafka_producer.py"])

def escuchar_respuesta_kafka():
    logging.info("Escuchando respuestas de Kafka...")
    consumer_conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'responder_group',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe([TOPIC_RESPONSE])
    timeout = time.time() + 10  # Espera máxima de 10 segundos

    while time.time() < timeout:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            logging.error(f"Error en Kafka: {msg.error()}")
            continue
        try:
            data = json.loads(msg.value().decode("utf-8"))
            logging.info(f"Respuesta recibida de Kafka: {data}")
            break
        except Exception as e:
            logging.error(f"Error al procesar la respuesta: {e}")
    consumer.close()

# Flujo principal para el lanzamiento de los procesos
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # 1. Iniciar el consumidor en un hilo
    consumer_thread = threading.Thread(target=iniciar_kafka_consumer, daemon=True)
    consumer_thread.start()
    time.sleep(2)

    # 2. Ejecutar el productor (envía solicitud)
    ejecutar_kafka_producer()

    # 3. Escuchar la respuesta y mostrarla
    escuchar_respuesta_kafka()

    logging.info("Flujo completo finalizado.")
