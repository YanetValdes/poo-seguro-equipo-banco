"""Pruebas automatizadas de Sumativa 3, sin depender de Internet."""
import json
import math
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
import requests

from main import capturar_monto
from servicios.indicadores import obtener_uf, precio_en_pesos, ErrorIndicador, API_UF
from servicios.persistencia import (conectar, guardar_cliente, guardar_cuenta,
                                    listar_cuentas, obtener_cuenta, contar_detalles,
                                    guardar_transaccion)
from model.cliente import Cliente
from model.cuenta_vista import CuentaVista


class MockResponse:
    """Doble de prueba para simular respuestas de requests sin acceder a Internet."""

    def __init__(self, json_data=None, text="", status_code=200):
        self._json_data = json_data
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(
                f"HTTP Error {self.status_code}",
                response=self
            )

    def json(self):
        if self._json_data is not None:
            return self._json_data
        return json.loads(self.text)


def fake_api(datos):
    return lambda url, timeout, headers: MockResponse(json_data=datos)


class Sumativa3Test(unittest.TestCase):
    def test_api_uf_respuesta_valida_simulada(self):
        def mock_req(url, timeout, headers):
            self.assertEqual(timeout, 5)
            self.assertEqual(url, API_UF)
            return MockResponse(json_data={"serie": [{"valor": 39000}]})
        self.assertEqual(obtener_uf(requester=mock_req), 39000)
        self.assertEqual(precio_en_pesos(2, 39000), 78000)

    def test_api_uf_caida_red(self):
        def mock_req(url, timeout, headers):
            raise requests.exceptions.ConnectionError("sin Internet")
        with self.assertRaises(ErrorIndicador):
            obtener_uf(requester=mock_req)

    def test_api_uf_timeout(self):
        def mock_req(url, timeout, headers):
            raise requests.exceptions.Timeout("tiempo excedido")
        with self.assertRaisesRegex(ErrorIndicador, "tiempo"):
            obtener_uf(requester=mock_req)

    def test_api_uf_http_error(self):
        def mock_req(url, timeout, headers):
            return MockResponse(status_code=503)
        with self.assertRaises(ErrorIndicador):
            obtener_uf(requester=mock_req)

    def test_api_uf_json_malformado(self):
        def mock_req(url, timeout, headers):
            return MockResponse(text="{mal json")
        with self.assertRaises(ErrorIndicador):
            obtener_uf(requester=mock_req)

    def test_api_uf_formato_inesperado(self):
        for datos in ([], {}, {"serie": []}, {"serie": [None]},
                      {"serie": [{"valor": "39000"}]},
                      {"serie": [{"valor": -8}]},
                      {"serie": [{"valor": True}]}):
            with self.subTest(datos=datos), self.assertRaises(ErrorIndicador):
                obtener_uf(requester=fake_api(datos))

    def test_api_uf_infinito_y_nan(self):
        for valor in (math.inf, -math.inf, math.nan):
            with self.subTest(valor=valor), self.assertRaises(ErrorIndicador):
                obtener_uf(requester=fake_api({"serie": [{"valor": valor}]}))

    def test_api_costo_en_uf_valida_argumentos(self):
        for valor in (0, -3, math.nan, math.inf, "2", True):
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                precio_en_pesos(valor, 39000)
        self.assertEqual(precio_en_pesos(2, 39000), 78000)

    def test_entrada_interactiva(self):
        self.assertEqual(capturar_monto(lambda _: "1500"), 1500)
        self.assertEqual(capturar_monto(lambda _: "  10.5 "), 10.5)
        for valor in ("abc", "-5", "0", "NaN", "inf", "-inf", ""):
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                capturar_monto(lambda _: valor)

    def test_persistencia_en_dos_conexiones_reales(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "banco_prueba.sqlite3"
            cliente = Cliente("18.765.432-7", "Ana", "Prueba", "123456", "ana@example.cl")
            cuenta = CuentaVista("CV-TEST", cliente, 9000)
            with closing(conectar(ruta)) as con:
                with con:
                    guardar_cliente(con, cliente)
                    guardar_cuenta(con, cuenta)
                    guardar_transaccion(con, "T1", "CV-TEST", "2026-10-15", "retiro",
                                        [("cargo", 100), ("tarifa", 50)])
            self.assertTrue(ruta.exists())
            with closing(conectar(ruta)) as con:
                self.assertEqual(obtener_cuenta(con, "CV-TEST")[3], 9000)
                self.assertEqual(contar_detalles(con, "T1"), 2)
                self.assertEqual(len(listar_cuentas(con)), 1)

    def test_sqlite_no_duplica_y_actualiza(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "test.sqlite3"
            cliente = Cliente("18.765.432-7", "Ana", "Prueba", "123456", "ana@example.cl")
            cuenta = CuentaVista("CV-TEST", cliente, 9000)
            with closing(conectar(ruta)) as con:
                with con:
                    guardar_cliente(con, cliente)
                    guardar_cuenta(con, cuenta)
                    guardar_transaccion(con, "T1", "CV-TEST", "2026-10-15", "retiro",
                                        [("cargo", 100)])
            cuenta.depositar(100)
            with closing(conectar(ruta)) as con:
                with con:
                    guardar_cliente(con, cliente)
                    guardar_cuenta(con, cuenta)
                    guardar_transaccion(con, "T1", "CV-TEST", "2026-10-15", "retiro",
                                        [("cargo", 100), ("tarifa", 50)])
                self.assertEqual(len(listar_cuentas(con)), 1)
                self.assertEqual(obtener_cuenta(con, "CV-TEST")[3], 9100)
                self.assertEqual(contar_detalles(con, "T1"), 2)

    def test_sqlite_claves_foraneas_y_rollback(self):
        with tempfile.TemporaryDirectory() as carpeta:
            with closing(conectar(Path(carpeta) / "test.sqlite3")) as con:
                with self.assertRaises(sqlite3.IntegrityError):
                    with con:
                        con.execute("INSERT INTO cuentas VALUES ('SIN-CLIENTE','X','Cuenta',500)")
                self.assertEqual(listar_cuentas(con), [])

    def test_sqlite_consultas_parametrizadas(self):
        with tempfile.TemporaryDirectory() as carpeta:
            with closing(conectar(Path(carpeta) / "test.sqlite3")) as con:
                self.assertIsNone(obtener_cuenta(con, "CV-123' OR 1=1 --"))
                self.assertEqual(con.execute("SELECT COUNT(*) FROM clientes").fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()
