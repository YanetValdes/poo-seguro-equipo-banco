"""
Módulo que define la clase Transaccion con soporte para líneas de detalle.
"""

from typing import List
from model.cuenta import Cuenta
from model.detalle_transaccion import DetalleTransaccion


class Transaccion:
    """
    Representa una transacción bancaria compuesta por múltiples líneas de detalle.
    Aplica encapsulamiento, composición y validación rigurosa de datos.
    """

    def __init__(self, id_transaccion: str, fecha: str, tipo: str, cuenta: Cuenta):
        self.id_transaccion = id_transaccion
        self.fecha = fecha
        self.tipo = tipo
        self.cuenta = cuenta
        self.__detalles: List[DetalleTransaccion] = []

    @property
    def id_transaccion(self) -> str:
        """Retorna el identificador único de la transacción."""
        return self.__id_transaccion

    @id_transaccion.setter
    def id_transaccion(self, valor: str):
        """Valida que el identificador no esté vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El ID de la transacción no puede estar vacío.")
        self.__id_transaccion = valor.strip()

    @property
    def fecha(self) -> str:
        """Retorna la fecha u hora de la transacción."""
        return self.__fecha

    @fecha.setter
    def fecha(self, valor: str):
        """Valida que la fecha no esté vacía."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La fecha no puede estar vacía.")
        self.__fecha = valor.strip()

    @property
    def tipo(self) -> str:
        """Retorna el tipo de operación efectuada."""
        return self.__tipo

    @tipo.setter
    def tipo(self, valor: str):
        """Valida que el tipo de transacción no esté vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El tipo de transacción no puede estar vacío.")
        self.__tipo = valor.strip()

    @property
    def cuenta(self) -> Cuenta:
        """Retorna la cuenta sobre la cual se ejecutó la transacción."""
        return self.__cuenta

    @cuenta.setter
    def cuenta(self, valor: Cuenta):
        """Valida que la cuenta sea una instancia válida de Cuenta."""
        if not isinstance(valor, Cuenta):
            raise TypeError("La cuenta asociada debe ser una instancia de la clase Cuenta.")
        self.__cuenta = valor

    @property
    def detalles(self) -> List[DetalleTransaccion]:
        """Retorna una copia inmutable de la lista de detalles."""
        return list(self.__detalles)

    def agregar_detalle(self, concepto: str, monto: float) -> DetalleTransaccion:
        """
        Crea y agrega una nueva línea de detalle a la transacción.
        El número de línea se calcula correlativamente.
        """
        numero_linea = len(self.__detalles) + 1
        detalle = DetalleTransaccion(numero_linea=numero_linea, concepto=concepto, monto=monto)
        self.__detalles.append(detalle)
        return detalle

    def calcular_total(self) -> float:
        """Calcula y retorna la suma de los montos de todas las líneas de detalle."""
        return sum(d.monto for d in self.__detalles)

    def generar_comprobante(self) -> str:
        """Genera un comprobante formateado con el encabezado, líneas de detalle y total."""
        lineas = [
            "=" * 60,
            f"           COMPROBANTE DE TRANSACCIÓN BANCARIA",
            "=" * 60,
            f" Folio        : {self.__id_transaccion}",
            f" Fecha        : {self.__fecha}",
            f" Tipo Operación: {self.__tipo}",
            f" Cuenta       : {self.__cuenta.tipo_cuenta()} N° {self.__cuenta.numero_cuenta}",
            f" Titular      : {self.__cuenta.titular.nombre_completo} (RUT: {self.__cuenta.titular.rut})",
            "-" * 60,
            " DESGLOSE DE LÍNEAS DE DETALLE:",
            "-" * 60,
        ]

        if not self.__detalles:
            lineas.append("  (No existen líneas de detalle registradas)")
        else:
            for d in self.__detalles:
                lineas.append(str(d))

        lineas.extend([
            "-" * 60,
            f" MONTO TOTAL OPERACIÓN: ${self.calcular_total():>15,.0f}",
            f" Saldo Posterior      : ${self.__cuenta.saldo:>15,.0f}",
            "=" * 60,
        ])
        return "\n".join(lineas)

    def __str__(self) -> str:
        return (
            f"Transacción {self.__id_transaccion} ({self.__tipo}) | "
            f"Total: ${self.calcular_total():,.0f} | Líneas: {len(self.__detalles)}"
        )
