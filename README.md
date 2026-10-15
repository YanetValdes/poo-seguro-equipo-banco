# Sistema Bancario POO Seguro | Evaluación Sumativa N.º 3

**Integrantes:** Yanet Valeria Valdés Riquelme y Dayana del Carmen Reyes Osses  
**Carrera:** Técnico Analista Programador | **Institución:** INACAP Puente Alto  
**Asignatura:** Programación Orientada a Objeto Seguro  
**Tipo:** Prototipo académico. No es un sistema bancario de producción.

## 1. Requisitos

- Python **3.10 o superior**.
- No se requiere instalar bibliotecas externas: se utilizan módulos estándar (`sqlite3`, `urllib`, `json`, `argparse` y `unittest`).
- Internet para consultar **la UF real**. El programa se ejecuta y maneja el error si no hay conexión.

## 2. Cómo instalar y ejecutar (también para el docente)

1. Descargar este repositorio completo o descomprimir el archivo ZIP.
2. Abrir una terminal dentro de la carpeta que contiene `main.py`.
3. Ejecutar los comandos siguientes:

```bash
python main.py
python -m unittest discover -v
```

En Windows, si `python` no está disponible, usar `py main.py` y `py -m unittest discover -v`.

**`python main.py` demuestra por defecto los criterios de la Sumativa 3**: crea objetos del banco, valida RUT, aplica reglas de mora y saldo insuficiente, ejecuta tres tipos de `girar()` por polimorfismo, guarda en SQLite y recupera los datos después de reabrir una conexión, intenta consultar la UF real y muestra entradas aceptadas/rechazadas. Si la API no responde, la aplicación captura el error y sigue operando. No se presenta un dato simulado como real.

Otras opciones útiles:

```bash
python main.py --interactivo             # solicitar un monto por teclado
python main.py --sin-api                 # ejecutar sin intentar consultar Internet
python main.py --bd otra_demo.sqlite3    # escoger archivo SQLite
python main.py --help                    # ver opciones
```

### Verificación de persistencia entre ejecuciones

1. Ejecutar `python main.py --sin-api`.
2. Comprobar que aparece `[OK] Cuentas recuperadas después de reabrir la base`.
3. Ejecutar **otra vez** el mismo comando, sin eliminar `banco_demo.sqlite3`.
4. Comprobar que ahora aparece `[OK] Registro de ejecución anterior leído desde SQLite`.

Se reutilizan los mismos identificadores de demostración y se actualiza su saldo, **sin duplicar cuentas**. No se confunde la persistencia con las variables temporales del proceso Python.

## 3. Relación con cada criterio evaluado

| Criterio | Archivo y demostración verificable |
|---|---|
| 2.1.2 Integración del sistema | `model/`, `main.py`: tres tipos de cuenta con `girar()` polimórfico; validación RUT; transacción y detalles; mora y saldo insuficiente; costo de tasación de ejemplo de **2 UF** obtenido a partir de indicador externo. |
| 2.1.3 Persistencia | `servicios/persistencia.py`: SQLite, tablas, claves foráneas y recuperación al reabrir conexión; `main.py` sección 7 y pruebas de dos conexiones. |
| 3.1.2 Validación de entradas | `main.py`: `capturar_monto()` acepta positivos finitos y rechaza texto, 0, negativos, NaN e infinito; sección 9 y `--interactivo`. |
| 3.1.1 Consumo de API | `servicios/indicadores.py`: petición HTTPS a `https://mindicador.cl/api/uf`; sección 8 de `main.py`, por defecto. |
| 3.1.3 Errores de API | `ErrorIndicador`, timeout de 5 s, manejo de error HTTP/red, JSON inválido, respuesta vacía y cotización no finita; `test_sumativa3.py`. |
| 3.1.4 README | Este documento: instalación, comandos de ejecución, estructura, seguridad, decisiones técnicas y uso de IA. |

**Nota:** la correspondencia se basa en los seis criterios explicados por el profesor en su correo. El equipo debe compararla con la rúbrica oficial completa antes de dar el trabajo por finalizado.

## 4. Estructura del código

```text
main.py                         Ejecución integral y demostración
model/                          Clases Cliente, Cuenta, subtipos, Crédito, etc.
servicios/indicadores.py        UF real, cálculo de costo y control de errores
servicios/persistencia.py       Conexión y operaciones SQLite parametrizadas
test_reglas_banco.py             5 pruebas del modelo POO y reglas bancarias
test_sumativa3.py                13 pruebas adicionales de API, entradas y SQLite
README.md                       Instalación, ejecución, decisiones y evidencias
GUIA_DE_CORRECCION_Y_ENTREGA.md Pasos para revisar, probar y actualizar GitHub
```

## 5. Integración del caso bancario

