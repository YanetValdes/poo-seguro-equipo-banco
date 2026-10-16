"""
Consulta segura de la UF chilena para el sistema bancario mediante la librería requests.
Aplica validación estricta de cotizaciones, tiempo de espera (timeout) y manejo de excepciones.
"""
import math
import requests

API_UF = "https://mindicador.cl/api/uf"


class ErrorIndicador(Exception):
    """No fue posible consultar una cotización de UF válida."""


def obtener_uf(timeout=5, requester=None, session=None, opener=None):
    """
    Obtiene la cotización de la UF en CLP utilizando la librería requests y la API pública.
    Nunca fabrica una cotización falsa ni genera datos simulados como reales.

    Parámetros opcionales permiten inyectar simulaciones para pruebas sin conexión:
      - `requester`: función callable(url, timeout, headers) -> response
      - `session`: instancia de requests.Session
      - `opener`: adaptador de compatibilidad para pruebas legadas
    """
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("El timeout debe ser positivo y finito.")

    headers = {
        "Accept": "application/json",
        "User-Agent": "SistemaBancoAcademico/1.0",
    }

    try:
        if requester is not None:
            resp = requester(API_UF, timeout=timeout, headers=headers)
        elif session is not None:
            resp = session.get(API_UF, timeout=timeout, headers=headers)
        elif opener is not None:
            # Adaptador de compatibilidad para pruebas que usan opener
            class DummyReq:
                full_url = API_UF
            raw = opener(DummyReq(), timeout=timeout)
            import json
            datos = json.load(raw)
            resp = None
        else:
            resp = requests.get(API_UF, timeout=timeout, headers=headers)

        if resp is not None:
            if hasattr(resp, "raise_for_status"):
                resp.raise_for_status()
            datos = resp.json()

    except (requests.exceptions.Timeout, TimeoutError) as exc:
        raise ErrorIndicador("Falla por tiempo de espera de la API (timeout).") from exc
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.RequestException, OSError) as exc:
        raise ErrorIndicador("Falla de conexión o error HTTP de la API.") from exc
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
