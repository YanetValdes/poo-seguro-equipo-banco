"""
Módulo que define la clase base Cuenta para el sistema bancario.
"""

from model.cliente import Cliente
from model.saldo_insuficiente_exception import SaldoInsuficienteException
from model.cuenta_bloqueada_exception import CuentaBloqueadaException


class Cuenta:
    """
    Clase base que representa una cuenta bancaria.
    Maneja atributos privados, encapsulamiento mediante @property,
    validaciones en setters y lanzamiento de excepciones de negocio.
    """

    def __init__(self, numero_cuenta: str, titular: Cliente, saldo_inicial: float = 0.0):
        self.numero_cuenta = numero_cuenta
        self.titular = titular
        self.__bloqueada = False
        self.__saldo = 0.0
        self.saldo = saldo_inicial

    @property
    def numero_cuenta(self) -> str:
        """Retorna el número identificador de la cuenta."""
        return self.__numero_cuenta

    @numero_cuenta.setter
    def numero_cuenta(self, valor: str):
        """Valida que el número de cuenta sea una cadena no vacía."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El número de cuenta no puede estar vacío.")
        self.__numero_cuenta = valor.strip()

    @property
    def titular(self) -> Cliente:
        """Retorna el cliente titular de la cuenta."""
        return self.__titular

    @titular.setter
    def titular(self, valor: Cliente):
        """Valida que el titular sea una instancia de la clase Cliente."""
        if not isinstance(valor, Cliente):
            raise TypeError("El titular de la cuenta debe ser una instancia de Cliente.")
        self.__titular = valor

    @property
    def saldo(self) -> float:
        """Retorna el saldo disponible de la cuenta."""
        return self.__saldo

    @saldo.setter
    def saldo(self, valor: float):
        """Valida que el saldo a asignar sea un número real."""
        if not isinstance(valor, (int, float)):
            raise TypeError("El saldo debe ser un valor numérico.")
        self.__saldo = float(valor)

    @property
    def bloqueada(self) -> bool:
        """Indica si la cuenta se encuentra bloqueada."""
        return self.__bloqueada

    @bloqueada.setter
    def bloqueada(self, estado: bool):
        """Permite bloquear o desbloquear la cuenta."""
        if not isinstance(estado, bool):
            raise TypeError("El estado de bloqueo debe ser un valor booleano.")
        self.__bloqueada = estado

    def bloquear(self):
        """Bloquea la cuenta para impedir giros y depósitos."""
        self.__bloqueada = True

    def desbloquear(self):
        """Desbloquea la cuenta habilitando operaciones."""
        self.__bloqueada = False

    def depositar(self, monto: float) -> float:
        """
        Realiza un depósito a la cuenta.
        Lanza CuentaBloqueadaException si la cuenta está bloqueada.
        """
        if self.bloqueada:
            raise CuentaBloqueadaException(
                f"No es posible depositar: la cuenta {self.numero_cuenta} se encuentra bloqueada."
            )
        if not isinstance(monto, (int, float)) or monto <= 0:
            raise ValueError("El monto a depositar debe ser un número mayor a 0.")

        self.saldo += monto
        return self.saldo

    def girar(self, monto: float) -> str:
        """
        Método polimórfico base para realizar un giro (retiro) de dinero.
        Lanza CuentaBloqueadaException si la cuenta está bloqueada.
        Lanza SaldoInsuficienteException si el saldo no alcanza para cubrir el retiro.
        """
        if self.bloqueada:
            raise CuentaBloqueadaException(
                f"No es posible girar: la cuenta {self.numero_cuenta} se encuentra bloqueada."
            )
        if not isinstance(monto, (int, float)) or monto <= 0:
            raise ValueError("El monto a girar debe ser un número mayor a 0.")

        if monto > self.saldo:
            raise SaldoInsuficienteException(
                f"Saldo insuficiente en cuenta {self.numero_cuenta}. "
                f"Saldo disponible: ${self.saldo:,.0f} | Solicitado: ${monto:,.0f}"
            )

        self.saldo -= monto
        return (
            f"[{self.tipo_cuenta()}] Giro exitoso por ${monto:,.0f}. "
            f"Nuevo saldo: ${self.saldo:,.0f}"
        )

    def calcular_costo_mantencion(self) -> float:
        """
        Método polimórfico base para calcular el costo de mantención mensual de la cuenta.
        """
        return 0.0

    def tipo_cuenta(self) -> str:
        """Retorna el nombre descriptivo del tipo de cuenta."""
        return "Cuenta Bancaria Genérica"

    def __str__(self) -> str:
        estado = "BLOQUEADA" if self.bloqueada else "ACTIVA"
        return (
            f"{self.tipo_cuenta()} N° {self.numero_cuenta} | "
            f"Titular: {self.titular.nombre_completo} | "
            f"Saldo: ${self.saldo:,.0f} | Estado: {estado}"
        )
