"""
Paquete dao (Data Access Object) para el Sistema Bancario.
Proporciona acceso a datos SQLite con operaciones CRUD completas y consultas parametrizadas.
"""

from dao.conexion import conectar_db, ESQUEMA
from dao.cliente_dao import ClienteDAO
from dao.cuenta_dao import CuentaDAO
from dao.transaccion_dao import TransaccionDAO

__all__ = [
    "conectar_db",
    "ESQUEMA",
    "ClienteDAO",
    "CuentaDAO",
    "TransaccionDAO",
]
