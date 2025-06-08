import Ice
import RemoteCalculator  # Nos aseguramos de que no haya errores con la importaciñon

# Configuramos conexión con el servidor Ice
ICE_CONFIG = "config/calculator.config"

with Ice.initialize(ICE_CONFIG) as communicator:
    base = communicator.stringToProxy("calculator:tcp -h 127.0.0.1 -p 10000")
    calculator = RemoteCalculator.CalculatorPrx.checkedCast(base)

    if not calculator:
        raise RuntimeError("No se pudo conectar con el servidor Ice")

    # Probamos una operación
    resultado = calculator.sum(10.0, 20.0)
    print(f"Resultado de la suma: {resultado}")
