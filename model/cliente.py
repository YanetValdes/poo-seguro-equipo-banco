"""
Módulo que define la clase Cliente del sistema bancario.
"""


class Cliente:
    """
    Representa a un cliente del banco.
    Aplica encapsulamiento mediante atributos privados, properties y validaciones en setters.
    """

    def __init__(self, rut: str, nombre: str, apellido: str, telefono: str, email: str):
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email

    @property
    def rut(self) -> str:
        """Retorna el RUT del cliente."""
        return self.__rut

    @rut.setter
    def rut(self, valor: str):
        """Valida que el RUT no esté vacío y tenga una longitud mínima válida."""
        if not isinstance(valor, str) or len(valor.strip()) < 8:
            raise ValueError("El RUT debe ser una cadena válida de al menos 8 caracteres.")
        self.__rut = valor.strip()

    @property
    def nombre(self) -> str:
        """Retorna el nombre del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        """Valida que el nombre no esté vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def apellido(self) -> str:
        """Retorna el apellido del cliente."""
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str):
        """Valida que el apellido no esté vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El apellido no puede estar vacío.")
        self.__apellido = valor.strip()

    @property
    def telefono(self) -> str:
        """Retorna el teléfono de contacto del cliente."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        """Asigna el teléfono de contacto."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El teléfono no puede estar vacío.")
        self.__telefono = valor.strip()

    @property
    def email(self) -> str:
        """Retorna el correo electrónico del cliente."""
        return self.__email

    @email.setter
    def email(self, valor: str):
        """Valida que el email contenga formato básico (@ y punto)."""
        if not isinstance(valor, str) or "@" not in valor or "." not in valor:
            raise ValueError("El correo electrónico debe tener un formato válido (ej. usuario@dominio.cl).")
        self.__email = valor.strip()

    @property
    def nombre_completo(self) -> str:
        """Retorna el nombre completo del cliente."""
        return f"{self.__nombre} {self.__apellido}"

    def __str__(self) -> str:
        return f"Cliente: {self.nombre_completo} | RUT: {self.__rut} | Email: {self.__email}"
