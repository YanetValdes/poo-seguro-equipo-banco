"""
Módulo que define la clase CuentaCorriente.
"""

from model.cuenta import Cuenta
from model.cliente import Cliente
from model.saldo_insuficiente_exception import SaldoInsuficienteException
from model.cuenta_bloqueada_exception import CuentaBloqueadaException


class CuentaCorriente(Cuenta):
    """
    Representa una Cuenta Corriente en el sistema bancario.
    Hereda de Cuenta y sobrescribe métodos polimórficos de giro y mantención.
    Incorpora línea de sobregiro (crédito) y costo fijo de mantención mensual.
    """

    def __init__(
        self,
        numero_cuenta: str,
        titular: Cliente,
        saldo_inicial: float = 0.0,
        linea_sobregiro: float = 150000.0,
        costo_mantencion_base: float = 4990.0,
    ):
        super().__init__(numero_cuenta, titular, saldo_inicial)
        self.linea_sobregiro = linea_sobregiro
        self.costo_mantencion_base = costo_mantencion_base

    @property
    def linea_sobregiro(self) -> float:
        """Retorna el monto disponible para sobregiro."""
        return self.__linea_sobregiro

    @linea_sobregiro.setter
    def linea_sobregiro(self, valor: float):
        """Valida que la línea de sobregiro sea un número mayor o igual a 0."""
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("La línea de sobregiro debe ser un número mayor o igual a 0.")
        self.__linea_sobregiro = float(valor)

    @property
    def costo_mantencion_base(self) -> float:
        """Retorna la comisión de mantención base mensual."""
        return self.__costo_mantencion_base

    @costo_mantencion_base.setter
    def costo_mantencion_base(self, valor: float):
        """Valida que el costo de mantención sea mayor o igual a 0."""
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("El costo de mantención debe ser un número mayor o igual a 0.")
        self.__costo_mantencion_base = float(valor)

    @property
    def saldo_total_disponible(self) -> float:
        """Calcula el saldo propio más la línea de sobregiro."""
        return self.saldo + self.__linea_sobregiro

    def girar(self, monto: float) -> str:
        """
        Sobrescritura polimórfica: Permite girar fondos utilizando el saldo disponible
        y la línea de sobregiro autorizada.
        Lanza CuentaBloqueadaException si la cuenta está bloqueada.
        Lanza SaldoInsuficienteException si el monto excede el saldo + sobregiro.
        """
        if self.bloqueada:
            raise CuentaBloqueadaException(
                f"Giro rechazado: La Cuenta Corriente N° {self.numero_cuenta} se encuentra bloqueada."
            )
        if not isinstance(monto, (int, float)) or monto <= 0:
            raise ValueError("El monto a girar debe ser mayor a 0.")

        total_disponible = self.saldo_total_disponible
        if monto > total_disponible:
            raise SaldoInsuficienteException(
                f"Saldo insuficiente en Cuenta Corriente N° {self.numero_cuenta}. "
                f"Total disponible (Saldo ${self.saldo:,.0f} + Línea sobregiro ${self.__linea_sobregiro:,.0f}): "
                f"${total_disponible:,.0f} | Solicitado: ${monto:,.0f}"
            )

        self.saldo -= monto

        if self.saldo < 0:
            sobregiro_usado = abs(self.saldo)
            return (
                f"[{self.tipo_cuenta()}] Giro exitoso por ${monto:,.0f}. "
                f"¡AVISO!: Uso de línea de sobregiro por ${sobregiro_usado:,.0f}. "
                f"Saldo contable: ${self.saldo:,.0f} (Línea remanente: ${self.__linea_sobregiro - sobregiro_usado:,.0f})"
            )

        return (
            f"[{self.tipo_cuenta()}] Giro exitoso por ${monto:,.0f}. "
            f"Saldo disponible: ${self.saldo:,.0f}"
        )

    def calcular_costo_mantencion(self) -> float:
        """
        Sobrescritura polimórfica: Cobra mantención mensual fija más interés si hay sobregiro utilizado.
        """
        costo = self.__costo_mantencion_base
        if self.saldo < 0:
            # 2% de interés mensual sobre el monto sobregirado
            interes_sobregiro = abs(self.saldo) * 0.02
            costo += interes_sobregiro
        return costo

    def tipo_cuenta(self) -> str:
        return "Cuenta Corriente"
