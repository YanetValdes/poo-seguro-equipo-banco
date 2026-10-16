"""
Módulo DAO para la entidad Transaccion y sus líneas de detalle.
Implementa operaciones CRUD completas y maneja la composición con DetalleTransaccion.
"""
from typing import List, Optional
from model.transaccion import Transaccion
from dao.cuenta_dao import CuentaDAO


class TransaccionDAO:
    """Data Access Object para Transacciones bancarias y sus detalles."""

    def __init__(self, conexion, cuenta_dao: Optional[CuentaDAO] = None):
        self.conexion = conexion
        self.cuenta_dao = cuenta_dao or CuentaDAO(conexion)

    def crear(self, transaccion: Transaccion) -> bool:
        """
        Inserta la cabecera de la transacción y sus detalles (CREATE).
        Si la transacción ya existe, actualiza los datos.
        """
        detalles = transaccion.detalles
        if not detalles:
            raise ValueError("Una transacción debe incluir por lo menos una línea de detalle.")

        query_trx = """
            INSERT INTO transacciones (id, numero_cuenta, fecha, tipo)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                numero_cuenta = excluded.numero_cuenta,
                fecha = excluded.fecha,
                tipo = excluded.tipo
        """
        self.conexion.execute(
            query_trx,
            (
                transaccion.id_transaccion,
                transaccion.cuenta.numero_cuenta,
                transaccion.fecha,
                transaccion.tipo,
            ),
        )

        # Reemplazar detalles asociados
        self.conexion.execute("DELETE FROM detalles WHERE transaccion_id = ?", (transaccion.id_transaccion,))
        query_det = """
            INSERT INTO detalles (transaccion_id, posicion, concepto, monto)
            VALUES (?, ?, ?, ?)
        """
        self.conexion.executemany(
            query_det,
            [
                (transaccion.id_transaccion, d.numero_linea, d.concepto, d.monto)
                for d in detalles
            ],
        )
        return True

    def obtener_por_id(self, id_transaccion: str) -> Optional[Transaccion]:
        """Consulta una transacción por su ID con todos sus detalles (READ)."""
        query_trx = """
            SELECT id, numero_cuenta, fecha, tipo
            FROM transacciones
            WHERE id = ?
        """
        fila_trx = self.conexion.execute(query_trx, (id_transaccion,)).fetchone()
        if not fila_trx:
            return None

        cuenta = self.cuenta_dao.obtener_por_numero(fila_trx[1])
        if not cuenta:
            return None

        transaccion = Transaccion(
            id_transaccion=fila_trx[0],
            fecha=fila_trx[2],
            tipo=fila_trx[3],
            cuenta=cuenta,
        )

        # Cargar detalles
        query_det = """
            SELECT posicion, concepto, monto
            FROM detalles
            WHERE transaccion_id = ?
            ORDER BY posicion
        """
        for det_fila in self.conexion.execute(query_det, (id_transaccion,)).fetchall():
            transaccion.agregar_detalle(concepto=det_fila[1], monto=det_fila[2])

        return transaccion

    def listar_todas(self) -> List[Transaccion]:
        """Consulta y retorna todas las transacciones registradas (READ)."""
        query = "SELECT id FROM transacciones ORDER BY fecha DESC"
        transacciones = []
        for fila in self.conexion.execute(query).fetchall():
            trx = self.obtener_por_id(fila[0])
            if trx:
                transacciones.append(trx)
        return transacciones

    def actualizar(self, transaccion: Transaccion) -> bool:
        """Actualiza una transacción existente y sus líneas de detalle (UPDATE)."""
        return self.crear(transaccion)

    def eliminar(self, id_transaccion: str) -> bool:
        """Elimina una transacción y sus detalles asociados (DELETE)."""
        self.conexion.execute("DELETE FROM detalles WHERE transaccion_id = ?", (id_transaccion,))
        cursor = self.conexion.execute("DELETE FROM transacciones WHERE id = ?", (id_transaccion,))
        return cursor.rowcount > 0

    def contar_detalles(self, id_transaccion: str) -> int:
        """Retorna la cantidad de líneas de detalle asociadas a una transacción."""
        query = "SELECT COUNT(*) FROM detalles WHERE transaccion_id = ?"
        return self.conexion.execute(query, (id_transaccion,)).fetchone()[0]
