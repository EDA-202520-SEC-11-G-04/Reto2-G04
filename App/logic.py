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
    """
    Retorna el resultado del requerimiento 3
    """
    inicio = time.process_time()  
    
    viajes_filtrados = []  
    for i in range(len(catalog)):
        viaje = catalog[i]  # Obtener el elemento actual
        try:
            distancia = float(viaje.get("trip_distance", 0))  
        except ValueError:
            continue
        
        if distancia >= distancia_inicial and distancia <= distancia_final:
            viajes_filtrados.append(viaje)  # Agregar el viaje a la lista filtrada
    if len(viajes_filtrados) == 0:
        return {"mensaje": "No hay trayectos en ese rango de distancia"}
    
    #lamba para el ordenamiento
    viajes_ordenados = sorted(
        viajes_filtrados, 
        key=lambda x: (
            -float(x.get("trip_distance", 0)),  
            -float(x.get("total_amount", 0))    
        )
    )
    
    total = len(viajes_ordenados)  
    
    # Obtener los primeros N y los últimos N elementos
    primeros = viajes_ordenados[:n]  
    ultimos = viajes_ordenados[-n:]   
    
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




def req_5(catalog, fecha_inicial_str, fecha_final_str):
    """
    Retorna el resultado del requerimiento 5
    """
    inicio = time.process_time() 
    
    # Convertir fechas
    try:
        fecha_inicial = datetime.strptime(fecha_inicial_str, '%Y-%m-%d').date()  
        fecha_final = datetime.strptime(fecha_final_str, '%Y-%m-%d').date()  
    except ValueError:
        return {"mensaje": "Error en el formato de fechas. Usa 'YYYY-MM-DD'."}  # Manejo de error
    
    # Crear el diccionario
    dias = {i: [[] for _ in range(24)] for i in range(7)}  
    total_trayectos = 0  
    
    for i in range(len(catalog)):
        viaje = catalog[i]  
        
        try:
            pickup_str = viaje.get("pickup_datetime")  
            dropoff_str = viaje.get("dropoff_datetime")  
            pickup = datetime.strptime(pickup_str, '%Y-%m-%d %H:%M:%S') 
            dropoff = datetime.strptime(dropoff_str, '%Y-%m-%d %H:%M:%S')  
            fecha = pickup.date()  
        except (KeyError, ValueError, TypeError):
            continue  
        
        if fecha < fecha_inicial or fecha > fecha_final:
            continue 
        
        duracion_minutos = (dropoff - pickup).total_seconds() / 60  
        try:
            costo = float(viaje.get("total_amount", 0)) 
        except ValueError:
            costo = 0  
        
        dia = pickup.weekday()  
        hora = pickup.hour  
        
        dias[dia][hora].append({"costo": costo, "duracion": duracion_minutos})  # Añadir al diccionario
        total_trayectos += 1  
        
    resultados = []  
    
    for dia_num in range(7): 
        nombre_dia = logic2.days_of_week[dia_num]  
        franjas = []  
        
        for hora in range(24):  
            lista_hora = dias[dia_num][hora]
            if not lista_hora: 
                continue
                
            costos = [x["costo"] for x in lista_hora]  
            duraciones = [x["duracion"] for x in lista_hora] 
            
            promedio_costo = sum(costos) / len(costos) if costos else 0
            min_costo = min(costos) if costos else 0
            max_costo = max(costos) if costos else 0
            
            promedio_duracion = sum(duraciones) / len(duraciones) if duraciones else 0
            min_duracion = min(duraciones) if duraciones else 0
            max_duracion = max(duraciones) if duraciones else 0
            
            franjas.append({
                "hora": hora,
                "promedio_costo": promedio_costo,
                "min_costo": min_costo,
                "max_costo": max_costo,
                "promedio_duracion": promedio_duracion,
                "min_duracion": min_duracion,
                "max_duracion": max_duracion
            })
        if franjas:
            resultados.append({"dia": nombre_dia, "franjas": franjas})
            
    fin = time.process_time()  # Obtener el tiempo final
    tiempo_ms = (fin - inicio) * 1000  # Calcular tiempo
    
    return {
        "total_trayectos": total_trayectos,
        "dias": resultados,  
        "tiempo_ms": tiempo_ms
    }

