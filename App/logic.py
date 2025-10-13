import time
import sys
import csv
from collections import Counter, defaultdict
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
import DataStructures.array_list as list
from tabulate import tabulate

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    #catalog = {
    #    "trayectos": []}
    catalog=list.new_list()
    return catalog


# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    start_time = time.perf_counter()
    data = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                list.add_last(catalog,row)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

    end_time = time.perf_counter()
    elapsed = (end_time - start_time) * 1000  # milisegundos
    print(f"Archivo cargado correctamente en {elapsed:.2f} ms. Total de trayectos: {list.size(catalog)}")
    return catalog
   

# Funciones de consulta sobre el catálogo

def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    try:
        return list.get_element(catalog, id)
    except IndexError:
        return None


def req_1(control, fecha_inicio_str, fecha_fin_str, n):
    """
    Requerimiento 1:
    - Filtra los trayectos cuya pickup_datetime está entre fecha_inicio_str y fecha_fin_str (inclusive).
    - Ordena del más antiguo al más reciente.
    - Devuelve los N primeros y N últimos (si el filtro produce < 2N trayectos, devuelve todos).
    - Retorna un diccionario con:
        - tiempo_ejecucion_ms
        - total_trayectos
        - primeros: lista de dicts con los campos requeridos
        - ultimos: lista de dicts con los campos requeridos (vacía si no hay)
    Campos devueltos por trayecto:
        - "Inicio" (YYYY-MM-DD HH:MM:SS)
        - "Fin"   (YYYY-MM-DD HH:MM:SS)
        - "Duración (min)" (float, 2 decimales)
        - "Distancia (mi)" (float)
        - "Costo total ($)" (float)
    """

    # Validaciones básicas
    if not control or "elements" not in control or not isinstance(control["elements"], list):
        return {
            "tiempo_ejecucion_ms": 0.0,
            "total_trayectos": 0,
            "primeros": [],
            "ultimos": [],
            "mensaje": "Control inválido o sin elementos."
        }

    # Parseo de las fechas de entrada (si fallan lanzar excepción)
    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d %H:%M:%S")
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return {
            "tiempo_ejecucion_ms": 0.0,
            "total_trayectos": 0,
            "primeros": [],
            "ultimos": [],
            "mensaje": f"Formato de fecha inválido: {e}"
        }

    inicio_t = time.time()

    # Filtrar y almacenar solo los trayectos válidos dentro del rango con la fecha parseada
    filtrados = []
    for t in control["elements"]:
        try:
            pickup_s = t.get("pickup_datetime", "")
            # parseo inline
            pickup_dt = datetime.strptime(pickup_s, "%Y-%m-%d %H:%M:%S")
            if fecha_inicio <= pickup_dt <= fecha_fin:
                # intentar parsear dropoff para calcular duración; si falla, se dejará duración como None
                dropoff_s = t.get("dropoff_datetime", "")
                try:
                    dropoff_dt = datetime.strptime(dropoff_s, "%Y-%m-%d %H:%M:%S")
                    dur_min = round((dropoff_dt - pickup_dt).total_seconds() / 60, 2)
                    dropoff_fmt = dropoff_s
                except Exception:
                    dur_min = None
                    dropoff_fmt = dropoff_s if dropoff_s else ""

                # convertir numericamente distancia y total_amount si es posible
                try:
                    distancia = float(t.get("trip_distance", 0.0))
                except Exception:
                    distancia = 0.0
                try:
                    costo = float(t.get("total_amount", 0.0))
                except Exception:
                    costo = 0.0

                filtrados.append({
                    "_pickup_dt": pickup_dt,            # campo auxiliar para ordenar
                    "Inicio": pickup_s,
                    "Fin": dropoff_fmt,
                    "Duración (min)": dur_min,
                    "Distancia (mi)": distancia,
                    "Costo total ($)": costo
                })
        except Exception:
            # ignorar filas con pickup mal formateado u otros errores
            continue

    total = len(filtrados)

    if total == 0:
        fin_t = time.time()
        return {
            "tiempo_ejecucion_ms": round((fin_t - inicio_t) * 1000, 2),
            "total_trayectos": 0,
            "primeros": [],
            "ultimos": [],
            "mensaje": "No se encontraron trayectos en el rango indicado."
        }

    # Ordenar por pickup datetime (campo auxiliar)
    filtrados.sort(key=lambda x: x["_pickup_dt"])  # del más antiguo al más reciente

    # Quitar campo auxiliar y preparar listas resultado
    # Seleccionar N primeros y N últimos según la regla (si < 2N devolver todos)
    if total <= 2 * n:
        primeros_lista = [ {k:v for k,v in item.items() if k != "_pickup_dt"} for item in filtrados ]
        ultimos_lista = []
    else:
        primeros_lista = [ {k:v for k,v in item.items() if k != "_pickup_dt"} for item in filtrados[:n] ]
        ultimos_lista = [ {k:v for k,v in item.items() if k != "_pickup_dt"} for item in filtrados[-n:] ]

    fin_t = time.time()
    tiempo_ms = round((fin_t - inicio_t) * 1000, 2)

    return {
        "tiempo_ejecucion_ms": tiempo_ms,
        "total_trayectos": total,
        "primeros": primeros_lista,
        "ultimos": ultimos_lista
    }

def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
