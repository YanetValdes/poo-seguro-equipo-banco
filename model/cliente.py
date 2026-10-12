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
        self.__mora_vigente = False

    @property
    def rut(self) -> str:
        """Retorna el RUT del cliente."""
        return self.__rut

    @rut.setter
    def rut(self, valor: str):
        """Valida formato y dígito verificador del RUT chileno (módulo 11)."""
        if not isinstance(valor, str):
            raise ValueError("El RUT debe ser texto.")
        limpio = valor.strip().replace(".", "").replace("-", "").upper()
        if len(limpio) < 8 or len(limpio) > 9 or not limpio[:-1].isdigit() or limpio[-1] not in "0123456789K":
            raise ValueError("Formato de RUT inválido.")
        numero, dv = limpio[:-1], limpio[-1]
        suma = sum(int(digito) * (2 + i % 6) for i, digito in enumerate(reversed(numero)))
        calculado = 11 - (suma % 11)
        esperado = "0" if calculado == 11 else "K" if calculado == 10 else str(calculado)
        if dv != esperado:
            raise ValueError("RUT inválido: el dígito verificador no corresponde.")
        self.__rut = f"{int(numero)}-{dv}"

    @property
    def mora_vigente(self) -> bool:
        """Indica si el cliente registra mora vigente."""
        return self.__mora_vigente

    @mora_vigente.setter
    def mora_vigente(self, valor: bool):
        if not isinstance(valor, bool):
            raise TypeError("La mora vigente debe ser True o False.")
        self.__mora_vigente = valor

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
