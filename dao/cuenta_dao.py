"""
Módulo DAO para la jerarquía polimórfica de Cuentas Bancarias.
Implementa operaciones CRUD completas y reconstruye el subtipo correspondiente.
"""
from typing import List, Optional
from model.cuenta import Cuenta
from model.cuenta_ahorro import CuentaAhorro
from model.cuenta_corriente import CuentaCorriente
from model.cuenta_vista import CuentaVista
from dao.cliente_dao import ClienteDAO


class CuentaDAO:
    """Data Access Object para Cuentas Bancarias polimórficas."""

    def __init__(self, conexion, cliente_dao: Optional[ClienteDAO] = None):
        self.conexion = conexion
        self.cliente_dao = cliente_dao or ClienteDAO(conexion)

    def crear(self, cuenta: Cuenta) -> bool:
        """
        Inserta una cuenta bancaria asociada a un titular preexistente (CREATE).
        Si la cuenta ya existe, actualiza sus datos mediante ON CONFLICT.
        """
        query = """
            INSERT INTO cuentas (numero, rut_cliente, tipo, saldo)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(numero) DO UPDATE SET
                rut_cliente = excluded.rut_cliente,
                tipo = excluded.tipo,
                saldo = excluded.saldo
        """
        cursor = self.conexion.execute(
            query,
            (
                cuenta.numero_cuenta,
                cuenta.titular.rut,
                cuenta.tipo_cuenta(),
                cuenta.saldo,
            ),
        )
        return cursor.rowcount > 0

    def _instanciar_subtipo(self, numero: str, rut_cliente: str, tipo: str, saldo: float) -> Optional[Cuenta]:
        """Instancia la subclase polimórfica adecuada según el tipo registrado."""
        titular = self.cliente_dao.obtener_por_rut(rut_cliente)
        if not titular:
            return None

        # Si el titular tiene mora en base de datos, temporalmente permitimos
        # reconstruir la cuenta ya existente sin violar la regla de nueva apertura
        mora_previa = titular.mora_vigente
        titular.mora_vigente = False
        try:
            if "Ahorro" in tipo:
                cuenta = CuentaAhorro(numero_cuenta=numero, titular=titular, saldo_inicial=saldo)
            elif "Corriente" in tipo:
                cuenta = CuentaCorriente(numero_cuenta=numero, titular=titular, saldo_inicial=saldo)
            elif "Vista" in tipo:
                cuenta = CuentaVista(numero_cuenta=numero, titular=titular, saldo_inicial=saldo)
            else:
                cuenta = Cuenta(numero_cuenta=numero, titular=titular, saldo_inicial=saldo)
        finally:
            titular.mora_vigente = mora_previa

        return cuenta

    def obtener_por_numero(self, numero: str) -> Optional[Cuenta]:
        """Consulta una cuenta por su número identificador (READ)."""
        query = "SELECT numero, rut_cliente, tipo, saldo FROM cuentas WHERE numero = ?"
        fila = self.conexion.execute(query, (numero,)).fetchone()
        if not fila:
            return None
        return self._instanciar_subtipo(fila[0], fila[1], fila[2], fila[3])

    def listar_todas(self) -> List[Cuenta]:
        """Consulta y retorna todas las cuentas como objetos de dominio (READ)."""
        query = "SELECT numero, rut_cliente, tipo, saldo FROM cuentas ORDER BY numero"
        cuentas = []
        for fila in self.conexion.execute(query).fetchall():
            cuenta = self._instanciar_subtipo(fila[0], fila[1], fila[2], fila[3])
            if cuenta:
                cuentas.append(cuenta)
        return cuentas

    def actualizar(self, cuenta: Cuenta) -> bool:
        """Actualiza el saldo y titular de una cuenta existente (UPDATE)."""
        query = """
            UPDATE cuentas
            SET rut_cliente = ?, tipo = ?, saldo = ?
            WHERE numero = ?
        """
        cursor = self.conexion.execute(
            query,
            (
                cuenta.titular.rut,
                cuenta.tipo_cuenta(),
                cuenta.saldo,
                cuenta.numero_cuenta,
            ),
        )
        return cursor.rowcount > 0

    def eliminar(self, numero: str) -> bool:
        """Elimina una cuenta bancaria por su número (DELETE)."""
        query = "DELETE FROM cuentas WHERE numero = ?"
        cursor = self.conexion.execute(query, (numero,))
        return cursor.rowcount > 0