- **POO:** `Cuenta` es la clase base; `CuentaAhorro`, `CuentaCorriente` y `CuentaVista` redefinen `girar()` para aplicar límites y comisiones distintas. `Empleado` tiene subclases `Ejecutivo` y `Cajero`.
- **Validación RUT:** `Cliente.rut` normaliza el texto, valida el dígito verificador módulo 11 y rechaza cambios inválidos conservando el estado previo.
- **Regla de mora:** la apertura de una cuenta rechaza a un cliente con `mora_vigente=True` mediante `ClienteConMoraException`.
- **Regla de saldo:** `girar()` rechaza fondos insuficientes mediante `SaldoInsuficienteException`, considerando las reglas del producto.
- **Composición:** `Transaccion` contiene `DetalleTransaccion`, y `Credito` genera y administra `CuotaCredito`.
- **Agregación:** las cuentas reciben una referencia a `Cliente` preexistente como titular.
- **Indicador externo:** el ejemplo de **tasación bancaria de 2 UF** cambia su valor en pesos en función de la UF consultada desde una API pública. Es un costo ilustrativo de la actividad, **no una tarifa bancaria real**. La tasa de interés del crédito es independiente de la UF.

## 6. Persistencia y seguridad

La aplicación crea automáticamente el archivo `banco_demo.sqlite3` en el directorio actual. Incluye las tablas `clientes`, `cuentas`, `transacciones` y `detalles`. Utiliza claves primarias y foráneas, consultas parametrizadas para reducir el riesgo de inyección SQL y transacciones que se revierten cuando una operación falla.

La escritura de cliente, cuentas y detalles proviene de **objetos de dominio en memoria**; el programa cierra la conexión y vuelve a abrirla para comprobar que los registros están en disco. El archivo de base de datos de demostración se excluye de Git con `.gitignore`.

**Limitaciones deliberadas:** no existe autenticación, autorización por rol, cifrado en reposo, bitácora de auditoría ni precisión monetaria de producción (SQLite `REAL`/`float`), por lo que **no debe utilizarse con datos financieros o personales reales**. Los datos de ejemplo son ficticios.

## 7. Manejo de API y validaciones

- Consulta HTTPS a `https://mindicador.cl/api/uf` con tiempo máximo de espera de **5 segundos**.
- Comprueba estructura JSON, serie no vacía, valor numérico, positivo y finito.
- Maneja excepciones de red, HTTP, tiempo de espera y respuesta inválida bajo `ErrorIndicador`.
- Si el servicio está caído, muestra `[AVISO]` y continúa. **No inventa una UF**.
- Las pruebas automáticas **simulan explícitamente respuestas HTTP** para verificar tanto éxito como errores aun sin Internet; el valor simulado de prueba no representa la cotización real.
- `capturar_monto()` valida `float`, rechaza valores no finitos y montos menores o iguales a 0. En la sección 9 se ven tanto ejemplos aceptados como rechazados.

## 8. Uso de inteligencia artificial y decisiones técnicas

Se utilizó ChatGPT como apoyo de revisión de la retroalimentación, propuestas de arquitectura, elaboración de pruebas, explicación y documentación. Las integrantes deben revisar el código, comprender las decisiones, ejecutarlo y confirmar que corresponde a la rúbrica antes de realizar su entrega. El uso de IA no reemplaza la responsabilidad académica del equipo.

| Decisión | Motivo técnico | Resultado |
|---|---|---|
| Adoptar `sqlite3` | Incluido en la biblioteca estándar; guarda registros entre ejecuciones sin un servidor adicional | Persistencia local reproducible |
| Adoptar `urllib.request` | Evita dependencias para solicitar UF por HTTPS | Integración externa más sencilla de instalar |
| Rechazar valores inventados ante caída | Usar una cotización simulada como real sería un resultado engañoso | `ErrorIndicador` y aviso claro |
| Parametrizar SQL | Evita concatenar entradas directamente en las consultas | Reduce riesgo de inyección SQL |
| Escribir dentro de `with conexion` | Permite confirmar o revertir operaciones como grupo | Comportamiento transaccional |
| Consultar UF por defecto | Hace visible el requisito de API al seguir solo el README | Ejecución docente más verificable |
| Probar API con dobles de prueba | El acceso externo puede fallar o variar con el tiempo | Pruebas repetibles sin Internet |
| Conservar el modelo Sumativa 2 | Evita reescribir clases que ya tenían comportamiento POO demostrado | Se agregan servicios sin perder reglas existentes |

## 9. Pruebas que debe ejecutar el equipo

```bash
python -m unittest discover -v
```

Se esperan **18 pruebas**: cinco en `test_reglas_banco.py` y trece en `test_sumativa3.py`. Deben terminar en `OK`. Se cubren RUT, mora, saldo insuficiente, agregación, validación de entrada, respuesta válida y fallida de API, timeout, HTTP, datos inválidos, persistencia entre conexiones, ausencia de duplicados, claves foráneas y SQL parametrizado.

## 10. Publicación y alcance de la evaluación

Esta versión debe copiarse al repositorio **[poo-seguro-equipo-banco](https://github.com/YanetValdes/poo-seguro-equipo-banco)** mediante un **nuevo commit**, incluyendo `servicios/` y `test_sumativa3.py`. El ZIP adjunto por sí solo no modifica GitHub. El equipo debe pedir autorización al profesor si desea que se considere una entrega posterior al plazo del **13 de octubre de 2026 a las 23:59**; un commit posterior no cambia automáticamente la evaluación original.

Para instrucciones de carga y evidencias, leer [`GUIA_DE_CORRECCION_Y_ENTREGA.md`](GUIA_DE_CORRECCION_Y_ENTREGA.md).
