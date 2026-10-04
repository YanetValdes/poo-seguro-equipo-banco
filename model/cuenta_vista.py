"""
Módulo que define la clase CuentaVista.
"""

from model.cuenta import Cuenta
from model.cliente import Cliente
from model.saldo_insuficiente_exception import SaldoInsuficienteException
from model.cuenta_bloqueada_exception import CuentaBloqueadaException


class CuentaVista(Cuenta):
    """
    Representa una Cuenta Vista (o Cuenta RUT) en el sistema bancario.
    Hereda de Cuenta y sobrescribe métodos polimórficos de giro y mantención.
    No permite sobregiro y cobra una tarifa fija por cada giro o transacción en cajero.
    """

    def __init__(
        self,
        numero_cuenta: str,
        titular: Cliente,
        saldo_inicial: float = 0.0,
        costo_fijo_giro: float = 300.0,
        costo_mantencion_mensual: float = 0.0,
    ):
        super().__init__(numero_cuenta, titular, saldo_inicial)
        self.costo_fijo_giro = costo_fijo_giro
        self.costo_mantencion_mensual = costo_mantencion_mensual

    @property
    def costo_fijo_giro(self) -> float:
        """Retorna la comisión fija cobrada por cada giro."""
        return self.__costo_fijo_giro

    @costo_fijo_giro.setter
    def costo_fijo_giro(self, valor: float):
        """Valida que el costo de giro sea mayor o igual a 0."""
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("El costo fijo de giro debe ser un número mayor o igual a 0.")
        self.__costo_fijo_giro = float(valor)

    @property
    def costo_mantencion_mensual(self) -> float:
        """Retorna el costo de mantención mensual."""
        return self.__costo_mantencion_mensual

    @costo_mantencion_mensual.setter
    def costo_mantencion_mensual(self, valor: float):
        """Valida que el costo de mantención sea mayor o igual a 0."""
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("El costo de mantención debe ser un número mayor o igual a 0.")
        self.__costo_mantencion_mensual = float(valor)

    def girar(self, monto: float) -> str:
        """
        Sobrescritura polimórfica: Aplica un cobro fijo por operación en cada giro.
        No permite sobregiros (el saldo no puede ser negativo).
        Lanza CuentaBloqueadaException si la cuenta está bloqueada.
        Lanza SaldoInsuficienteException si el saldo no alcanza para monto + comisión.
        """
        if self.bloqueada:
            raise CuentaBloqueadaException(
                f"Giro rechazado: La Cuenta Vista N° {self.numero_cuenta} se encuentra bloqueada."
            )
        if not isinstance(monto, (int, float)) or monto <= 0:
            raise ValueError("El monto a girar debe ser mayor a 0.")

        total_requerido = monto + self.__costo_fijo_giro
        if total_requerido > self.saldo:
            raise SaldoInsuficienteException(
                f"Saldo insuficiente en Cuenta Vista N° {self.numero_cuenta}. "
                f"Saldo actual: ${self.saldo:,.0f} | Requerido (monto ${monto:,.0f} + costo fijo ${self.__costo_fijo_giro:,.0f}): "
                f"${total_requerido:,.0f}"
            )

        self.saldo -= total_requerido
        return (
            f"[{self.tipo_cuenta()}] Giro exitoso de ${monto:,.0f} "
            f"(Tarifa de operación aplicada: ${self.__costo_fijo_giro:,.0f}). "
            f"Saldo restante: ${self.saldo:,.0f}"
        )

    def calcular_costo_mantencion(self) -> float:
        """
        Sobrescritura polimórfica: Retorna la tarifa plana de mantención para Cuenta Vista.
        """
        return self.__costo_mantencion_mensual

    def tipo_cuenta(self) -> str:
        return "Cuenta Vista"
