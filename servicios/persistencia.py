"""Persistencia de demostración mediante SQLite, con claves foráneas y SQL parametrizado.

Cada función de escritura participa en una transacción administrada por el llamador:
    with conexion:
        guardar_cliente(conexion, cliente)
        guardar_cuenta(conexion, cuenta)

SQLite almacena REAL (float) solo por simplicidad académica, no para banca real.
"""
import sqlite3

ESQUEMA = """
CREATE TABLE IF NOT EXISTS clientes (
    rut TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    email TEXT NOT NULL,
    mora_vigente INTEGER NOT NULL CHECK(mora_vigente IN (0,1))
);
CREATE TABLE IF NOT EXISTS cuentas (
    numero TEXT PRIMARY KEY,
    rut_cliente TEXT NOT NULL REFERENCES clientes(rut),
    tipo TEXT NOT NULL,
    saldo REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS transacciones (
    id TEXT PRIMARY KEY,
    numero_cuenta TEXT NOT NULL REFERENCES cuentas(numero),
    fecha TEXT NOT NULL,
    tipo TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS detalles (
    transaccion_id TEXT NOT NULL REFERENCES transacciones(id),
    posicion INTEGER NOT NULL,
    concepto TEXT NOT NULL,
    monto REAL NOT NULL CHECK(monto >= 0),
    PRIMARY KEY (transaccion_id, posicion)
);
"""


def conectar(ruta):
    """Abre una conexión SQLite y prepara tablas si aún no existen."""
    con = sqlite3.connect(str(ruta))
    try:
        con.execute("PRAGMA foreign_keys = ON")
        con.executescript(ESQUEMA)
    except Exception:
        con.close()
        raise
    return con


def guardar_cliente(con, cliente):
    con.execute(
        """INSERT INTO clientes (rut,nombre,apellido,email,mora_vigente)
           VALUES (?,?,?,?,?)
           ON CONFLICT(rut) DO UPDATE SET
               nombre=excluded.nombre, apellido=excluded.apellido,
               email=excluded.email, mora_vigente=excluded.mora_vigente""",
        (cliente.rut, cliente.nombre, cliente.apellido, cliente.email,
         int(cliente.mora_vigente)),
    )


def guardar_cuenta(con, cuenta):
    con.execute(
        """INSERT INTO cuentas (numero,rut_cliente,tipo,saldo) VALUES (?,?,?,?)
           ON CONFLICT(numero) DO UPDATE SET
               rut_cliente=excluded.rut_cliente, tipo=excluded.tipo,
               saldo=excluded.saldo""",
        (cuenta.numero_cuenta, cuenta.titular.rut, cuenta.tipo_cuenta(), cuenta.saldo),
    )


def guardar_transaccion(con, transaccion_id, numero_cuenta, fecha, tipo, detalles):
    """Guarda cabecera y líneas dentro de la transacción de su llamador."""
    lineas = list(detalles)
    if not lineas:
        raise ValueError("Una transacción debe incluir por lo menos un detalle.")
    con.execute(
        """INSERT INTO transacciones (id,numero_cuenta,fecha,tipo) VALUES (?,?,?,?)
           ON CONFLICT(id) DO UPDATE SET
               numero_cuenta=excluded.numero_cuenta,
               fecha=excluded.fecha, tipo=excluded.tipo""",
        (transaccion_id, numero_cuenta, fecha, tipo),
    )
    con.execute("DELETE FROM detalles WHERE transaccion_id = ?", (transaccion_id,))
    con.executemany(
        "INSERT INTO detalles (transaccion_id,posicion,concepto,monto) VALUES (?,?,?,?)",
        [(transaccion_id, i, concepto, monto)
         for i, (concepto, monto) in enumerate(lineas, 1)],
    )


def listar_cuentas(con):
    """Recupera cuentas desde el disco, no desde las variables Python."""
    return con.execute(
        "SELECT numero,rut_cliente,tipo,saldo FROM cuentas ORDER BY numero"
    ).fetchall()


def obtener_cuenta(con, numero):
    return con.execute(
        "SELECT numero,rut_cliente,tipo,saldo FROM cuentas WHERE numero = ?", (numero,)
    ).fetchone()


def contar_detalles(con, transaccion_id):
    return con.execute(
        "SELECT COUNT(*) FROM detalles WHERE transaccion_id = ?", (transaccion_id,)
    ).fetchone()[0]
