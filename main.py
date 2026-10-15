"""
=============================================================================
PROGRAMA PRINCIPAL - EVALUACIÓN SUMATIVA N°3
Asignatura: Programación Orientada a Objeto Seguro
Sistema Bancario - Demostración de Clases, Herencia, Polimorfismo y Excepciones
=============================================================================
"""

import sys
import argparse
import sqlite3
from contextlib import closing
from servicios.indicadores import API_UF, obtener_uf, precio_en_pesos, ErrorIndicador
from servicios.persistencia import (
    conectar, guardar_cliente, guardar_cuenta, listar_cuentas, guardar_transaccion,
    obtener_cuenta, contar_detalles,
)

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
from model.cliente_con_mora_exception import ClienteConMoraException


def separador(titulo: str):
    """Función auxiliar para imprimir encabezados limpios en consola."""
    print("\n" + "=" * 75)
    print(f"  {titulo.upper()}")
    print("=" * 75)


def capturar_monto(entrada=input):
    """Validación de entrada de usuario para consulta demostrativa."""
    texto = entrada("Ingrese un monto positivo en pesos: ").strip()
    try:
        monto = float(texto)
    except ValueError as exc:
        raise ValueError("Debe ingresar un número válido.") from exc
    import math
    if not math.isfinite(monto) or monto <= 0:
        raise ValueError("El monto debe ser positivo y finito.")
    return monto


