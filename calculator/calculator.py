import RemoteCalculator

class Calculator(RemoteCalculator.Calculator):
    def sum(self, a: float, b: float, context=None) -> float:
        print(f"[Servidor Ice] Recibida SUMA: {a} + {b}")  # DEBUG
        return a + b

    def sub(self, a: float, b: float, context=None) -> float:
        print(f"[Servidor Ice] Recibida RESTA: {a} - {b}")  # DEBUG
        return a - b

    def mult(self, a: float, b: float, context=None) -> float:
        print(f"[Servidor Ice] Recibida MULTIPLICACIÓN: {a} * {b}")  # DEBUG
        return a * b

    def div(self, a: float, b: float, context=None) -> float:
        if b == 0:
            raise RemoteCalculator.ZeroDivisionError()
        print(f"[Servidor Ice] Recibida DIVISIÓN: {a} / {b}")  # DEBUG
        return a / b

