"""
Módulo que define la clase base Empleado.
"""


class Empleado:
    """
    Clase base que representa a un funcionario o empleado del banco.
    Aplica encapsulamiento mediante atributos privados, properties y validaciones en setters.
    """

    def __init__(self, rut: str, nombre: str, apellido: str, sueldo_base: float):
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.sueldo_base = sueldo_base

    @property
    def rut(self) -> str:
        """Retorna el RUT del empleado."""
        return self.__rut

    @rut.setter
    def rut(self, valor: str):
        """Valida que el RUT no esté vacío y tenga una longitud mínima válida."""
        if not isinstance(valor, str) or len(valor.strip()) < 8:
            raise ValueError("El RUT del empleado debe ser una cadena válida de al menos 8 caracteres.")
        self.__rut = valor.strip()

    @property
    def nombre(self) -> str:
        """Retorna el nombre del empleado."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        """Valida que el nombre no esté vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del empleado no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def apellido(self) -> str:
        """Retorna el apellido del empleado."""
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str):
        """Valida que el apellido no esté vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El apellido del empleado no puede estar vacío.")
        self.__apellido = valor.strip()

    @property
    def sueldo_base(self) -> float:
        """Retorna el sueldo base del empleado."""
        return self.__sueldo_base

    @sueldo_base.setter
    def sueldo_base(self, valor: float):
        """Valida que el sueldo base sea un valor numérico superior a 0."""
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("El sueldo base debe ser un valor numérico mayor a 0.")
        self.__sueldo_base = float(valor)

    @property
    def nombre_completo(self) -> str:
        """Retorna el nombre completo del empleado."""
        return f"{self.__nombre} {self.__apellido}"

    def calcular_sueldo_total(self) -> float:
        """Método polimórfico base para calcular la remuneración líquida total."""
        return self.__sueldo_base

    def cargo(self) -> str:
        """Retorna el cargo o rol del empleado."""
        return "Empleado Bancario"

    def __str__(self) -> str:
        return (
            f"[{self.cargo()}] {self.nombre_completo} | RUT: {self.__rut} | "
            f"Sueldo Base: ${self.__sueldo_base:,.0f} | Total: ${self.calcular_sueldo_total():,.0f}"
        )
