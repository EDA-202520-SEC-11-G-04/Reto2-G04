import sys
from tabulate import tabulate
import App.logic as logic
from datetime import datetime

def new_logic():
    """
        Se crea una instancia del controlador
    """
    return logic.new_logic()
    

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Carga los datos
    """
    
    filename = input("Indiquez le chemin du fichier CSV: ")
    control = logic.load_data(control, filename)
    
    if control and "elements" in control:
        elements = control["elements"]

        filtered_data = []
        sample = elements[:5] + elements[-5:]
        for t in sample:
            start_str = t.get("pickup_datetime", "")
            end_str = t.get("dropoff_datetime", "")
            duration = ""

            # Calcul de la durée si les deux dates sont présentes et valides
            try:
                start = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
                end = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
                duration = round((end - start).total_seconds() / 60, 2)
            except:
                pass  # si une date est invalide, on laisse la durée vide

            filtered_data.append({
                "Inicio": start_str,
                "Fin": end_str,
                "Duración (min)": duration,
                "Distancia (mi)": t.get("trip_distance", ""),
                "Costo total ($)": t.get("total_amount", "")
            })

        print("\nPrimeros 5 trayectos:")
        print(tabulate(filtered_data[:5], headers="keys", tablefmt="grid", showindex=True))

        print("\nÚltimos 5 trayectos:")
        print(tabulate(filtered_data[-5:], headers="keys", tablefmt="grid", showindex=True))

    return control
   


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    return logic.get_data(control,id)

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    fecha_ini=input("fecha inicial del filtro (YYYY-MM-DD HH:MM:SS) :")
    fecha_fin=input("fecha final del filtro (YYYY-MM-DD HH:MM:SS) :")
    N=int(input("N primeros y N últimos : "))
    res=logic.req_1(control,fecha_ini, fecha_fin, N)
    
    print(f"\n Tiempo de ejecución: {res['tiempo_ejecucion_ms']:.2f} ms")
    print(f"Total de trayectos encontrados: {res['total_trayectos']}\n")

    if "mensaje" in res:
        print(res["mensaje"])
        return

    # Si no trayecto
    if not res["primeros"]:
        print("No hay trayectos para mostrar.")
        return

    # Construire les tableaux pour tabulate
    headers = ["Inicio", "Fin", "Duración (min)", "Distancia (mi)", "Costo total ($)"]

    print("Primeros trayectos:")
    print(tabulate(res["primeros"], headers="keys", tablefmt="grid", floatfmt=".2f"))

    if res["ultimos"]:
        print("\n Últimos trayectos:")
        print(tabulate(res["ultimos"], headers="keys", tablefmt="grid", floatfmt=".2f"))


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    distancia_inicial = float(input("Distancia mínima (millas): "))
    distancia_final = float(input("Distancia máxima (millas): "))
    n = int(input("Número de trayectos a mostrar (N primeros y N últimos): "))

    trips = control

    res = logic.req_3(trips, distancia_inicial, distancia_final, n)

    print(f"\nTiempo de ejecución: {res['tiempo_ms']:.2f} ms")
    print(f"Total de trayectos encontrados: {res['total_trayectos']}\n")

    if "mensaje" in res:
        print(res["mensaje"])
        return

    if not res["primeros"]:
        print("No hay trayectos para mostrar.")
        return

    headers = [
        "pickup_datetime", "dropoff_datetime", "trip_distance",
        "total_amount", "pickup_longitude", "pickup_latitude",
        "dropoff_longitude", "dropoff_latitude"
    ]

    print("Primeros trayectos:")
    primeros = [t for t in res["primeros"]["elements"]]
    primeros_tab = [[t.get(h, "") for h in headers] for t in primeros]
    print(tabulate(primeros_tab, headers=headers, tablefmt="grid", floatfmt=".2f"))

    if res["ultimos"]:
        print("\nÚltimos trayectos:")
        ultimos = [t for t in res["ultimos"]["elements"]]
        ultimos_tab = [[t.get(h, "") for h in headers] for t in ultimos]
        print(tabulate(ultimos_tab, headers=headers, tablefmt="grid", floatfmt=".2f"))



def print_req_4(control):
    fecha_terminacion = input("Fecha de terminación (YYYY-MM-DD): ")
    momento = input("Momento ('ANTES' o 'DESPUES'): ").upper()
    tiempo_ref = input("Hora de referencia (HH:MM:SS): ")
    n = int(input("Número de trayectos a mostrar (N primeros y N últimos): "))

    res = logic.req_4(control, fecha_terminacion, momento, tiempo_ref, n)

    print(f"\nTiempo de ejecución: {res['tiempo_ms']:.2f} ms")
    print(f"Total de trayectos encontrados: {res['total_trayectos']}\n")

    if "mensaje" in res:
        print(res["mensaje"])
        return

    if not res["primeros"]:
        print("No hay trayectos para mostrar.")
        return

    # ✅ Colonnes à afficher
    headers = [
        "pickup_datetime", "pickup_longitude", "pickup_latitude",
        "dropoff_datetime", "dropoff_longitude", "dropoff_latitude",
        "trip_distance", "total_amount"
    ]

    print("Primeros trayectos:")
    primeros = [t for t in res["primeros"]["elements"]]
    primeros_tab = [[t.get(h, "") for h in headers] for t in primeros]
    print(tabulate(primeros_tab, headers=headers, tablefmt="grid", floatfmt=".2f"))

    if res["ultimos"]:
        print("\nÚltimos trayectos:")
        ultimos = [t for t in res["ultimos"]["elements"]]
        ultimos_tab = [[t.get(h, "") for h in headers] for t in ultimos]
        print(tabulate(ultimos_tab, headers=headers, tablefmt="grid", floatfmt=".2f"))



def print_req_5(control):
    fecha_terminacion = input("Fecha de terminación (YYYY-MM-DD): ")
    hora_terminacion = input("Hora de terminación (HH, 0-23): ")
    n = int(input("Número de horas a mostrar (N primeras y N últimas): "))

    hora_formateada = f"{int(hora_terminacion):02d}:00:00"

    trips = control

    res = logic.req_5(trips, fecha_terminacion, hora_formateada, n)

    print(f"\nTiempo de ejecución: {res['tiempo_ms']:.2f} ms")
    print(f"Total de trayectos encontrados: {res['total_trayectos']}\n")

    if "mensaje" in res:
        print(res["mensaje"])
        return

    if not res["primeros"]:
        print("No hay resultados para mostrar.")
        return

    headers = [
        "hora",
        "promedio_costo",
        "min_costo",
        "max_costo",
        "promedio_duracion",
        "min_duracion",
        "max_duracion"
    ]

    # Primeras horas
    print("Primeras horas:")
    primeros = [t for t in res["primeros"]["elements"]]
    primeros_tab = [[t.get(h, "") for h in headers] for t in primeros]
    print(tabulate(primeros_tab, headers=headers, tablefmt="grid", floatfmt=".2f"))

    # Ultimas horas
    if res["ultimos"]:
        print("\nÚltimas horas:")
        ultimos = [t for t in res["ultimos"]["elements"]]
        ultimos_tab = [[t.get(h, "") for h in headers] for t in ultimos]
        print(tabulate(ultimos_tab, headers=headers, tablefmt="grid", floatfmt=".2f"))


def print_req_6(control):
    """Imprime los resultados del requerimiento 6"""

    hora_inicial = input("Hora inicial (HH, 0-23): ")
    hora_final = input("Hora final (HH, 0-23): ")
    barrio = input("Barrio de inicio: ").strip()
    n = int(input("Número de trayectos a mostrar (N primeros y N últimos): "))

    hora_inicial_str = f"{int(hora_inicial):02d}:00:00"
    hora_final_str = f"{int(hora_final):02d}:00:00"

    trips = control 

    try:
        res = logic.req_6(trips, hora_inicial_str, hora_final_str, barrio, n)
    except Exception as e:
        print(f"Error al ejecutar el requerimiento 6: {e}")
        return

    if "mensaje" in res:
        print(res["mensaje"])
        return

    print(f"\nTiempo de ejecución: {res['tiempo_ms']:.2f} ms")
    print(f"Total de trayectos encontrados: {res['total_trayectos']}\n")


    print(f"Barrio de inicio: {barrio}")
    print(f"Barrio destino más visitado: {res['barrio_destino_mas_visitado']}")
    print(f"Distancia promedio: {res['distancia_promedio']:.2f} millas")
    print(f"Duración promedio: {res['duracion_promedio']:.2f} minutos")
    print(f"Método de pago más usado: {res['metodo_mas_usado']}")
    print(f"Método con mayor recaudo: {res['metodo_mayor_recaudo']}\n")


    print("Destinos más visitados:")
    destinos = [t for t in res["primeros"]["elements"]]
    if not destinos:
        print("No hay destinos para mostrar.")
        return

    headers = ["barrio_destino", "cantidad"]
    destinos_tab = [[t.get(h, "") for h in headers] for t in destinos]
    print(tabulate(destinos_tab, headers=headers, tablefmt="grid", floatfmt=".0f"))






# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 6:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
