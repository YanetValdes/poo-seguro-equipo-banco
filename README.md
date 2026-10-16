# Sistema Bancario POO Seguro | Evaluación Sumativa N.º 3

**Carrera:** Técnico Analista Programador | **Institución:** INACAP Puente Alto  
**Asignatura:** Programación Orientada a Objeto Seguro  
**Tipo de Entrega:** Proyecto de Demostración Académica POO Seguro  

---

## Apartado 1: Integrantes y Negocio Bancario

### 1.1 Integrantes del Proyecto
* **Yanet Valeria Valdés Riquelme**
* **Dayana del Carmen Reyes Osses**

### 1.2 Descripción del Negocio Bancario
El sistema modela las operaciones centrales de una institución financiera chilena bajo estándares de **Programación Orientada a Objeto Seguro (POO Seguro)**, organizando el dominio bancario en entidades de clientes, personal bancario, productos de ahorro y crédito, transacciones operativas, capa de persistencia DAO en SQLite y servicios de cotización financiera externa.

### 1.3 Cumplimiento de los Cinco Requisitos Centrales
1. **Tres subtipos de cuenta con polimorfismo:**
   * Clase base `Cuenta` y tres subtipos concretos: `CuentaAhorro`, `CuentaCorriente` y `CuentaVista`.
   * Demostración polimórfica del método `girar(monto)`:
     * `CuentaAhorro`: aplica límite de giros gratuitos anuales y cobra comisión adicional por giros posteriores.
     * `CuentaCorriente`: permite operar con saldo disponible propio más línea de sobregiro autorizada, generando saldo contable negativo hasta el límite pactado.
     * `CuentaVista`: cobra una tarifa fija de operación por cada retiro ($300) y rechaza cualquier saldo negativo.
   * Demostración complementaria con `calcular_costo_mantencion()`: $0 en ahorro, costo base más recargo por sobregiro en cuenta corriente, y tarifa plana en cuenta vista.
2. **Validación estricta de datos:**
   * **RUT Chileno:** Validación matemática formal mediante algoritmo Módulo 11 en `Cliente.rut`, verificación del dígito verificador (0-9 o K) y preservación del estado previo ante intentos de asignación inválida.
   * **Montos monetarios seguros:** Verificación de números estrictamente positivos, finitos (`math.isfinite()`) y descarte explícito de booleanos (`bool`), previniendo corrupción de saldos mediante `NaN` o `inf`.
   * **Atributos personales:** Nombres no vacíos, formato básico de correo electrónico y teléfono de contacto.
3. **Transacciones con líneas de detalle (Composición):**
   * Clase `Transaccion` compuesta por una colección de objetos `DetalleTransaccion`.
   * Cada línea registra número correlativo, concepto de cobro/abono y monto.
   * Cálculo acumulado automático del total de la transacción y generación de comprobante formal formateado.
4. **Dos reglas del negocio que impiden operaciones:**
   * **Regla 1 (Apertura de cuenta):** Un cliente con mora vigente (`mora_vigente=True`) tiene prohibida la apertura de nuevos productos bancarios, lanzando `ClienteConMoraException`.
   * **Regla 2 (Operaciones monetarias):** Todo intento de giro que exceda los fondos permitidos (saldo o saldo + sobregiro) es rechazado mediante `SaldoInsuficienteException`. Adicionalmente, cualquier operación sobre cuentas con bloqueo administrativo activo lanza `CuentaBloqueadaException`, y no se permite pagar cuotas de créditos no aprobados.
5. **Cálculo monetario con indicador externo:**
   * Integración de la cotización real de la Unidad de Fomento (UF) chilena en pesos (CLP) consultada en vivo desde el servicio público `https://mindicador.cl/api/uf`.
   * Cálculo ilustrativo del costo de tasación bancaria (ejemplo: **2 UF** convertidas a pesos según el valor de mercado del día).

