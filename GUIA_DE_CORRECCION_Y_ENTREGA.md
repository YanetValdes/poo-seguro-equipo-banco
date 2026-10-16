# Guía de revisión y entrega | Sumativa 3, Sistema Bancario

## Primero: qué pasó con la nota

Según el correo del profesor, Sumativa 3 se evaluó sobre el **último commit anterior al 13 de octubre de 2026 a las 23:59**. El que evaluó fue `7cf63c4` del 12 de octubre, correspondiente a correcciones de Sumativa 2. Por eso la nota se refiere a funciones que **no estaban publicadas** en esa revisión. El informe Word corregido de Sumativa 2 **no sustituye** la entrega del repositorio de Sumativa 3.

Este archivo explica cómo revisar una versión posterior corregida y solicitar autorización para que el docente la reevalúe. **No asegura que la nota de la entrega original cambie.**

## 1. Abrir los archivos correctamente

1. Descomprimir `Sistema_Bancario_Sumativa3_REVISADO.zip`.
2. Entrar en la carpeta `poo-seguro-equipo-banco-main` (debe verse `main.py`).
3. Abrir esa carpeta en Visual Studio Code, Antigravity o el editor de Python que usen.
4. Abrir una terminal dentro de esa misma carpeta.
5. En Windows pueden usar `py` en lugar de `python`, o desactivar los alias de la tienda de Windows en Configuración de aplicaciones si `python` no responde.

## 2. Ejecutar el programa

```bash
python --version
python main.py
```

Comprobar que aparecen las secciones: RUT inválido, excepciones de negocio, tres tipos de cuenta, transacción, SQLite, UF por API y validación de entradas.

Si aparece `[AVISO]` al consultar la API, eso indica que el código controló una falla del servicio o de la conexión, **no** que la consulta haya tenido éxito. Cuando Internet funcione, deben volver a ejecutar para verificar una cotización real.

Si no tienen Internet, pueden ejecutar de manera intencional:

```bash
python main.py --sin-api
```

## 3. Ejecutar 23 pruebas automatizadas

```bash
python -m unittest discover -v
```

Se debe ver `Ran 23 tests` y `OK`. Las pruebas cubren DAO y CRUD completo (`test_dao.py`), reglas de negocio POO (`test_reglas_banco.py`) y peticiones con `requests` y persistencia (`test_sumativa3.py`).

## 4. Demostrar que la información permanece guardada

Ejecutar dos veces (sin borrar la base):

```bash
python main.py --sin-api
python main.py --sin-api
```

En la primera ejecución debe aparecer el mensaje de cuentas recuperadas al reabrir SQLite y el ciclo CRUD del DAO. En la segunda, además, debe aparecer que se recuperó un registro de la ejecución anterior. El archivo `banco_demo.sqlite3` se genera automáticamente y **no** debe subirse a GitHub.

## 5. Ingresar un dato por teclado

```bash
python main.py --interactivo --sin-api
```

Primero probar `abc` y comprobar el rechazo. Ejecutar otra vez e ingresar `25000`: se acepta. La sección 9 también demuestra entradas inválidas de forma automática.

## 6. Actualizar GitHub con un nuevo commit

**Importante:** Para poder usar `git push`, deben disponer de acceso al repositorio y autenticación en GitHub. No hay cambios remotos automáticos al descomprimir un ZIP.

Opción con terminal Git instalada:

```bash
git clone https://github.com/YanetValdes/poo-seguro-equipo-banco.git
cd poo-seguro-equipo-banco
```

Copiar **el contenido interno** de la carpeta corregida dentro de la carpeta clonada, reemplazando los archivos existentes y agregando los nuevos. Debe quedar `main.py` en la raíz, con `model/`, `dao/` y `servicios/` al lado. No crear una carpeta `poo-seguro-equipo-banco-main` dentro del repositorio.

Luego ejecutar:

```bash
git status
git add README.md main.py model dao servicios requirements.txt test_reglas_banco.py test_sumativa3.py test_dao.py GUIA_DE_CORRECCION_Y_ENTREGA.md EVIDENCIA_TECNICA_PRUEBAS.txt .gitignore
git commit -m "Implementar Sumativa 3: Capa DAO CRUD, requests API UF, validaciones seguras y 23 pruebas"
git push origin main
```

Si `git push` falla por permisos o autenticación, la propietaria del repositorio debe ingresar a su cuenta de GitHub y configurar el acceso. Si aparecen cambios remotos inesperados, detenerse y revisar antes de sobrescribir.

Después de subir, abrir el repositorio en GitHub y comprobar que aparecen en la raíz las carpetas `model/`, `dao/`, `servicios/`, más `main.py`, `README.md`, `requirements.txt` y los archivos de prueba. Verificar también la fecha y el identificador del nuevo commit.

## 7. Evidencias que conviene guardar

- Captura de terminal de `python -m unittest discover -v` mostrando 23 tests y `OK`.
- Captura de `python main.py` mostrando validación de RUT, reglas bancarias y polimorfismo.
- Capturas de sección 7: primera y segunda ejecución con SQLite persistido y demostración CRUD del DAO.
- Captura de sección 8 con **cotización UF real y precio en pesos** vía `requests`.
- Captura de sección 9 con entrada aceptada y rechazada.
- Pantallazo del nuevo commit con las carpetas `dao/`, `model/`, `servicios/` en GitHub.

Las capturas deben venir de la ejecución real del programa; no inventar salidas ni afirmar una consulta UF real si solo se probaron respuestas simuladas.

## 8. Cómo responder al docente

Solicitar respetuosamente si existe una posibilidad de **reevaluación excepcional o actividad recuperativa**, dejando explícito que las correcciones se publicaron *después* del plazo y que se entiende la evaluación del commit originalmente entregado. Adjuntar el enlace al nuevo commit, la salida de pruebas y explicar que la nueva versión contempla SQLite, API UF, validaciones, manejo de fallas y README. No presentar el cambio posterior como entrega puntual de la evaluación original.

## 9. Limitaciones de esta revisión

- Se usó como base el ZIP suministrado y el correo del profesor.
- No se adjuntó la **rúbrica completa oficial de Sumativa 3**; las mejoras se vincularon con los seis criterios enumerados en el correo.
- La API puede estar inaccesible desde algunas redes: las pruebas automatizadas verifican lógica sin conexión, pero **no prueban disponibilidad pública en vivo**.
- El proyecto es docente y de demostración, no un sistema financiero real.
