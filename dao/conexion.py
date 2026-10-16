"""
Módulo de conexión y gestión del esquema SQLite para la capa DAO.
Asegura la activación de claves foráneas y la preparación de las tablas.
"""
import sqlite3

ESQUEMA = """
CREATE TABLE IF NOT EXISTS clientes (
    rut TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    telefono TEXT NOT NULL,
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
    transaccion_id TEXT NOT NULL REFERENCES transacciones(id) ON DELETE CASCADE,
    posicion INTEGER NOT NULL,
    concepto TEXT NOT NULL,
    monto REAL NOT NULL CHECK(monto >= 0),
    PRIMARY KEY (transaccion_id, posicion)
);
"""


def conectar_db(ruta):
    """
    Abre una conexión SQLite hacia la ruta indicada.
    Habilita claves foráneas y ejecuta el esquema de base de datos.
    """
    con = sqlite3.connect(str(ruta))
    try:
        con.execute("PRAGMA foreign_keys = ON")
        con.executescript(ESQUEMA)
        columnas = [fila[1] for fila in con.execute("PRAGMA table_info(clientes)").fetchall()]
        if "telefono" not in columnas and "rut" in columnas:
            con.execute("ALTER TABLE clientes ADD COLUMN telefono TEXT NOT NULL DEFAULT ''")
    except Exception:
        con.close()
        raise
    return con
