import time
import sys
import csv
from collections import Counter, defaultdict
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
import DataStructures.array_list as list
from tabulate import tabulate
from DataStructures.Map import map as mp

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

def sort_criteria_dropoff_desc(t1, t2):
    """
    Critère de tri : du plus récent au plus ancien selon dropoff_datetime
    """
    try:
        dt1 = datetime.strptime(t1["dropoff_datetime"], "%Y-%m-%d %H:%M:%S")
        dt2 = datetime.strptime(t2["dropoff_datetime"], "%Y-%m-%d %H:%M:%S")
        return dt1 > dt2   # True si t1 est plus récent → tri décroissant
    except:
        return False
    
def sort_criteria_dropoff_desc(t1, t2):
    """
    Critère de tri : du plus récent au plus ancien selon dropoff_datetime
    """
    try:
        dt1 = datetime.strptime(t1["dropoff_datetime"], "%Y-%m-%d %H:%M:%S")
        dt2 = datetime.strptime(t2["dropoff_datetime"], "%Y-%m-%d %H:%M:%S")
        return dt1 > dt2   # True si t1 est plus récent → tri décroissant
    except:
        return False


def req_4(catalog, fecha_terminacion_str, momento, tiempo_ref_str, n):
    """
    Requerimiento 4:
    - Filtra los trayectos terminados en una fecha específica.
    - Selecciona los que ocurren ANTES o DESPUES de una hora dada.
    - Usa una tabla hash con llave = fecha de terminación.
    - Ordena los resultados del más reciente al más antiguo.
    """

    if not catalog or "elements" not in catalog:
        return {
            "tiempo_ms": 0.0,
            "total_trayectos": 0,
            "primeros": list.new_list(),
            "ultimos": list.new_list(),
            "mensaje": "Catálogo inválido o vacío."
        }

    try:
        fecha_terminacion = datetime.strptime(fecha_terminacion_str, "%Y-%m-%d").date()
        tiempo_ref = datetime.strptime(tiempo_ref_str, "%H:%M:%S").time()
    except Exception as e:
        return {
            "tiempo_ms": 0.0,
            "total_trayectos": 0,
            "primeros": list.new_list(),
            "ultimos": list.new_list(),
            "mensaje": f"Formato de fecha/hora inválido: {e}"
        }

    inicio_t = time.time()

    # --- Création de la table hash ---
    tabla = mp.new_map(100, 0.5)

    # --- Filtrer les trajets ---
    for t in catalog["elements"]:
        try:
            drop_dt = datetime.strptime(t["dropoff_datetime"], "%Y-%m-%d %H:%M:%S")
        except:
            continue

        if drop_dt.date() == fecha_terminacion:
            drop_time = drop_dt.time()
            cond = (momento == "ANTES" and drop_time < tiempo_ref) or \
                   (momento == "DESPUES" and drop_time > tiempo_ref)

            if cond:
                # Si la date n’existe pas encore dans la table, l’ajouter
                if not mp.contains(tabla, fecha_terminacion_str):
                    mp.put(tabla, fecha_terminacion_str, list.new_list())

                trips = mp.get(tabla, fecha_terminacion_str)
                list.add_last(trips, t)
                mp.put(tabla, fecha_terminacion_str, trips)

    # --- Récupérer les trajets filtrés ---
    filtrados = mp.get(tabla, fecha_terminacion_str)
    if not filtrados or list.size(filtrados) == 0:
        fin_t = time.time()
        return {
            "tiempo_ms": round((fin_t - inicio_t) * 1000, 2),
            "total_trayectos": 0,
            "primeros": list.new_list(),
            "ultimos": list.new_list(),
            "mensaje": "No se encontraron trayectos en el rango indicado."
        }

    # --- Trier du plus récent au plus ancien ---
    filtrados = list.merge_sort(filtrados, sort_criteria_dropoff_desc)

    total = list.size(filtrados)

    # --- Extraire N premiers et N derniers ---
    primeros = list.sub_list(filtrados, 0, min(n, total))
    ultimos = list.sub_list(filtrados, max(0, total - n), min(n, total))

    fin_t = time.time()

    return {
        "tiempo_ms": round((fin_t - inicio_t) * 1000, 2),
        "total_trayectos": total,
        "primeros": primeros,
        "ultimos": ultimos
    }



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
