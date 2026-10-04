"""
Módulo que define la clase CuotaCredito.
"""


class CuotaCredito:
    """
    Representa una cuota individual perteneciente a un crédito bancario.
    Maneja el número de cuota, el monto a pagar, la fecha de vencimiento y su estado de pago.
    """

    def __init__(self, numero_cuota: int, monto: float, fecha_vencimiento: str):
        self.numero_cuota = numero_cuota
        self.monto = monto
        self.fecha_vencimiento = fecha_vencimiento
        self.__pagada = False

    @property
    def numero_cuota(self) -> int:
        """Retorna el número correlativo de la cuota."""
        return self.__numero_cuota

    @numero_cuota.setter
    def numero_cuota(self, valor: int):
        """Valida que el número de cuota sea un entero positivo mayor a 0."""
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("El número de cuota debe ser un entero mayor a 0.")
        self.__numero_cuota = valor

    @property
    def monto(self) -> float:
        """Retorna el valor monetario de la cuota."""
        return self.__monto

    @monto.setter
    def monto(self, valor: float):
        """Valida que el monto de la cuota sea numérico y positivo."""
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("El monto de la cuota debe ser un valor numérico mayor a 0.")
        self.__monto = float(valor)

    @property
    def fecha_vencimiento(self) -> str:
        """Retorna la fecha de vencimiento en formato texto (ej. YYYY-MM-DD)."""
        return self.__fecha_vencimiento

    @fecha_vencimiento.setter
    def fecha_vencimiento(self, valor: str):
        """Valida que la fecha de vencimiento sea una cadena válida no vacía."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La fecha de vencimiento no puede estar vacía.")
        self.__fecha_vencimiento = valor.strip()

    @property
    def pagada(self) -> bool:
        """Indica si la cuota ha sido pagada."""
        return self.__pagada

    def pagar(self):
        """Marca la cuota como pagada."""
        if self.__pagada:
            raise ValueError(f"La cuota N° {self.__numero_cuota} ya se encuentra pagada.")
        self.__pagada = True

    def __str__(self) -> str:
        estado = "PAGADA" if self.__pagada else "PENDIENTE"
        return (
            f"Cuota N° {self.__numero_cuota:02d} | "
            f"Monto: ${self.__monto:,.0f} | "
            f"Vencimiento: {self.__fecha_vencimiento} | Estado: {estado}"
        )
