"""
Módulo que define la clase DetalleTransaccion (Línea de detalle).
"""


class DetalleTransaccion:
    """
    Representa una línea de detalle individual perteneciente a una transacción bancaria.
    Aplica atributos privados, getters y setters con validación.
    """

    def __init__(self, numero_linea: int, concepto: str, monto: float):
        self.numero_linea = numero_linea
        self.concepto = concepto
        self.monto = monto

    @property
    def numero_linea(self) -> int:
        """Retorna el número correlativo de la línea de detalle."""
        return self.__numero_linea

    @numero_linea.setter
    def numero_linea(self, valor: int):
        """Valida que el número de línea sea un entero mayor a 0."""
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("El número de línea debe ser un entero mayor a 0.")
        self.__numero_linea = valor

    @property
    def concepto(self) -> str:
        """Retorna la descripción o glosa del concepto."""
        return self.__concepto

    @concepto.setter
    def concepto(self, valor: str):
        """Valida que el concepto no esté vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El concepto del detalle no puede estar vacío.")
        self.__concepto = valor.strip()

    @property
    def monto(self) -> float:
        """Retorna el monto asociado a esta línea de detalle."""
        return self.__monto

    @monto.setter
    def monto(self, valor: float):
        """Valida que el monto sea un valor numérico."""
        if not isinstance(valor, (int, float)):
            raise TypeError("El monto del detalle debe ser un valor numérico.")
        self.__monto = float(valor)

    def __str__(self) -> str:
        return f"  Línea {self.__numero_linea:02d}: {self.__concepto:<35} | ${self.__monto:>10,.0f}"