def main(interactivo=False, base_datos="banco_demo.sqlite3", consultar_api=True):
    print(">>> INICIANDO SISTEMA BANCARIO POO SEGURO <<<\n")

    # -------------------------------------------------------------------------
    # 1. CREACIÓN DE CLIENTE Y EMPLEADOS (EJECUTIVO Y CAJERO)
    # -------------------------------------------------------------------------
    separador("1. Creación de Entidades Principales (Cliente, Ejecutivo, Cajero)")

    cliente1 = Cliente(
        rut="18.765.432-7",
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

    # Evidencia: setter de RUT detecta un dígito verificador incorrecto.
    separador("Validación de dato: RUT chileno")
    try:
        cliente1.rut = "18.765.432-1"  # Dígito incorrecto, el correcto es 7.
        print("[ERROR] Un RUT inválido fue aceptado.")
    except ValueError as error:
        print(f"[CAPTURA EXITOSA] ValueError por RUT inválido: {error}")
        print(f"[OK] El RUT anterior se conserva: {cliente1.rut}")

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

    # Regla exigida por la ficha: cliente con mora vigente no puede abrir cuenta.
    separador("Regla del negocio: prohibición de apertura con mora vigente")
    cliente1.mora_vigente = True
    try:
        CuentaVista(numero_cuenta="CV-RECHAZADA", titular=cliente1, saldo_inicial=0,
                    costo_fijo_giro=300.0, costo_mantencion_mensual=1000.0)
        print("[ERROR] Se permitió abrir una cuenta con mora vigente.")
    except ClienteConMoraException as error:
        print(f"[CAPTURA EXITOSA] ClienteConMoraException: {error}")
    finally:
        cliente1.mora_vigente = False
        print("[OK] Estado de mora restablecido para continuar la demostración.")

    # Evidencia de agregación: la cuenta referencia un objeto Cliente ya creado.
    separador("Agregación Cliente-Cuenta")
    print(f"[OK] Cuenta y cliente comparten la misma referencia: {cuenta_ahorro.titular is cliente1}")

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
    # 7. PERSISTENCIA REAL CON SQLITE Y RELECTURA DE DISCO
    # -------------------------------------------------------------------------
    separador("7. Persistencia SQLite: escritura y recuperación")
    try:
        with closing(conectar(base_datos)) as conexion:
            anterior = obtener_cuenta(conexion, cuenta_corriente.numero_cuenta)
            if anterior is None:
                print("[INFO] No había registro previo: se inicializa la base de datos.")
            else:
                print(f"[OK] Registro de ejecución anterior leído desde SQLite: {anterior}")
            with conexion:  # commit de todas las escrituras; rollback si algo falla
                guardar_cliente(conexion, cliente1)
                for cuenta in cuentas:
                    guardar_cuenta(conexion, cuenta)
                guardar_transaccion(
                    conexion, transaccion.id_transaccion, transaccion.cuenta.numero_cuenta,
                    transaccion.fecha, transaccion.tipo,
                    [(detalle.concepto, detalle.monto) for detalle in transaccion.detalles],
                )
        # Cerramos y ABRIMOS OTRA CONEXIÓN para evidenciar persistencia en disco.
        with closing(conectar(base_datos)) as conexion:
            print("[OK] Cuentas recuperadas después de reabrir la base:", listar_cuentas(conexion))
            print("[OK] Líneas de detalle recuperadas:", contar_detalles(conexion, "TRX-885412"))
    except sqlite3.Error as error:
        print(f"[ERROR] Fallo de la base de datos: {error}")
        raise SystemExit(1) from error

    # -------------------------------------------------------------------------
    # 8. CONSUMO REAL DE API UF Y MANEJO DE ERRORES
    # -------------------------------------------------------------------------
    separador("8. API externa: costo de tasación calculado en UF")
    if consultar_api:
        try:
            cotizacion = obtener_uf(timeout=5)
            print(f"[OK] UF consultada desde {API_UF}: ${cotizacion:,.2f} CLP")
            print(f"[OK] Ejemplo académico, tasación de 2 UF: ${precio_en_pesos(2, cotizacion):,.2f} CLP")
        except ErrorIndicador as error:
            print(f"[AVISO] No se pudo consultar la API: {error}")
            print("[OK] La aplicación continúa sin inventar el valor de la UF.")
    else:
        print("[INFO] Se omitió la consulta online con --sin-api.")

    # -------------------------------------------------------------------------
    # 9. VALIDACIÓN OBSERVABLE DE ENTRADAS, INCLUSO SIN TECLEAR
    # -------------------------------------------------------------------------
    separador("9. Validación de entradas de usuario")
    for texto in ("25000", "abc", "-100", "0", "NaN", "inf"):
        try:
            monto = capturar_monto(lambda _: texto)
            print(f"[OK] Entrada {texto!r}: ${monto:,.2f}")
        except ValueError as error:
            print(f"[RECHAZADO] Entrada {texto!r}: {error}")
    if interactivo:
        print("\n[INTERACTIVO] Ahora ingresa tu propio monto:")
        try:
            print(f"[OK] Entrada aceptada: ${capturar_monto():,.2f}")
        except (ValueError, EOFError) as error:
            print(f"[CAPTURA] Entrada rechazada: {error}")

    # -------------------------------------------------------------------------
    # 10. CIERRE EXITOSO
    # -------------------------------------------------------------------------
    separador("10. Verificación Final")
    print("[OK] Todas las clases fueron instanciadas e integradas correctamente.")
    print("[OK] Herencia con super().__init__() aplicada.")
    print("[OK] Polimorfismo demostrado con 3 resultados diferentes para el mismo método.")
    print("[OK] SaldoInsuficienteException, ClienteConMoraException y CuentaBloqueadaException capturadas.")
    print("[OK] RUT inválido rechazado y agregación Cliente-Cuenta demostrada.")
    print("[OK] Transacción con líneas de detalle procesada exitosamente.")
    print("[OK] Persistencia, validación de entradas y gestión de API implementadas.")
    print("\n>>> EJECUCIÓN DEL SISTEMA FINALIZADA CON ÉXITO <<<\n")


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="Sistema bancario: demostración Sumativa 3")
    parser.add_argument("--interactivo",action="store_true",help="Solicita y valida un monto por teclado")
    parser.add_argument("--sin-api", action="store_true", help="Omite consulta UF al ejecutar sin Internet")
    parser.add_argument("--api", action="store_true", help="Compatibilidad: consulta la UF (ya se hace por defecto)")
    parser.add_argument("--bd",default="banco_demo.sqlite3",help="Ruta a base SQLite")
    args=parser.parse_args()
    main(interactivo=args.interactivo, base_datos=args.bd, consultar_api=not args.sin_api)