### 1.4 Estructura del Proyecto
```text
├── dao/                         # Capa de Acceso a Datos (Data Access Object)
│   ├── __init__.py              # Exportación de clases DAO y conexión
│   ├── conexion.py              # Gestión de conexión SQLite y esquema con claves foráneas
│   ├── cliente_dao.py           # CRUD completo para Cliente
│   ├── cuenta_dao.py            # CRUD completo y reconstrucción polimórfica de Cuentas
│   └── transaccion_dao.py       # CRUD completo para Transaccion y DetalleTransaccion
├── model/                       # Capa de Dominio (Entidades POO)
│   ├── __init__.py              # Exportaciones unificadas del modelo
│   ├── cliente.py               # Entidad Cliente con validación de RUT
│   ├── cuenta.py                # Clase base Cuenta
│   ├── cuenta_ahorro.py         # Subtipo Cuenta de Ahorro
│   ├── cuenta_corriente.py      # Subtipo Cuenta Corriente con sobregiro
│   ├── cuenta_vista.py          # Subtipo Cuenta Vista con cobro fijo
│   ├── credito.py               # Crédito y gestión de cuotas
│   ├── cuota_credito.py         # Cuota individual amortizada
│   ├── empleado.py              # Clase base Empleado
│   ├── ejecutivo.py             # Empleado comercial con aprobación de créditos
│   ├── cajero.py                # Empleado de ventanilla
│   ├── transaccion.py           # Transacción bancaria
│   ├── detalle_transaccion.py   # Línea de detalle de transacción
│   └── excepciones.py           # Excepciones de negocio personalizadas
├── servicios/                   # Capa de Servicios Externos y Compatibilidad
│   ├── __init__.py
│   ├── indicadores.py           # Consumo de API UF con requests, timeout y control de fallas
│   └── persistencia.py          # Adaptador de persistencia retrocompatible
├── test_dao.py                  # Pruebas automatizadas de la capa DAO (CRUD)
├── test_reglas_banco.py         # Pruebas unitarias de reglas de negocio y POO
├── test_sumativa3.py            # Pruebas de API requests, validaciones y SQLite
├── requirements.txt             # Dependencias del proyecto (requests)
├── main.py                      # Punto de entrada y demostración integral del sistema
├── README.md                    # Documentación técnica oficial
└── GUIA_DE_CORRECCION_Y_ENTREGA.md # Pasos de verificación y entrega
```

---

## Apartado 2: Instalación y Ejecución

### 2.1 Requisitos Previos
* **Python 3.10 o superior** (probado y certificado en Python 3.14).
* Acceso a Internet para la consulta en vivo de la UF (si no hay red, el sistema continúa funcionando de forma segura sin interrumpir la ejecución).

### 2.2 Instalación de Dependencias
1. Clonar o descomprimir el proyecto en una carpeta de trabajo.
2. Abrir una terminal en el directorio raíz (donde se ubica `main.py`).
3. Instalar las dependencias especificadas en `requirements.txt`:

```bash
pip install -r requirements.txt
```

> **Nota para Windows:** Si al escribir `python` o `pip` se abre la Microsoft Store o aparece *"Python was not found"*, utilice el comando `py` en su lugar (`py -m pip install -r requirements.txt` y `py main.py`), o desactive los alias de ejecución en Windows (*Configuración > Aplicaciones > Alias de ejecución de aplicaciones > Desactivar python.exe de Microsoft Store*). También puede invocar la ruta completa de su ejecutable de Python.

### 2.3 Comandos de Ejecución

#### A. Demostración Principal Integral
```bash
python main.py
```
*(O en Windows: `py main.py`)*

Este comando ejecuta de manera secuencial los 10 módulos del sistema:
1. Creación de clientes, ejecutivos y cajeros con validación de RUT.
2. Apertura e inicialización de cuentas de ahorro, corriente y vista.
3. Demostración de polimorfismo con `girar()` y `calcular_costo_mantencion()`.
4. Captura y manejo seguro de `SaldoInsuficienteException`, `CuentaBloqueadaException` y `ClienteConMoraException`.
5. Solicitud, aprobación por ejecutivo y pago amortizado de crédito bancario.
6. Emisión de transacción con desglose de múltiples líneas de detalle.
7. Persistencia SQLite y demostración de operaciones CRUD completas en la capa DAO.
8. Consulta segura de UF mediante la librería `requests` y cálculo de tasación bancaria.
9. Validación observable de entradas de usuario (rechazo de `NaN`, `inf`, texto, negativos y cero).
10. Verificación final de consistencia del sistema.

#### B. Ejecución de la Suite Completa de Pruebas Automatizadas
```bash
python -m unittest discover -v
```
*(O en Windows: `py -m unittest discover -v`)*

