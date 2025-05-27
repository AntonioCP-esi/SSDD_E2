import subprocess
import threading
import logging
import time
import Ice
import json
from confluent_kafka import Consumer

# Configuración
KAFKA_BROKER = "localhost:9092"
TOPIC_RESPONSE = "calculator_responses"

def iniciar_servidor_ice():
    logging.info("🧊 Iniciando servidor Ice...")
    return subprocess.Popen(["python", "-m", "calculator.command_handlers", "calculator"])

def verificar_servidor_ice():
    logging.info("🔎 Verificando servidor Ice...")
    intentos = 10
    while intentos > 0:
        try:
            with Ice.initialize() as communicator:
                base = communicator.stringToProxy("calculator:tcp -h 127.0.0.1 -p 10000")
                proxy = Ice.checkedCast(base, Ice.ObjectPrx)
                if proxy:
                    logging.info("✅ Servidor Ice en ejecución.")
                    return True
        except:
            pass
        logging.warning("⏳ Esperando al servidor Ice...")
        time.sleep(2)
        intentos -= 1
    logging.error("❌ No se pudo conectar con el servidor Ice.")
    return False

def iniciar_kafka_consumer():
    logging.info("🟡 Iniciando consumidor de Kafka...")
    subprocess.run(["python", "calculator/kafka_consumer.py"])

def ejecutar_kafka_producer():
    logging.info("🟢 Enviando solicitud desde el productor Kafka...")
    subprocess.run(["python", "calculator/kafka_producer.py"])

def escuchar_respuesta_kafka():
    logging.info("📥 Escuchando respuestas de Kafka...")
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
            logging.info(f"✅ Respuesta recibida de Kafka: {data}")
            break
        except Exception as e:
            logging.error(f"Error al procesar la respuesta: {e}")
    consumer.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # 1. Iniciar el servidor Ice
    server_proc = iniciar_servidor_ice()
    time.sleep(2)

    # 2. Verificar que está listo
    if not verificar_servidor_ice():
        server_proc.kill()
        exit(1)

    # 3. Iniciar el consumidor en un hilo
    consumer_thread = threading.Thread(target=iniciar_kafka_consumer, daemon=True)
    consumer_thread.start()
    time.sleep(2)

    # 4. Ejecutar el productor (envía solicitud)
    ejecutar_kafka_producer()

    # 5. Escuchar la respuesta y mostrarla
    escuchar_respuesta_kafka()

    # 6. Cierre opcional (detener servidor si quieres)
    server_proc.terminate()
    logging.info("✅ Flujo completo finalizado.")
