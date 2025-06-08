import threading
import subprocess
import logging
import Ice
from calculator.calculator import Calculator

class Server(Ice.Application):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__file__)

    def run(self, args: list[str]) -> int:
        # Iniciamos el consumidor de Kafka en un hilo aparte
        print("Iniciando consumidor de Kafka automáticamente...")
        threading.Thread(target=self.iniciar_kafka_consumer, daemon=True).start()

        # Iniciamos el servidor Ice
        servant = Calculator()
        adapter = self.communicator().createObjectAdapter("calculator")
        proxy = adapter.add(servant, self.communicator().stringToIdentity("calculator"))
        print(f"Servidor Ice iniciado con proxy: {proxy}")

        adapter.activate()
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()
        return 0

    def iniciar_kafka_consumer(self):
        """Ejecuta el consumidor de Kafka en segundo plano."""
        subprocess.run(["python", "calculator/kafka_consumer.py"])

