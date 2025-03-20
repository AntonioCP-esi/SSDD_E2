from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient, NewTopic
import json
import Ice
import RemoteCalculator  # Importamos la interfaz de Ice

# Configuración de Kafka
KAFKA_BROKER = "localhost:9092"
TOPIC_REQUEST = "calculator_requests"
TOPIC_RESPONSE = "calculator_responses"

# Asegurar que los topics existen antes de usarlos
admin_client = AdminClient({'bootstrap.servers': KAFKA_BROKER})
existing_topics = admin_client.list_topics().topics

for topic in [TOPIC_REQUEST, TOPIC_RESPONSE]:
    if topic not in existing_topics:
        print(f"Creando topic: {topic}")
        admin_client.create_topics([NewTopic(topic, num_partitions=1, replication_factor=1)])

# Configurar el consumidor de Kafka
consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'calculator_group',
    'auto.offset.reset': 'earliest'  # Asegura que lee desde el inicio
}
consumer = Consumer(consumer_conf)
consumer.subscribe([TOPIC_REQUEST])

# Validar mensajes entrantes
def validar_peticion(request):
    """Verifica que la petición tiene los campos correctos."""
    if not isinstance(request, dict):
        return False, "Formato incorrecto: No es un objeto JSON válido"
    if "id" not in request or not isinstance(request["id"], str):
        return False, "Falta el campo 'id' o no es un string"
    if "operation" not in request or request["operation"] not in ["sum", "sub", "mult", "div"]:
        return False, "Operación no válida"
    if "args" not in request or not isinstance(request["args"], dict):
        return False, "Falta el campo 'args' o no es un objeto"
    if "op1" not in request["args"] or "op2" not in request["args"]:
        return False, "Faltan operandos en 'args'"
    if not isinstance(request["args"]["op1"], (int, float)) or not isinstance(request["args"]["op2"], (int, float)):
        return False, "Los operandos deben ser números"
    return True, None

# Configurar conexión con Ice
ICE_CONFIG = "config/calculator.config"
with Ice.initialize(ICE_CONFIG) as communicator:
    base = communicator.stringToProxy("calculator:tcp -h 127.0.0.1 -p 10000")
    calculator = RemoteCalculator.CalculatorPrx.checkedCast(base)

    if not calculator:
        raise RuntimeError("No se pudo conectar con el servidor Ice!")

    print("Esperando mensajes en Kafka...")

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error en Kafka: {msg.error()}")
            continue

        # 🔹 Depuración: Mostrar el mensaje en bruto antes de procesarlo
        print(f"Mensaje recibido en Kafka (RAW): {msg.value()}")

        try:
            request = json.loads(msg.value().decode('utf-8'))
            is_valid, error_msg = validar_peticion(request)

            if not is_valid:
                response = {"id": request.get("id", "unknown"), "status": False, "error": error_msg}
                print(f"⚠️ Mensaje inválido recibido: {error_msg}")
            else:
                operation = request["operation"]
                op1 = request["args"]["op1"]
                op2 = request["args"]["op2"]
                request_id = request["id"]

                if operation == "sum":
                    result = calculator.sum(op1, op2)
                elif operation == "sub":
                    result = calculator.sub(op1, op2)
                elif operation == "mult":
                    result = calculator.mult(op1, op2)
                elif operation == "div":
                    result = calculator.div(op1, op2)

                response = {"id": request_id, "status": True, "result": result}
                print(f"Operación '{operation}' realizada: {op1} {operation} {op2} = {result}")

        except Exception as e:
            response = {"id": request.get("id", "unknown"), "status": False, "error": str(e)}
            print(f"Error al procesar la solicitud: {str(e)}")

        # Publicar la respuesta en Kafka
        producer_conf = {'bootstrap.servers': KAFKA_BROKER}
        producer = Producer(producer_conf)
        producer.produce(TOPIC_RESPONSE, json.dumps(response).encode('utf-8'))
        producer.flush()

        print(f"Respuesta enviada a Kafka: {response}")