Ejecuta **23 pruebas unitarias** divididas en 3 suites:
* `test_dao.py` (5 pruebas): Operaciones CRUD en `ClienteDAO`, `CuentaDAO` (polimórfica) y `TransaccionDAO`, más integridad referencial y rollback.
* `test_reglas_banco.py` (5 pruebas): Reglas de negocio POO, dígito verificador de RUT, agregación y bloqueo por mora.
* `test_sumativa3.py` (13 pruebas): Integración con `requests`, timeouts, errores HTTP (503), caídas de red, JSON malformado, persistencia en disco y validación de montos.

Resultado esperado: **`Ran 23 tests ... OK`**.

#### C. Opciones de Ejecución Adicionales
```bash
python main.py --sin-api                 # Ejecución demostrativa sin acceder a Internet
python main.py --interactivo             # Permite teclear montos manualmente por consola
python main.py --bd otra_base.sqlite3    # Especifica una ruta personalizada para SQLite
python main.py --help                    # Despliega la ayuda de parámetros CLI
```

### 2.4 Demostración de Persistencia entre Ejecuciones
Para comprobar que los datos no son meras variables en memoria y persisten en disco:
1. Ejecutar: `python main.py --sin-api`  
   *(Se inicializa la base `banco_demo.sqlite3` y se guardan los registros).*
2. Ejecutar nuevamente: `python main.py --sin-api`  
   *(El sistema reporta: `[OK] Registro de ejecución anterior leído desde SQLite: ('CC-2002', ...)`).*

---

## Apartado 3: Decisiones de Diseño y Seguridad (POO Seguro)

### 3.1 Arquitectura en Capas y Patrón DAO
Se desacopló la lógica de negocio del almacenamiento de datos separando estrictamente:
* **`model/`**: Entidades puras de dominio bancario, independientes de cualquier motor de base de datos.
* **`dao/`**: Clases especializadas (`ClienteDAO`, `CuentaDAO`, `TransaccionDAO`) responsables de las operaciones CRUD (Crear, Consultar, Actualizar, Eliminar).
* **`servicios/`**: Integración de datos externos (`indicadores.py`) desacoplada del flujo de la aplicación.

### 3.2 Prevención de Inyección SQL y Transaccionalidad
* **Consultas Parametrizadas:** Ninguna consulta SQL concatena cadenas ni interpola variables de usuario. Todas las sentencias utilizan marcadores de posición posicionales (`?`), delegando el escape seguro al controlador `sqlite3`.
* **Integridad Referencial:** En cada conexión se ejecuta de manera obligatoria `PRAGMA foreign_keys = ON;`, impidiendo que existan cuentas huérfanas o detalles sin transacción válida asociada.
* **Gestión de Transacciones ACID:** Las escrituras críticas se ejecutan dentro de bloques de contexto `with conexion:`, garantizando que si una operación intermedia falla, se ejecuta automáticamente un `ROLLBACK` y se mantiene la base de datos consistente.

### 3.3 Encapsulamiento y Protección contra Manipulación
* **Atributos Privados:** Todas las variables de estado críticas utilizan prefijo de doble guion bajo (`__saldo`, `__bloqueada`, `__mora_vigente`, `__detalles`, etc.), evitando accesos directos desde el exterior.
* **Getters y Setters con Invariantes:** Las mutaciones de estado pasan por validadores estrictos. Por ejemplo:
  * El setter de `mora_vigente` solo admite booleanos estrictos (`TypeError`).
  * El setter de `rut` recalcula el dígito verificador y, si no coincide, rechaza el cambio manteniendo el RUT anterior.
  * Los métodos de cobro y abono rechazan tipos coercitivos como `bool` y valores no finitos como `math.nan` y `math.inf`.

### 3.4 Consumo Seguro y Continuidad de la API Externa
* Se adoptó la librería **`requests`** con un límite estricto de espera de **5 segundos** (`timeout=5`) para prevenir bloqueos por congelamiento de socket.
* Manejo granular de fallos de red (`requests.exceptions.ConnectionError`), caídas del servidor remoto (`requests.exceptions.HTTPError`), timeouts (`requests.exceptions.Timeout`) y respuestas corruptas (`requests.exceptions.JSONDecodeError`).
* **Principio de Continuidad del Servicio:** Ante fallos de la API, el sistema captura `ErrorIndicador`, notifica un `[AVISO]` claro al operador y **continúa la ejecución del banco sin interrumpir la operación ni fabricar cotizaciones falsas**.

---

## Apartado 4: Uso de Inteligencia Artificial con Ejemplos Concretos y Justificación Técnica

