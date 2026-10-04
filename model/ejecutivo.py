"""
Módulo que define la clase Ejecutivo.
"""

from model.empleado import Empleado
from model.credito import Credito


class Ejecutivo(Empleado):
    """
    Representa a un ejecutivo comercial de banco.
    Hereda de Empleado y utiliza super().__init__().
    Tiene la facultad de evaluar y aprobar créditos, recibiendo comisiones por venta.
    """

    def __init__(
        self,
        rut: str,
        nombre: str,
        apellido: str,
        sueldo_base: float,
        comision_por_credito: float = 35000.0,
    ):
        super().__init__(rut, nombre, apellido, sueldo_base)
        self.comision_por_credito = comision_por_credito
        self.__creditos_aprobados = 0

    @property
    def comision_por_credito(self) -> float:
        """Retorna el valor de la comisión asignada por cada crédito aprobado."""
        return self.__comision_por_credito

    @comision_por_credito.setter
    def comision_por_credito(self, valor: float):
        """Valida que la comisión sea un número no negativo."""
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("La comisión por crédito debe ser un número mayor o igual a 0.")
        self.__comision_por_credito = float(valor)

    @property
    def creditos_aprobados(self) -> int:
        """Retorna la cantidad de créditos aprobados por el ejecutivo."""
        return self.__creditos_aprobados

    def aprobar_credito(self, credito: Credito) -> str:
        """
        Aprueba formalmente un crédito bancario y registra la comisión para el ejecutivo.
        """
        if not isinstance(credito, Credito):
            raise TypeError("El objeto a aprobar debe ser una instancia de Credito.")
        if credito.aprobado:
            return f"El crédito N° {credito.codigo} ya se encontraba previamente aprobado."

        credito.aprobado = True
        self.__creditos_aprobados += 1
        return (
            f"Ejecutivo {self.nombre_completo} aprobó con éxito el crédito N° {credito.codigo} "
            f"para {credito.cliente.nombre_completo} por ${credito.monto_solicitado:,.0f}."
        )

    def calcular_sueldo_total(self) -> float:
        """
        Sobrescritura polimórfica: Sueldo base más las comisiones por créditos aprobados.
        """
        comisiones_totales = self.__creditos_aprobados * self.__comision_por_credito
        return self.sueldo_base + comisiones_totales

    def cargo(self) -> str:
        return "Ejecutivo de Cuentas"
