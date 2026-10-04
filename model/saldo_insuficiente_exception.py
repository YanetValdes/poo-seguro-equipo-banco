"""
Módulo que define la excepción SaldoInsuficienteException.
"""


class SaldoInsuficienteException(Exception):
    """
    Excepción lanzada cuando una cuenta no posee saldo suficiente
    (considerando saldo disponible o línea de crédito/sobregiro)
    para completar una operación.
    """

    def __init__(self, mensaje: str = "Saldo insuficiente para realizar la operación."):
        super().__init__(mensaje)
        self.__mensaje = mensaje

    @property
    def mensaje(self) -> str:
        """Retorna el mensaje explicativo de la excepción."""
        return self.__mensaje
