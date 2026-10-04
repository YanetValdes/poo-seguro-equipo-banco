"""
Módulo que define la excepción CuentaBloqueadaException.
"""


class CuentaBloqueadaException(Exception):
    """
    Excepción lanzada cuando se intenta realizar una operación monetaria
    (giro, transferencia o depósito) sobre una cuenta que se encuentra bloqueada.
    """

    def __init__(self, mensaje: str = "La cuenta bancaria se encuentra bloqueada."):
        super().__init__(mensaje)
        self.__mensaje = mensaje

    @property
    def mensaje(self) -> str:
        """Retorna el mensaje explicativo de la excepción."""
        return self.__mensaje
