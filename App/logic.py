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
    - Filtra los trayectos cuya 'Inicio' está entre fecha_inicio_str y fecha_fin_str (inclusive).
    - Ordena del más antiguo al más reciente (usando merge_sort de array_list).
    - Devuelve los N primeros y N últimos trayectos (si el filtro produce < 2N, devuelve todos).
    """

    # Vérification du control
    if not control or "elements" not in control:
        return {
            "tiempo_ejecucion_ms": 0.0,
            "total_trayectos": 0,
            "primeros": [],
            "ultimos": [],
            "mensaje": "Control inválido o sin elementos."
        }

    # Parsing des dates d'entrée
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

    # --- Filtrage ---
    filtrados = list.new_list()

    for t in control["elements"]:
        try:
            inicio_s = t.get("pickup_datetime", "")
            fin_s = t.get("dropoff_datetime", "")

            inicio_dt = datetime.strptime(inicio_s, "%Y-%m-%d %H:%M:%S")

            if fecha_inicio <= inicio_dt <= fecha_fin:
                try:
                    fin_dt = datetime.strptime(fin_s, "%Y-%m-%d %H:%M:%S")
                    dur_min = round((fin_dt - inicio_dt).total_seconds() / 60, 2)
                except Exception:
                    dur_min = None

                distancia = float(t.get("trip_distance", 0.0))
                costo = float(t.get("total_amount", 0.0))

                list.add_last(filtrados, {
                    "Inicio": inicio_s,
                    "Fin": fin_s,
                    "Duración (min)": dur_min,
                    "Distancia (mi)": distancia,
                    "Costo total ($)": costo
                })
        except:
            continue

    total = list.size(filtrados)
    if total == 0:
        fin_t = time.time()
        return {
            "tiempo_ejecucion_ms": round((fin_t - inicio_t) * 1000, 2),
            "total_trayectos": 0,
            "primeros": [],
            "ultimos": [],
            "mensaje": "No se encontraron trayectos en el rango indicado."
        }

    # --- Tri sur 'Inicio' ---
    filtrados = list.merge_sort(filtrados, sort_criteria_inicio)

    # --- Extraction des premiers et derniers ---
    elements = filtrados["elements"]
    if total <= 2 * n:
        primeros = elements
        ultimos = []
    else:
        primeros = elements[:n]
        ultimos = elements[-n:]

    fin_t = time.time()

    return {
        "tiempo_ejecucion_ms": round((fin_t - inicio_t) * 1000, 2),
        "total_trayectos": total,
        "primeros": primeros,
        "ultimos": ultimos
    }


def sort_criteria_inicio(t1, t2):
    return t1["Inicio"] < t2["Inicio"]

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
