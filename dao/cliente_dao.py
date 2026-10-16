"""
Módulo DAO para la entidad Cliente.
Implementa operaciones CRUD completas con consultas parametrizadas en SQLite.
"""
from typing import List, Optional
from model.cliente import Cliente


class ClienteDAO:
    """Data Access Object para la entidad Cliente."""

    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, cliente: Cliente) -> bool:
        """
        Inserta un nuevo cliente en la base de datos (CREATE).
        Si el cliente ya existe, actualiza sus datos mediante ON CONFLICT.
        """
        query = """
            INSERT INTO clientes (rut, nombre, apellido, telefono, email, mora_vigente)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(rut) DO UPDATE SET
                nombre = excluded.nombre,
                apellido = excluded.apellido,
                telefono = excluded.telefono,
                email = excluded.email,
                mora_vigente = excluded.mora_vigente
        """
        cursor = self.conexion.execute(
            query,
            (
                cliente.rut,
                cliente.nombre,
                cliente.apellido,
                cliente.telefono,
                cliente.email,
                1 if cliente.mora_vigente else 0,
            ),
        )
        return cursor.rowcount > 0

    def obtener_por_rut(self, rut: str) -> Optional[Cliente]:
        """Consulta un cliente por su clave primaria RUT (READ)."""
        query = """
            SELECT rut, nombre, apellido, telefono, email, mora_vigente
            FROM clientes
            WHERE rut = ?
        """
        fila = self.conexion.execute(query, (rut,)).fetchone()
        if not fila:
            return None
        cli = Cliente(
            rut=fila[0],
            nombre=fila[1],
            apellido=fila[2],
            telefono=fila[3],
            email=fila[4],
        )
        cli.mora_vigente = bool(fila[5])
        return cli

    def listar_todos(self) -> List[Cliente]:
        """Consulta y retorna todos los clientes registrados (READ)."""
        query = """
            SELECT rut, nombre, apellido, telefono, email, mora_vigente
            FROM clientes
            ORDER BY apellido, nombre
        """
        clientes = []
        for fila in self.conexion.execute(query).fetchall():
            cli = Cliente(
                rut=fila[0],
                nombre=fila[1],
                apellido=fila[2],
                telefono=fila[3],
                email=fila[4],
            )
            cli.mora_vigente = bool(fila[5])
            clientes.append(cli)
        return clientes

    def actualizar(self, cliente: Cliente) -> bool:
        """Actualiza los datos de un cliente existente (UPDATE)."""
        query = """
            UPDATE clientes
            SET nombre = ?, apellido = ?, telefono = ?, email = ?, mora_vigente = ?
            WHERE rut = ?
        """
        cursor = self.conexion.execute(
            query,
            (
                cliente.nombre,
                cliente.apellido,
                cliente.telefono,
                cliente.email,
                1 if cliente.mora_vigente else 0,
                cliente.rut,
            ),
        )
        return cursor.rowcount > 0

    def eliminar(self, rut: str) -> bool:
        """Elimina un cliente por su RUT (DELETE)."""
        query = "DELETE FROM clientes WHERE rut = ?"
        cursor = self.conexion.execute(query, (rut,))
        return cursor.rowcount > 0
