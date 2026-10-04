"""
Módulo que define la clase Credito.
"""

from typing import List
from model.cliente import Cliente
from model.cuota_credito import CuotaCredito


class Credito:
    """
    Representa un crédito solicitado por un cliente.
    Contiene el monto solicitado, la tasa de interés, el plazo en meses,
    y gestiona una colección de cuotas (CuotaCredito).
    """

    def __init__(
        self,
        codigo: str,
        cliente: Cliente,
        monto_solicitado: float,
        tasa_interes: float = 0.05,
        plazo_meses: int = 12,
    ):
        self.codigo = codigo
        self.cliente = cliente
        self.monto_solicitado = monto_solicitado
        self.tasa_interes = tasa_interes
        self.plazo_meses = plazo_meses
        self.__aprobado = False
        self.__cuotas: List[CuotaCredito] = []
        self.generar_cuotas()

    @property
    def codigo(self) -> str:
        """Retorna el código único del crédito."""
        return self.__codigo

    @codigo.setter
    def codigo(self, valor: str):
        """Valida que el código sea una cadena no vacía."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código del crédito no puede estar vacío.")
        self.__codigo = valor.strip()

    @property
    def cliente(self) -> Cliente:
        """Retorna el cliente titular del crédito."""
        return self.__cliente

    @cliente.setter
    def cliente(self, valor: Cliente):
        """Valida que el cliente sea una instancia de Cliente."""
        if not isinstance(valor, Cliente):
            raise TypeError("El titular del crédito debe ser un objeto Cliente válido.")
        self.__cliente = valor

    @property
    def monto_solicitado(self) -> float:
        """Retorna el monto solicitado en el crédito."""
        return self.__monto_solicitado

    @monto_solicitado.setter
    def monto_solicitado(self, valor: float):
        """Valida que el monto solicitado sea un número mayor a cero."""
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("El monto solicitado debe ser mayor a 0.")
        self.__monto_solicitado = float(valor)

    @property
    def tasa_interes(self) -> float:
        """Retorna la tasa de interés global del crédito."""
        return self.__tasa_interes

    @tasa_interes.setter
    def tasa_interes(self, valor: float):
        """Valida que la tasa de interés sea mayor o igual a 0."""
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("La tasa de interés debe ser mayor o igual a 0.")
        self.__tasa_interes = float(valor)

    @property
    def plazo_meses(self) -> int:
        """Retorna el número de meses pactado para pagar el crédito."""
        return self.__plazo_meses

    @plazo_meses.setter
    def plazo_meses(self, valor: int):
        """Valida que el plazo de meses sea un entero positivo mayor a cero."""
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("El plazo en meses debe ser un entero mayor a 0.")
        self.__plazo_meses = valor

    @property
    def aprobado(self) -> bool:
        """Indica si el crédito está aprobado por un ejecutivo."""
        return self.__aprobado

    @aprobado.setter
    def aprobado(self, valor: bool):
        """Asigna el estado de aprobación del crédito."""
        if not isinstance(valor, bool):
            raise TypeError("El estado de aprobación debe ser un valor booleano.")
        self.__aprobado = valor

    @property
    def cuotas(self) -> List[CuotaCredito]:
        """Retorna la lista de cuotas asociadas al crédito."""
        return list(self.__cuotas)

    @property
    def monto_total(self) -> float:
        """Calcula el monto total final a pagar incluyendo los intereses."""
        return self.__monto_solicitado * (1.0 + self.__tasa_interes)

    def generar_cuotas(self):
        """Genera las cuotas del crédito dividiendo el monto total entre el plazo en meses."""
        self.__cuotas.clear()
        valor_cuota = self.monto_total / self.__plazo_meses
        for i in range(1, self.__plazo_meses + 1):
            fecha = f"Mes {i:02d}"
            cuota = CuotaCredito(numero_cuota=i, monto=valor_cuota, fecha_vencimiento=fecha)
            self.__cuotas.append(cuota)

    def pagar_cuota(self, numero_cuota: int):
        """Marca una cuota como pagada por su número."""
        for c in self.__cuotas:
            if c.numero_cuota == numero_cuota:
                c.pagar()
                return
        raise ValueError(f"No se encontró la cuota N° {numero_cuota} en el crédito {self.__codigo}.")

    def saldo_pendiente(self) -> float:
        """Retorna la suma total de las cuotas que aún no han sido pagadas."""
        return sum(c.monto for c in self.__cuotas if not c.pagada)

    def __str__(self) -> str:
        estado = "APROBADO" if self.__aprobado else "PENDIENTE APROBACIÓN"
        return (
            f"Crédito N° {self.__codigo} | Cliente: {self.cliente.nombre_completo} | "
            f"Monto Solicitado: ${self.__monto_solicitado:,.0f} | Total a pagar: ${self.monto_total:,.0f} | "
            f"Plazo: {self.__plazo_meses} meses | Estado: {estado}"
        )
