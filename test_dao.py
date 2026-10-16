"""
Pruebas automatizadas para la capa DAO (Data Access Object) del Sistema Bancario.
Verifica operaciones CRUD completas (Crear, Consultar, Actualizar, Eliminar)
y claves foráneas en SQLite.
"""
import sqlite3
import tempfile
import unittest
from pathlib import Path

from dao.conexion import conectar_db
from dao.cliente_dao import ClienteDAO
from dao.cuenta_dao import CuentaDAO
from dao.transaccion_dao import TransaccionDAO

from model.cliente import Cliente
from model.cuenta_ahorro import CuentaAhorro
from model.cuenta_corriente import CuentaCorriente
from model.cuenta_vista import CuentaVista
from model.transaccion import Transaccion


class DAOTest(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp_dir.name) / "test_dao.sqlite3"
        self.conexion = conectar_db(self.db_path)
        self.cliente_dao = ClienteDAO(self.conexion)
        self.cuenta_dao = CuentaDAO(self.conexion, self.cliente_dao)
        self.transaccion_dao = TransaccionDAO(self.conexion, self.cuenta_dao)

        self.cliente1 = Cliente(
            rut="18.765.432-7",
            nombre="Matías",
            apellido="Tapia",
            telefono="+56987654321",
            email="matias.tapia@banco.cl",
        )
        self.cuenta_vista = CuentaVista(
            numero_cuenta="CV-101",
            titular=self.cliente1,
            saldo_inicial=50000.0,
        )

    def tearDown(self):
        self.conexion.close()
        self.tmp_dir.cleanup()

    # -------------------------------------------------------------------------
    # PRUEBAS CRUD CLIENTEDAO
    # -------------------------------------------------------------------------
    def test_cliente_dao_crud_completo(self):
        # 1. CREATE
        creado = self.cliente_dao.crear(self.cliente1)
        self.assertTrue(creado)

        # 2. READ (por RUT)
        recuperado = self.cliente_dao.obtener_por_rut(self.cliente1.rut)
        self.assertIsNotNone(recuperado)
        self.assertEqual(recuperado.rut, self.cliente1.rut)
        self.assertEqual(recuperado.nombre, "Matías")
        self.assertEqual(recuperado.telefono, "+56987654321")
        self.assertEqual(recuperado.email, "matias.tapia@banco.cl")
        self.assertFalse(recuperado.mora_vigente)

        # READ (listar todos)
        todos = self.cliente_dao.listar_todos()
        self.assertEqual(len(todos), 1)

        # 3. UPDATE
        self.cliente1.nombre = "Matías Ignacio"
        self.cliente1.mora_vigente = True
        actualizado = self.cliente_dao.actualizar(self.cliente1)
        self.assertTrue(actualizado)

        modificado = self.cliente_dao.obtener_por_rut(self.cliente1.rut)
        self.assertEqual(modificado.nombre, "Matías Ignacio")
        self.assertTrue(modificado.mora_vigente)

        # 4. DELETE
        eliminado = self.cliente_dao.eliminar(self.cliente1.rut)
        self.assertTrue(eliminado)
        self.assertIsNone(self.cliente_dao.obtener_por_rut(self.cliente1.rut))
        self.assertEqual(len(self.cliente_dao.listar_todos()), 0)

    # -------------------------------------------------------------------------
    # PRUEBAS CRUD CUENTADAO Y POLIMORFISMO
    # -------------------------------------------------------------------------
    def test_cuenta_dao_crud_y_polimorfismo(self):
        self.cliente_dao.crear(self.cliente1)

        # 1. CREATE para tres subtipos polimórficos
        c_ahorro = CuentaAhorro("AH-201", self.cliente1, 80000.0)
        c_corriente = CuentaCorriente("CC-202", self.cliente1, 20000.0)
        c_vista = CuentaVista("CV-203", self.cliente1, 50000.0)

        self.assertTrue(self.cuenta_dao.crear(c_ahorro))
        self.assertTrue(self.cuenta_dao.crear(c_corriente))
        self.assertTrue(self.cuenta_dao.crear(c_vista))

        # 2. READ y verificación de reconstrucción de clase exacta
        rec_ahorro = self.cuenta_dao.obtener_por_numero("AH-201")
        rec_corriente = self.cuenta_dao.obtener_por_numero("CC-202")
        rec_vista = self.cuenta_dao.obtener_por_numero("CV-203")

        self.assertIsInstance(rec_ahorro, CuentaAhorro)
        self.assertIsInstance(rec_corriente, CuentaCorriente)
        self.assertIsInstance(rec_vista, CuentaVista)

        self.assertEqual(rec_ahorro.saldo, 80000.0)
        self.assertEqual(rec_corriente.saldo, 20000.0)
        self.assertEqual(rec_vista.saldo, 50000.0)

        # READ (listar todas)
        todas = self.cuenta_dao.listar_todas()
        self.assertEqual(len(todas), 3)

        # 3. UPDATE
        rec_vista.saldo = 45000.0
        self.assertTrue(self.cuenta_dao.actualizar(rec_vista))
        releida = self.cuenta_dao.obtener_por_numero("CV-203")
        self.assertEqual(releida.saldo, 45000.0)

        # 4. DELETE
        self.assertTrue(self.cuenta_dao.eliminar("CV-203"))
        self.assertIsNone(self.cuenta_dao.obtener_por_numero("CV-203"))
        self.assertEqual(len(self.cuenta_dao.listar_todas()), 2)

    # -------------------------------------------------------------------------
    # PRUEBAS CRUD TRANSACCIONDAO Y COMPOSICIÓN DETALLES
    # -------------------------------------------------------------------------
    def test_transaccion_dao_crud_con_detalles(self):
        self.cliente_dao.crear(self.cliente1)
        self.cuenta_dao.crear(self.cuenta_vista)

        # 1. CREATE con líneas de detalle
        trx = Transaccion("TRX-001", "2026-10-15 10:00:00", "Giro Cajero", self.cuenta_vista)
        trx.agregar_detalle("Retiro de dinero", 20000.0)
        trx.agregar_detalle("Comisión por uso de cajero", 300.0)
        self.assertTrue(self.transaccion_dao.crear(trx))

        # 2. READ por ID y composición de detalles
        rec_trx = self.transaccion_dao.obtener_por_id("TRX-001")
        self.assertIsNotNone(rec_trx)
        self.assertEqual(rec_trx.id_transaccion, "TRX-001")
        self.assertEqual(rec_trx.cuenta.numero_cuenta, "CV-101")
        self.assertEqual(len(rec_trx.detalles), 2)
        self.assertEqual(rec_trx.calcular_total(), 20300.0)
        self.assertEqual(self.transaccion_dao.contar_detalles("TRX-001"), 2)

        # READ (listar todas)
        self.assertEqual(len(self.transaccion_dao.listar_todas()), 1)

        # 3. UPDATE (modificar y agregar detalle)
        trx.agregar_detalle("Seguro voluntario", 1500.0)
        self.assertTrue(self.transaccion_dao.actualizar(trx))
        rec_trx2 = self.transaccion_dao.obtener_por_id("TRX-001")
        self.assertEqual(len(rec_trx2.detalles), 3)
        self.assertEqual(rec_trx2.calcular_total(), 21800.0)

        # 4. DELETE (debe eliminar transacción y detalles en cascada)
        self.assertTrue(self.transaccion_dao.eliminar("TRX-001"))
        self.assertIsNone(self.transaccion_dao.obtener_por_id("TRX-001"))
        self.assertEqual(self.transaccion_dao.contar_detalles("TRX-001"), 0)

    # -------------------------------------------------------------------------
    # PRUEBAS DE SEGURIDAD E INTEGRIDAD REFERENCIAL
    # -------------------------------------------------------------------------
    def test_seguridad_clave_foranea_en_dao(self):
        # Intentar insertar una cuenta con un titular inexistente debe fallar
        cliente_inexistente = Cliente("11.111.111-1", "Fantasma", "SinGuardar", "000", "f@b.cl")
        cuenta_invalida = CuentaVista("CV-FAIL", cliente_inexistente, 1000)

        with self.assertRaises(sqlite3.IntegrityError):
            self.cuenta_dao.crear(cuenta_invalida)

    def test_transaccion_sin_detalles_rechazada(self):
        self.cliente_dao.crear(self.cliente1)
        self.cuenta_dao.crear(self.cuenta_vista)
        trx_vacia = Transaccion("TRX-VACIA", "2026-10-15", "Vacia", self.cuenta_vista)

        with self.assertRaises(ValueError):
            self.transaccion_dao.crear(trx_vacia)


if __name__ == "__main__":
    unittest.main()
