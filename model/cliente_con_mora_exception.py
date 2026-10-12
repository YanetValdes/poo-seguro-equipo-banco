"""Excepción para la regla que prohíbe abrir cuentas con mora vigente."""

class ClienteConMoraException(Exception):
    """Se lanza al intentar abrir una cuenta para un cliente con mora vigente."""