### 4.1 Declaración de Uso de IA
En el desarrollo y revisión de este proyecto se empleó asistencia de Inteligencia Artificial (ChatGPT / Antigravity) como herramienta de soporte para la revisión de retroalimentación docente, sugerencias de refactorización y elaboración de casos de prueba. Las alumnas integrantes analizaron, ejecutaron, adaptaron y validaron técnicamente cada fragmento de código antes de incorporarlo al proyecto.

### 4.2 Ejemplos Concretos de Asistencia y Justificación Técnica

#### Ejemplo 1: Diseño de la Capa DAO con Consultas Parametrizadas
* **Interacción / Prompt:**  
  *Solicitud:* *"Diseñar una capa `dao/` separada de `model/` para SQLite que implemente CRUD completo para Cliente, Cuenta y Transacción, reconstruyendo las subclases polimórficas de Cuenta sin acoplar el modelo a SQL"*.
* **Propuesta de la IA:** Implementación de clases `ClienteDAO`, `CuentaDAO` y `TransaccionDAO` con sentencias `INSERT ... ON CONFLICT DO UPDATE` y consultas parametrizadas `?`.
* **Justificación técnica y validación del equipo:**  
  Se aceptó el uso de `ON CONFLICT(numero) DO UPDATE SET ...` porque permite actualizar cuentas existentes sin generar duplicados. Sin embargo, el equipo detectó que al reconstruir `Cuenta` desde SQLite, si el cliente titular tenía `mora_vigente=True`, el constructor de `Cuenta` lanzaba `ClienteConMoraException` (diseñada para nuevas aperturas). El equipo corrigió este comportamiento en `CuentaDAO._instanciar_subtipo()` para preservar el titular y permitir la lectura histórica sin violar la regla de negocio.

#### Ejemplo 2: Transición de `urllib` a `requests` y Dobles de Prueba
* **Interacción / Prompt:**  
  *Solicitud:* *"Reemplazar urllib por requests en servicios/indicadores.py aplicando timeout de 5 segundos, control de fallas y diseñar dobles de prueba para verificarlo sin conexión a Internet"*.
* **Propuesta de la IA:** Reescribir `obtener_uf()` usando `requests.get()`, `resp.raise_for_status()`, capturar `requests.exceptions.RequestException` y utilizar una clase `MockResponse` en las pruebas unitarias.
* **Justificación técnica y validación del equipo:**  
  `requests` simplifica la lectura de JSON y el manejo de códigos de estado HTTP frente a la verbosidad de `urllib`. La clase `MockResponse` se validó para simular caídas de red (`ConnectionError`), timeouts (`Timeout`) y errores de servidor (`503 Service Unavailable`), garantizando que la suite de pruebas unitarias pueda ejecutarse de forma 100% reproducible y offline en cualquier computador.

#### Ejemplo 3: Detección de Vulnerabilidad de Coerción en Montos Monetarios
* **Interacción / Prompt:**  
  *Solicitud:* *"Auditar los métodos girar() y depositar() de Cuenta en busca de fallos de seguridad en la validación de tipos numéricos"*.
* **Propuesta de la IA:** La validación previa `if not isinstance(monto, (int, float)) or monto <= 0:` presentaba dos brechas: en Python, `bool` hereda de `int` (`isinstance(True, int)` es `True`), y `float('nan') <= 0` evalúa a `False`. Esto permitía depositar `True` (sumando $1) o `float('nan')` (contaminando el saldo a `NaN`).
* **Justificación técnica y validación del equipo:**  
  El equipo adoptó de inmediato la sugerencia de blindaje en `model/cuenta.py` y sus subtipos:
  ```python
  if isinstance(monto, bool) or not isinstance(monto, (int, float)) or not math.isfinite(monto) or monto <= 0:
      raise ValueError("El monto a girar debe ser un número positivo y finito mayor a 0.")
  ```
  Esta decisión responde directamente al criterio evaluado de Programación Orientada a Objeto Seguro, garantizando integridad matemática y tipos estrictos.

---

## Apartado 5: Verificación de Pruebas

Para reproducir la verificación oficial ejecutada en el entorno:
```bash
python -m unittest discover -v
```
Se ejecutan **23 pruebas unitarias**, todas con resultado `ok`:
* 5 pruebas en `test_dao.py` (CRUD completo y claves foráneas).
* 5 pruebas en `test_reglas_banco.py` (reglas bancarias y encapsulamiento).
* 13 pruebas en `test_sumativa3.py` (API `requests`, validación de entradas y persistencia).
