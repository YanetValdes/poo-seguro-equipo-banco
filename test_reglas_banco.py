import unittest
from model.cliente import Cliente
from model.cuenta_vista import CuentaVista
from model.cliente_con_mora_exception import ClienteConMoraException
from model.saldo_insuficiente_exception import SaldoInsuficienteException

class ReglasBancoTest(unittest.TestCase):
    def setUp(self):
        self.cliente = Cliente('18.765.432-7', 'Ana', 'Prueba', '999999999', 'ana@example.cl')

    def test_rut_invalido_y_estado_conservado(self):
        with self.assertRaises(ValueError):
            self.cliente.rut = '18.765.432-1'
        self.assertEqual(self.cliente.rut, '18765432-7')

    def test_mora_impide_abrir_cuenta(self):
        self.cliente.mora_vigente = True
        with self.assertRaises(ClienteConMoraException):
            CuentaVista('CV-001', self.cliente, 5000)

    def test_saldo_insuficiente(self):
        cuenta = CuentaVista('CV-002', self.cliente, 1000)
        with self.assertRaises(SaldoInsuficienteException):
            cuenta.girar(50000)

    def test_agregacion(self):
        cuenta = CuentaVista('CV-003', self.cliente, 1000)
        self.assertIs(cuenta.titular, self.cliente)

    def test_mora_setter_solo_booleanos(self):
        with self.assertRaises(TypeError):
            self.cliente.mora_vigente = 'sí'

if __name__ == '__main__':
    unittest.main()
