"""
Módulo que define la clase CuentaAhorro.
"""

from model.cuenta import Cuenta
from model.cliente import Cliente
from model.saldo_insuficiente_exception import SaldoInsuficienteException
from model.cuenta_bloqueada_exception import CuentaBloqueadaException


class CuentaAhorro(Cuenta):
    """
    Representa una Cuenta de Ahorro en el sistema bancario.
    Hereda de Cuenta y sobrescribe métodos polimórficos de giro y mantención.
    Tiene reglas de giros máximos gratuitos y tasa de interés preferencial.
    """

    def __init__(
        self,
        numero_cuenta: str,
        titular: Cliente,
        saldo_inicial: float = 0.0,
        tasa_interes_anual: float = 0.035,
        limite_giros_gratis: int = 2,
        costo_giro_adicional: float = 1200.0,
    ):
        super().__init__(numero_cuenta, titular, saldo_inicial)
        self.tasa_interes_anual = tasa_interes_anual
        self.limite_giros_gratis = limite_giros_gratis
        self.costo_giro_adicional = costo_giro_adicional
        self.__giros_realizados = 0

    @property
    def tasa_interes_anual(self) -> float:
        """Retorna la tasa de interés anual de la cuenta."""
        return self.__tasa_interes_anual

    @tasa_interes_anual.setter
    def tasa_interes_anual(self, valor: float):
        """Valida que la tasa de interés sea un número no negativo."""
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("La tasa de interés anual debe ser un número mayor o igual a 0.")
        self.__tasa_interes_anual = float(valor)

    @property
    def limite_giros_gratis(self) -> int:
        """Retorna el número de giros gratuitos permitidos."""
        return self.__limite_giros_gratis

    @limite_giros_gratis.setter
    def limite_giros_gratis(self, valor: int):
        """Valida que el límite de giros gratuitos sea un entero no negativo."""
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("El límite de giros gratuitos debe ser un entero no negativo.")
        self.__limite_giros_gratis = valor

    @property
    def costo_giro_adicional(self) -> float:
        """Retorna el costo cobrado por cada giro adicional."""
        return self.__costo_giro_adicional

    @costo_giro_adicional.setter
    def costo_giro_adicional(self, valor: float):
        """Valida que el costo de giro adicional sea numérico no negativo."""
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("El costo de giro adicional debe ser mayor o igual a 0.")
        self.__costo_giro_adicional = float(valor)

    @property
    def giros_realizados(self) -> int:
        """Retorna la cantidad de giros efectuados."""
        return self.__giros_realizados

    def girar(self, monto: float) -> str:
        """
        Sobrescritura polimórfica: Realiza un giro considerando el límite de giros gratuitos.
        Si se superan los giros gratuitos, se cobra una comisión adicional.
        Lanza CuentaBloqueadaException si la cuenta está bloqueada.
        Lanza SaldoInsuficienteException si el saldo no cubre el monto + comisión.
        """
        if self.bloqueada:
            raise CuentaBloqueadaException(
                f"Giro rechazado: La Cuenta de Ahorro N° {self.numero_cuenta} se encuentra bloqueada."
            )
        if not isinstance(monto, (int, float)) or monto <= 0:
            raise ValueError("El monto a girar debe ser mayor a 0.")

        comision = 0.0
        detalle_comision = "Giro gratuito dentro del límite permitido."
        if self.__giros_realizados >= self.__limite_giros_gratis:
            comision = self.__costo_giro_adicional
            detalle_comision = f"Límite de giros gratuitos alcanzado. Se aplicó cargo por ${comision:,.0f}."

        total_a_descontar = monto + comision

        if total_a_descontar > self.saldo:
            raise SaldoInsuficienteException(
                f"Saldo insuficiente en Cuenta de Ahorro N° {self.numero_cuenta}. "
                f"Saldo actual: ${self.saldo:,.0f} | Requerido (monto ${monto:,.0f} + comisión ${comision:,.0f}): "
                f"${total_a_descontar:,.0f}"
            )

        self.saldo -= total_a_descontar
        self.__giros_realizados += 1

        return (
            f"[{self.tipo_cuenta()}] Giro exitoso de ${monto:,.0f} (Giro #{self.__giros_realizados}). "
            f"{detalle_comision} Saldo restante: ${self.saldo:,.0f}"
        )

    def calcular_costo_mantencion(self) -> float:
        """
        Sobrescritura polimórfica: La cuenta de ahorro tiene costo de mantención $0
        (orientada al fomento del ahorro).
        """
        return 0.0

    def calcular_interes_mensual(self) -> float:
        """Calcula la ganancia de interés mensual según la tasa anual pactada."""
        tasa_mensual = self.__tasa_interes_anual / 12
        return self.saldo * tasa_mensual

    def tipo_cuenta(self) -> str:
        return "Cuenta de Ahorro"
