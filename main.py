"""
=============================================================================
PROGRAMA PRINCIPAL - EVALUACIÓN SUMATIVA N°2
Asignatura: Programación Orientada a Objeto Seguro
Sistema Bancario - Demostración de Clases, Herencia, Polimorfismo y Excepciones
=============================================================================
"""

import sys

# Asegurar codificación UTF-8 en consolas Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from model.cliente import Cliente
from model.cuenta import Cuenta
from model.cuenta_ahorro import CuentaAhorro
from model.cuenta_corriente import CuentaCorriente
from model.cuenta_vista import CuentaVista
from model.cuota_credito import CuotaCredito
from model.credito import Credito
from model.empleado import Empleado
from model.ejecutivo import Ejecutivo
from model.cajero import Cajero
from model.transaccion import Transaccion
from model.detalle_transaccion import DetalleTransaccion
from model.saldo_insuficiente_exception import SaldoInsuficienteException
from model.cuenta_bloqueada_exception import CuentaBloqueadaException


def separador(titulo: str):
    """Función auxiliar para imprimir encabezados limpios en consola."""
    print("\n" + "=" * 75)
    print(f"  {titulo.upper()}")
    print("=" * 75)


def main():
    print(">>> INICIANDO SISTEMA BANCARIO POO SEGURO <<<\n")

    # -------------------------------------------------------------------------
    # 1. CREACIÓN DE CLIENTE Y EMPLEADOS (EJECUTIVO Y CAJERO)
    # -------------------------------------------------------------------------
    separador("1. Creación de Entidades Principales (Cliente, Ejecutivo, Cajero)")

    cliente1 = Cliente(
        rut="18.765.432-1",
        nombre="Matías",
        apellido="Tapia",
        telefono="+56987654321",
        email="matias.tapia@banco.cl"
    )
    print(f"[*] {cliente1}")

    ejecutivo = Ejecutivo(
        rut="15.234.567-8",
        nombre="Camila",
        apellido="Morales",
        sueldo_base=950000.0,
        comision_por_credito=40000.0
    )
    print(f"[*] {ejecutivo}")

    cajero = Cajero(
        rut="16.987.654-3",
        nombre="Roberto",
        apellido="González",
        sueldo_base=680000.0,
        numero_caja=2,
        bono_responsabilidad_caja=75000.0
    )
    print(f"[*] {cajero}")

    # -------------------------------------------------------------------------
    # 2. CREACIÓN DE SUBTIPOS DE CUENTA (HERENCIA Y SUPER().__INIT__)
    # -------------------------------------------------------------------------
    separador("2. Cuentas Bancarias (CuentaAhorro, CuentaCorriente, CuentaVista)")

    cuenta_ahorro = CuentaAhorro(
        numero_cuenta="AH-1001",
        titular=cliente1,
        saldo_inicial=80000.0,
        tasa_interes_anual=0.04,
        limite_giros_gratis=1,
        costo_giro_adicional=1500.0
    )

    cuenta_corriente = CuentaCorriente(
        numero_cuenta="CC-2002",
        titular=cliente1,
        saldo_inicial=20000.0,
        linea_sobregiro=100000.0,
        costo_mantencion_base=5000.0
    )

    cuenta_vista = CuentaVista(
        numero_cuenta="CV-3003",
        titular=cliente1,
        saldo_inicial=50000.0,
        costo_fijo_giro=300.0,
        costo_mantencion_mensual=1000.0
    )

    cuentas: list[Cuenta] = [cuenta_ahorro, cuenta_corriente, cuenta_vista]
    for c in cuentas:
        print(f" -> {c}")

    # -------------------------------------------------------------------------
    # 3. DEMOSTRACIÓN DE POLIMORFISMO
    # (Los tres subtipos sobrescriben y ejecutan el mismo método con resultados diferentes)
    # -------------------------------------------------------------------------
    separador("3. Demostración de Polimorfismo: Mismo método 'girar()'")
    print("Ejecutando c.girar(35000) en cada subtipo de cuenta:")

    monto_a_girar = 35000.0
    for cuenta in cuentas:
        print(f"\n[Tipo de Cuenta]: {cuenta.tipo_cuenta()} (Saldo previo: ${cuenta.saldo:,.0f})")
        # Invocación polimórfica del método sobrescrito
        mensaje_resultado = cuenta.girar(monto_a_girar)
        print(f"  Resultado : {mensaje_resultado}")

    print("\n" + "-" * 75)
    print("Demostración complementaria de polimorfismo con 'calcular_costo_mantencion()':")
    for cuenta in cuentas:
        costo = cuenta.calcular_costo_mantencion()
        print(f" -> {cuenta.tipo_cuenta():<20} | Costo de Mantención Mensual: ${costo:,.0f}")

    # -------------------------------------------------------------------------
    # 4. MANEJO DE EXCEPCIONES PROPIAS CON TRY / EXCEPT
    # -------------------------------------------------------------------------
    separador("4. Manejo Seguro de Excepciones Propias (SaldoInsuficiente y CuentaBloqueada)")

    # 4.1 Provocar SaldoInsuficienteException
    print("[CASO 1] Intento de giro que excede los fondos permitidos...")
    try:
        # La cuenta vista tiene menos de $15,000 tras el giro anterior
        monto_excesivo = 500000.0
        print(f"Intentando girar ${monto_excesivo:,.0f} desde Cuenta Vista {cuenta_vista.numero_cuenta}...")
        cuenta_vista.girar(monto_excesivo)
        print("ERROR: La excepción no fue lanzada.")
    except SaldoInsuficienteException as e:
        print(f"[CAPTURA EXITOSA] SaldoInsuficienteException capturada:")
        print(f"  Mensaje de excepción: {e}")
        print("  >> El sistema manejó el error de forma segura y continúa ejecutándose.")

    # 4.2 Provocar CuentaBloqueadaException
    print("\n[CASO 2] Intento de giro sobre una cuenta bloqueada...")
    try:
        print(f"Bloqueando Cuenta de Ahorro N° {cuenta_ahorro.numero_cuenta}...")
        cuenta_ahorro.bloquear()
        print(f"Estado de la cuenta: bloqueada={cuenta_ahorro.bloqueada}")

        print("Intentando realizar un giro de $5,000 en la cuenta bloqueada...")
        cuenta_ahorro.girar(5000.0)
        print("ERROR: La excepción no fue lanzada.")
    except CuentaBloqueadaException as e:
        print(f"[CAPTURA EXITOSA] CuentaBloqueadaException capturada:")
        print(f"  Mensaje de excepción: {e}")
        print("  >> El sistema protegió la cuenta bloqueada y continúa ejecutándose.")

    # Desbloquear para restablecer la cuenta
    cuenta_ahorro.desbloquear()
    print(f"\n[INFO] Cuenta de Ahorro desbloqueada nuevamente (bloqueada={cuenta_ahorro.bloqueada}).")

    # -------------------------------------------------------------------------
    # 5. GESTIÓN DE CRÉDITO Y CUOTAS (CREDITO, CUOTACREDITO Y EJECUTIVO)
    # -------------------------------------------------------------------------
    separador("5. Crédito Bancario, Generación de Cuotas y Aprobación")

    credito1 = Credito(
        codigo="CRED-2026-001",
        cliente=cliente1,
        monto_solicitado=600000.0,
        tasa_interes=0.06,  # 6% de interés total
        plazo_meses=3       # 3 cuotas mensuales
    )
    print(f"[*] {credito1}")

    # El ejecutivo evalúa y aprueba el crédito
    resultado_aprobacion = ejecutivo.aprobar_credito(credito1)
    print(f"[*] {resultado_aprobacion}")
    print(f"[*] Sueldo actualizado del Ejecutivo ({ejecutivo.nombre_completo}): ${ejecutivo.calcular_sueldo_total():,.0f}")

    print("\nDetalle de cuotas generadas para el crédito:")
    for cuota in credito1.cuotas:
        print(f"  -> {cuota}")

    print("\nSimulando el pago de la Cuota N° 1...")
    credito1.pagar_cuota(1)
    for cuota in credito1.cuotas:
        print(f"  -> {cuota}")
    print(f"Saldo pendiente total del crédito: ${credito1.saldo_pendiente():,.0f}")

    # -------------------------------------------------------------------------
    # 6. TRANSACCIÓN CON LÍNEAS DE DETALLE
    # -------------------------------------------------------------------------
    separador("6. Transacción Bancaria con Múltiples Líneas de Detalle")

    transaccion = Transaccion(
        id_transaccion="TRX-885412",
        fecha="2026-10-04 14:30:00",
        tipo="Giro en Mostrador con Cobros Adicionales",
        cuenta=cuenta_corriente
    )

    # Agregar líneas de detalle a la transacción
    transaccion.agregar_detalle("Retiro de efectivo en caja", 25000.0)
    transaccion.agregar_detalle("Comisión por uso de mostrador", 1200.0)
    transaccion.agregar_detalle("Seguro voluntario de protección de giro", 2500.0)
    transaccion.agregar_detalle("Impuesto de timbres y estampillas", 350.0)

    # Mostrar comprobante formal
    print(transaccion.generar_comprobante())

    # -------------------------------------------------------------------------
    # 7. CIERRE EXITOSO
    # -------------------------------------------------------------------------
    separador("7. Verificación Final")
    print("[OK] Todas las clases fueron instanciadas e integradas correctamente.")
    print("[OK] Herencia con super().__init__() aplicada.")
    print("[OK] Polimorfismo demostrado con 3 resultados diferentes para el mismo método.")
    print("[OK] SaldoInsuficienteException y CuentaBloqueadaException provocadas y capturadas.")
    print("[OK] Transacción con líneas de detalle procesada exitosamente.")
    print("\n>>> EJECUCIÓN DEL SISTEMA FINALIZADA CON ÉXITO <<<\n")


if __name__ == "__main__":
    main()
