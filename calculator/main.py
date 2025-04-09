import threading
import logging
import subprocess
import time
import Ice
from confluent_kafka import AdminClient

# Configuración
KAFKA_BROKER = "localhost:9092"
TOPIC_REQUEST = "calculator_requests"
TOPIC_RESPONSE = "calculator_responses"

def verificar_servidor_ice():
    """Verifica si el servidor Ice está en ejecución antes de continuar."""
    logging.info("Verificando servidor Ice...")
    intentos = 10  # Intentará conectarse hasta 10 veces
    while intentos > 0:
        try:
            with Ice.initialize() as communicator:
                base = communicator.stringToProxy("calculator:tcp -h 127.0.0.1 -p 10000")
                calculator = Ice.checkedCast(base, Ice.ObjectPrx)
                if calculator:
                    logging.info("✅ Servidor Ice está en ejecución.")
                    return True
        except Exception:
            pass
        logging.warning("⏳ Esperando que el servidor Ice inicie...")
        time.sleep(3)
        intentos -= 1

    logging.error("❌ No se pudo conectar al servidor Ice. Asegúrate de iniciarlo.")
    return False

def iniciar_kafka_consumer():
    """Ejecuta el consumidor de Kafka en un hilo separado."""
    logging.info("Iniciando consumidor de Kafka...")
    subprocess.run(["python", "calculator/kafka_consumer.py"])

def verificar_kafka():
    """Verifica si Kafka está en ejecución y los topics existen."""
    logging.info("Verificando conexión con Kafka...")
    try:
        admin_client = AdminClient({'bootstrap.servers': KAFKA_BROKER})
        existing_topics = admin_client.list_topics(timeout=5).topics

        if TOPIC_REQUEST not in existing_topics or TOPIC_RESPONSE not in existing_topics:
            logging.warning(f"⚠️ No se encontraron los topics {TOPIC_REQUEST} o {TOPIC_RESPONSE}.")
            return False
        logging.info("✅ Kafka está en ejecución y los topics existen.")
        return True
    except Exception as e:
        logging.error(f"❌ Error al conectar con Kafka: {e}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Verificar que Kafka y el servidor Ice están en ejecución antes de continuar
    if not verificar_kafka():
        logging.error("No se puede iniciar el consumidor sin Kafka.")
        exit(1)

    if not verificar_servidor_ice():
        exit(1)

    # Iniciar el consumidor de Kafka en un hilo separado
    kafka_thread = threading.Thread(target=iniciar_kafka_consumer, daemon=True)
    kafka_thread.start()

    # Mantener el programa corriendo hasta que se detenga manualmente
    kafka_thread.join()
