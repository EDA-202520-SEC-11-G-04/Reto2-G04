import math
from DataStructures import array_list as list

def encontrar_barrio(lat, lon, neighborhoods):
    """
    Retorna el nombre del barrio más cercano a las coordenadas dadas (lat, lon)
    según los centroides almacenados en la lista 'neighborhoods'.
    """

    # Si no hay barrios cargados, retornamos "Desconocido"
    if list.is_empty(neighborhoods):
        return "Desconocido"

    barrio_cercano = "Desconocido"
    distancia_minima = float("inf")

    # Recorremos todos los barrios de la lista
    for i in range(0, list.size(neighborhoods)):
        barrio = list.get_element(neighborhoods, i)
        try:
            lat_barrio = float(barrio["lat"])
            lon_barrio = float(barrio["lon"])
            nombre_barrio = barrio["neighborhood"]

            # Distancia euclidiana simple (no geodésica, pero suficiente para este reto)
            distancia = math.sqrt((lat - lat_barrio)**2 + (lon - lon_barrio)**2)

            if distancia < distancia_minima:
                distancia_minima = distancia
                barrio_cercano = nombre_barrio

        except Exception:
            # Si algún valor no se puede convertir, lo omitimos
            continue

    return barrio_cercano

def days_of_week(weekday_num):
    """
    Retorna el nombre del día de la semana según el número devuelto por datetime.weekday().
    0 = Lunes ... 6 = Domingo
    """
    dias = {
        0: "Lunes",
        1: "Martes",
        2: "Miércoles",
        3: "Jueves",
        4: "Viernes",
        5: "Sábado",
        6: "Domingo"
    }

    return dias.get(weekday_num, "Desconocido")

def sort_criteria(viaje1, viaje2):
        d1 = float(viaje1.get("trip_distance", 0))
        d2 = float(viaje2.get("trip_distance", 0))
        if d1 > d2:
            return True
        elif d1 == d2:
            return float(viaje1.get("total_amount", 0)) > float(viaje2.get("total_amount", 0))
        else:
            return False
        
def sort_horas(r1, r2):
    return int(r1["hora"]) < int(r2["hora"])