def req_6(catalog, neighborhoods, barrio_inicio, fecha_inicial_str, fecha_final_str):
    """
    Retorna el resultado del requerimiento 6
    """

    inicio = time.time()

    fecha_inicial = datetime.datetime.strptime(fecha_inicial_str, '%Y-%m-%d').date()
    fecha_final = datetime.datetime.strptime(fecha_final_str, '%Y-%m-%d').date()

    viajes_filtrados = []
    total_distancia = 0.0
    total_duracion = 0.0

    for viaje in catalog:
        pickup = datetime.datetime.fromisoformat(viaje["pickup_datetime"])
        dropoff = datetime.datetime.fromisoformat(viaje["dropoff_datetime"])
        fecha = pickup.date()

        if fecha < fecha_inicial or fecha > fecha_final:
            continue

        origen = logic2.encontrar_barrio(float(viaje["pickup_latitude"]), float(viaje["pickup_longitude"]), neighborhoods)

        if origen != barrio_inicio:
            continue

        viajes_filtrados.append(viaje)

        total_distancia += float(viaje["trip_distance"])
        total_duracion += (dropoff - pickup).total_seconds() / 60

    total_viajes = len(viajes_filtrados)

    if total_viajes == 0:
        return {"mensaje": "No se encontraron trayectos para ese barrio y rango de fechas"}

    distancia_promedio = total_distancia / total_viajes
    duracion_promedio = total_duracion / total_viajes

    # Agrupar por barrio destino
    destinos = {}
    for viaje in viajes_filtrados:
        destino = logic2.encontrar_barrio(float(viaje["dropoff_latitude"]), float(viaje["dropoff_longitude"]), neighborhoods)
        if destino not in destinos:
            destinos[destino] = 0
        destinos[destino] += 1

    barrio_destino_mas_visitado = max(destinos, key=destinos.get)

    # Agrupar por método de pago
    metodos = {}
    for viaje in viajes_filtrados:
        metodo = viaje["payment_type"]
        costo = float(viaje["total_amount"])
        pickup = datetime.datetime.fromisoformat(viaje["pickup_datetime"])
        dropoff = datetime.datetime.fromisoformat(viaje["dropoff_datetime"])
        duracion = (dropoff - pickup).total_seconds() / 60

        if metodo not in metodos:
            metodos[metodo] = {"cantidad": 0, "total_pago": 0.0, "total_duracion": 0.0}

        metodos[metodo]["cantidad"] += 1
        metodos[metodo]["total_pago"] += costo
        metodos[metodo]["total_duracion"] += duracion

    # Calcular estadísticas por método
    lista_metodos = []
    for metodo, data in metodos.items():
        cantidad = data["cantidad"]
        promedio_pago = data["total_pago"] / cantidad
        promedio_duracion = data["total_duracion"] / cantidad
        lista_metodos.append({
            "metodo": metodo,
            "cantidad_trayectos": cantidad,
            "promedio_pago": promedio_pago,
            "duracion_promedio": promedio_duracion
        })

    # Encontrar mas_usado (método con mayor cantidad_trayectos)
    mas_usado = max(lista_metodos, key=lambda x: x["cantidad_trayectos"])["metodo"]

    # Encontrar mas_recaudo (método con mayor total_pago, ya que cantidad * promedio_pago = total_pago)
    mas_recaudo = max(metodos, key=lambda m: metodos[m]["total_pago"])

    for metodo in lista_metodos:
        metodo["es_mas_usado"] = (metodo["metodo"] == mas_usado)
        metodo["es_mas_recaudo"] = (metodo["metodo"] == mas_recaudo)

    fin = time.time()
    tiempo_ms = (fin - inicio) * 1000

    return {
        "total_viajes": total_viajes,
        "distancia_promedio": distancia_promedio,
        "duracion_promedio": duracion_promedio,
        "barrio_destino_mas_visitado": barrio_destino_mas_visitado,
        "metodos_pago": lista_metodos,
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
