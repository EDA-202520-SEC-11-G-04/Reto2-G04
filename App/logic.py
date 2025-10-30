import time
import sys
import csv
from collections import Counter, defaultdict
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
import DataStructures.array_list as list
from DataStructures.Map import map_linear_probing as mp
import App.logic2 as logic2

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


def req_3(catalog, distancia_inicial, distancia_final, n):
    """Retorna el resultado del requerimiento 3"""

    inicio = time.process_time()

    viajes_filtrados = list.new_list()
    
    if isinstance(catalog, dict):
       if "trips" in catalog:
          catalog = catalog["trips"]
       elif "model" in catalog and "catalog" in catalog["model"]:
          catalog = catalog["model"]["catalog"]["trips"]


    lista_viajes = catalog
    for i in range(list.size(lista_viajes)):
        viaje = list.get_element(lista_viajes, i)

        try:
            distancia = float(viaje.get("trip_distance", 0))
        except ValueError:
            continue

        if distancia >= distancia_inicial and distancia <= distancia_final:
            list.add_last(viajes_filtrados, viaje)

    if list.size(viajes_filtrados) == 0:
        return {"mensaje": "No hay trayectos en ese rango de distancia"}

    # Ordenar
    viajes_ordenados = list.merge_sort(viajes_filtrados, logic2.sort_criteria)

    total = list.size(viajes_ordenados)

    # Obtener los primeros n y los últimos n elementos
    primeros = list.sub_list(viajes_ordenados, 0, n)
    ultimos = list.sub_list(viajes_ordenados, max(0, total - n), n)

    fin = time.process_time()
    tiempo_ms = (fin - inicio) * 1000

    resultado = {
        "total_trayectos": total,
        "primeros": primeros,
        "ultimos": ultimos,
        "tiempo_ms": tiempo_ms
    }

    return resultado



    
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

    if not catalog or "elements" not in catalog:
        return {"mensaje": "Catálogo inválido o vacío."}

    try:
        fecha_terminacion = datetime.strptime(fecha_terminacion_str, "%Y-%m-%d").date()
        tiempo_ref = datetime.strptime(tiempo_ref_str, "%H:%M:%S").time()
    except Exception as e:
        return {"mensaje": f"Formato de fecha/hora inválido: {e}"}

    inicio_t = time.time()

    tabla = mp.new_map(100, 0.5)

    for t in catalog["elements"]:
        try:
            drop_dt = datetime.strptime(t["dropoff_datetime"], "%Y-%m-%d %H:%M:%S")
        except:
            continue

        drop_date_str = drop_dt.strftime("%Y-%m-%d")
        drop_time = drop_dt.time()

        cond = (momento == "ANTES" and drop_time < tiempo_ref) or (momento == "DESPUES" and drop_time > tiempo_ref)
        if cond:
            trips = mp.get(tabla, drop_date_str)
            if trips is None:
                trips = list.new_list()
            list.add_last(trips, t)
            mp.put(tabla, drop_date_str, trips)

    fecha_str = fecha_terminacion.strftime("%Y-%m-%d")
    filtrados = mp.get(tabla, fecha_str)

    if not filtrados or list.size(filtrados) == 0:
        fin_t = time.time()
        return {
            "tiempo_ms": round((fin_t - inicio_t) * 1000, 2),
            "total_trayectos": 0,
            "primeros": list.new_list(),
            "ultimos": list.new_list(),
            "mensaje": "No se encontraron trayectos en el rango indicado."
        }

    filtrados = list.merge_sort(filtrados, sort_criteria_dropoff_desc)

    total = list.size(filtrados)
    primeros = list.sub_list(filtrados, 0, min(n, total))
    ultimos = list.sub_list(filtrados, max(0, total - n), min(n, total))

    fin_t = time.time()
    return {
        "tiempo_ms": round((fin_t - inicio_t) * 1000, 2),
        "total_trayectos": total,
        "primeros": primeros,
        "ultimos": ultimos
    }




def req_5(catalog, fecha_str, hora_final_str, n):
    """Retorna el resultado del requerimiento 5"""
    inicio = time.process_time()

    mapa_horas = mp.new_map(50, 0.7)  

    total_trayectos = 0
    fecha_limite = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    hora_limite = datetime.strptime(hora_final_str, "%H:%M:%S").time()

    for i in range(list.size(catalog)):
        viaje = list.get_element(catalog, i)
        try:
            dropoff = datetime.strptime(viaje.get("dropoff_datetime"), "%Y-%m-%d %H:%M:%S")
            costo = float(viaje.get("total_amount", 0))
            pickup = datetime.strptime(viaje.get("pickup_datetime"), "%Y-%m-%d %H:%M:%S")
            duracion = (dropoff - pickup).total_seconds() / 60 
        except (ValueError, TypeError):
            continue

        # Filtrar fecha y hora
        if dropoff.date() == fecha_limite and dropoff.time() <= hora_limite:
            hora = str(dropoff.hour).zfill(2) 

            if not mp.contains(mapa_horas, hora):
                mp.put(mapa_horas, hora, list.new_list())

            # Agregar viajes
            lista_hora = mp.get(mapa_horas, hora)
            list.add_last(lista_hora, {"costo": costo, "duracion": duracion})
            mp.put(mapa_horas, hora, lista_hora)
            total_trayectos += 1

    if total_trayectos == 0:
        return {"mensaje": "No se encontraron trayectos con esa fecha y hora límite."}

    resultados = list.new_list()
    llaves = mp.key_set(mapa_horas)

    for i in range(list.size(llaves)):
        hora = list.get_element(llaves, i)
        lista = mp.get(mapa_horas, hora)

        costos = [viaje["costo"] for viaje in lista["elements"]]
        duraciones = [viaje["duracion"] for viaje in lista["elements"]]

        promedio_costo = sum(costos) / len(costos)
        min_costo = min(costos)
        max_costo = max(costos)

        promedio_duracion = sum(duraciones) / len(duraciones)
        min_duracion = min(duraciones)
        max_duracion = max(duraciones)

        list.add_last(resultados, {
            "hora": hora,
            "promedio_costo": promedio_costo,
            "min_costo": min_costo,
            "max_costo": max_costo,
            "promedio_duracion": promedio_duracion,
            "min_duracion": min_duracion,
            "max_duracion": max_duracion
        })



    resultados_ordenados = list.merge_sort(resultados, logic2.sort_horas)
    total_horas = list.size(resultados_ordenados)

    # Primeras y últimas n horas
    primeros = list.sub_list(resultados_ordenados, 0, n)
    ultimos = list.sub_list(resultados_ordenados, max(0, total_horas - n), n)

    fin = time.process_time()
    tiempo_ms = (fin - inicio) * 1000

    return {
        "total_trayectos": total_trayectos,
        "primeros": primeros,
        "ultimos": ultimos,
        "tiempo_ms": tiempo_ms
    }

