"""Consulta segura de la UF chilena para una simulación bancaria académica."""
import json
import math
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_UF = "https://mindicador.cl/api/uf"


class ErrorIndicador(Exception):
    """No fue posible consultar una cotización de UF válida."""


def obtener_uf(timeout=5, opener=urlopen):
    """Obtiene UF en CLP usando una API real; nunca fabrica una cotización.

    `opener` permite simular respuestas en pruebas sin acceder a Internet.
    """
    if not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("El timeout debe ser positivo y finito.")
    solicitud = Request(
        API_UF,
        headers={"Accept": "application/json", "User-Agent": "SistemaBancoAcademico/1.0"},
    )
    try:
        with opener(solicitud, timeout=timeout) as respuesta:
            datos = json.load(respuesta)
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        raise ErrorIndicador("Falla de conexión, HTTP o tiempo de espera de la API.") from exc
    except (ValueError, UnicodeError, TypeError) as exc:
        raise ErrorIndicador("La API respondió con JSON inválido.") from exc

    if not isinstance(datos, dict):
        raise ErrorIndicador("La API no devolvió un objeto JSON.")
    serie = datos.get("serie")
    if not isinstance(serie, list) or not serie or not isinstance(serie[0], dict):
        raise ErrorIndicador("La API devolvió una serie UF vacía o inesperada.")
    valor = serie[0].get("valor")
    if (isinstance(valor, bool) or not isinstance(valor, (int, float))
            or not math.isfinite(valor) or valor <= 0):
        raise ErrorIndicador("La API devolvió una cotización de UF inválida.")
    return float(valor)


def precio_en_pesos(precio_uf, cotizacion_uf):
    """Calcula un costo de servicio bancario expresado en UF (ejemplo académico)."""
    for nombre, valor in (("Precio expresado en UF", precio_uf),
                          ("Cotización real de la UF", cotizacion_uf)):
        if (isinstance(valor, bool) or not isinstance(valor, (int, float))
                or not math.isfinite(valor) or valor <= 0):
            raise ValueError(f"{nombre} debe ser un número positivo y finito.")
    return round(precio_uf * cotizacion_uf, 2)
