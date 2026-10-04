"""
Módulo que define la clase Cajero.
"""

from model.empleado import Empleado
from model.cuenta import Cuenta


class Cajero(Empleado):
    """
    Representa a un cajero bancario encargado de la atención de ventanilla.
    Hereda de Empleado y utiliza super().__init__().
    Maneja número de caja y bono por responsabilidad de caja.
    """

    def __init__(
        self,
        rut: str,
        nombre: str,
        apellido: str,
        sueldo_base: float,
        numero_caja: int = 1,
        bono_responsabilidad_caja: float = 65000.0,
    ):
        super().__init__(rut, nombre, apellido, sueldo_base)
        self.numero_caja = numero_caja
        self.bono_responsabilidad_caja = bono_responsabilidad_caja

    @property
    def numero_caja(self) -> int:
        """Retorna el número de caja asignado."""
        return self.__numero_caja

    @numero_caja.setter
    def numero_caja(self, valor: int):
        """Valida que el número de caja sea un entero positivo mayor a 0."""
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("El número de caja debe ser un entero mayor a 0.")
        self.__numero_caja = valor

    @property
    def bono_responsabilidad_caja(self) -> float:
        """Retorna el bono por manejo y cuadratura de caja."""
        return self.__bono_responsabilidad_caja

    @bono_responsabilidad_caja.setter
    def bono_responsabilidad_caja(self, valor: float):
        """Valida que el bono de caja sea numérico no negativo."""
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("El bono de caja debe ser mayor o igual a 0.")
        self.__bono_responsabilidad_caja = float(valor)

    def atender_deposito(self, cuenta: Cuenta, monto: float) -> str:
        """Procesa un depósito en ventanilla."""
        if not isinstance(cuenta, Cuenta):
            raise TypeError("La cuenta a atender debe ser una instancia de Cuenta.")
        cuenta.depositar(monto)
        return (
            f"Caja N° {self.__numero_caja} ({self.nombre_completo}): "
            f"Depósito de ${monto:,.0f} efectuado exitosamente en cuenta {cuenta.numero_cuenta}."
        )

    def atender_giro(self, cuenta: Cuenta, monto: float) -> str:
        """Procesa un giro en ventanilla."""
        if not isinstance(cuenta, Cuenta):
            raise TypeError("La cuenta a atender debe ser una instancia de Cuenta.")
        resultado_giro = cuenta.girar(monto)
        return (
            f"Caja N° {self.__numero_caja} ({self.nombre_completo}): {resultado_giro}"
        )

    def calcular_sueldo_total(self) -> float:
        """
        Sobrescritura polimórfica: Sueldo base más asignación de pérdida/responsabilidad de caja.
        """
        return self.sueldo_base + self.__bono_responsabilidad_caja

    def cargo(self) -> str:
        return "Cajero Bancario"