def req_6(catalog, hora_inicial, hora_final, barrio_inicial, n):
    """Retorna el resultado del requerimiento 6 (viajes por rango de hora y barrio)."""

    inicio = time.process_time()

    total_viajes = 0
    total_distancia = 0
    total_duracion = 0

    mapa_destinos = mp.new_map(100, 0.7)
    mapa_metodos = mp.new_map(10, 0.7)

    for i in range(list.size(catalog)):
        viaje = list.get_element(catalog, i)
        try:
            pickup = datetime.strptime(viaje.get("pickup_datetime"), "%Y-%m-%d %H:%M:%S")
            dropoff = datetime.strptime(viaje.get("dropoff_datetime"), "%Y-%m-%d %H:%M:%S")
            distancia = float(viaje.get("trip_distance", 0))
            metodo = viaje.get("payment_type", "Desconocido")
            barrio_origen = viaje.get("pickup_barrio", "").strip()
            barrio_destino = viaje.get("dropoff_barrio", "").strip()
        except (ValueError, TypeError, AttributeError):
            continue

        # Filtro por rango de hora
        if hora_inicial <= pickup.hour <= hora_final and barrio_origen == barrio_inicial:
            duracion = (dropoff - pickup).total_seconds() / 60
            total_viajes += 1
            total_distancia += distancia
            total_duracion += duracion

            # Contar destinos
            if not mp.contains(mapa_destinos, barrio_destino):
                mp.put(mapa_destinos, barrio_destino, 1)
            else:
                valor = mp.get(mapa_destinos, barrio_destino)
                mp.put(mapa_destinos, barrio_destino, valor + 1)

            # Contar métodos de pago
            if not mp.contains(mapa_metodos, metodo):
                mp.put(mapa_metodos, metodo, {"cantidad": 1, "recaudo": float(viaje.get("total_amount", 0))})
            else:
                info = mp.get(mapa_metodos, metodo)
                info["cantidad"] += 1
                info["recaudo"] += float(viaje.get("total_amount", 0))
                mp.put(mapa_metodos, metodo, info)

    if total_viajes == 0:
        return {"mensaje": "No se encontraron trayectos en ese rango de horas para el barrio indicado."}

    distancia_promedio = total_distancia / total_viajes
    duracion_promedio = total_duracion / total_viajes

    # Calcular el barrio más visitado
    destinos = mp.key_set(mapa_destinos)
    barrio_mas_visitado = None
    max_viajes = 0

    for i in range(list.size(destinos)):
        barrio = list.get_element(destinos, i)
        cantidad = mp.get(mapa_destinos, barrio)
        if cantidad > max_viajes:
            max_viajes = cantidad
            barrio_mas_visitado = barrio

    # Métodos de pago más usados y de mayor recaudo
    metodos = mp.key_set(mapa_metodos)
    metodo_mas_usado = None
    metodo_mayor_recaudo = None
    max_uso = 0
    max_recaudo = 0

    for i in range(list.size(metodos)):
        metodo = list.get_element(metodos, i)
        info = mp.get(mapa_metodos, metodo)
        if info["cantidad"] > max_uso:
            max_uso = info["cantidad"]
            metodo_mas_usado = metodo
        if info["recaudo"] > max_recaudo:
            max_recaudo = info["recaudo"]
            metodo_mayor_recaudo = metodo

    # Lista de destinos más frecuentes
    lista_destinos = list.new_list()
    for i in range(list.size(destinos)):
        barrio = list.get_element(destinos, i)
        cantidad = mp.get(mapa_destinos, barrio)
        list.add_last(lista_destinos, {"barrio_destino": barrio, "cantidad": cantidad})

    def sort_destinos(d1, d2):
        return d1["cantidad"] > d2["cantidad"]

    destinos_ordenados = list.merge_sort(lista_destinos, sort_destinos)
    primeros = list.sub_list(destinos_ordenados, 0, n)

    fin = time.process_time()
    tiempo_ms = (fin - inicio) * 1000

    return {
        "total_viajes": total_viajes,
        "distancia_promedio": distancia_promedio,
        "duracion_promedio": duracion_promedio,
        "barrio_destino_mas_visitado": barrio_mas_visitado,
        "metodo_mas_usado": metodo_mas_usado,
        "metodo_mayor_recaudo": metodo_mayor_recaudo,
        "primeros": primeros,
        "tiempo_ms": tiempo_ms
    }


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
