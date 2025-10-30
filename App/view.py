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
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    distancia_inicial = float(input("Ingrese la distancia mínima (en millas): "))
    distancia_final = float(input("Ingrese la distancia máxima (en millas): "))
    N = int(input("Ingrese el número de trayectos a mostrar al inicio y al final: "))

    result = logic.req_3(control, distancia_inicial, distancia_final, N)

    print("\n--- Resultado del Requerimiento 3 ---")
    print("Total de trayectos:", result["total_trayectos"])
    print("Tiempo de ejecución (ms):", result["tiempo_ms"])
    print("\nPrimeros trayectos:")
    print(result["primeros"])
    print("\nÚltimos trayectos:")
    print(result["ultimos"])


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
    # Solicitar parámetros al usuario
    fecha_terminacion = input("Fecha de terminación (YYYY-MM-DD): ")
    hora_terminacion = input("Hora de terminación (HH, 0-23): ")
    n = int(input("Número de horas a mostrar (N primeras y N últimas): "))

    # Convertir hora al formato requerido por req_5
    hora_formateada = f"{int(hora_terminacion):02d}:00:00"

    # ⚙️ En tu caso, control YA es la lista de viajes (lt)
    trips = control

    # Llamar al requerimiento 5 con la lista de viajes
    res = logic.req_5(trips, fecha_terminacion, hora_formateada, n)

    # Mostrar resultados generales
    print(f"\nTiempo de ejecución: {res['tiempo_ms']:.2f} ms")
    print(f"Total de trayectos encontrados: {res['total_trayectos']}\n")

    # Si no hay resultados o mensaje de error
    if "mensaje" in res:
        print(res["mensaje"])
        return

    if not res["primeros"]:
        print("No hay resultados para mostrar.")
        return

    # Encabezados de columnas según los datos de req_5
    headers = [
        "hora",
        "promedio_costo",
        "min_costo",
        "max_costo",
        "promedio_duracion",
        "min_duracion",
        "max_duracion"
    ]

    # Mostrar primeras horas
    print("Primeras horas:")
    primeros = [t for t in res["primeros"]["elements"]]
    primeros_tab = [[t.get(h, "") for h in headers] for t in primeros]
    print(tabulate(primeros_tab, headers=headers, tablefmt="grid", floatfmt=".2f"))

    # Mostrar últimas horas
    if res["ultimos"]:
        print("\nÚltimas horas:")
        ultimos = [t for t in res["ultimos"]["elements"]]
        ultimos_tab = [[t.get(h, "") for h in headers] for t in ultimos]
        print(tabulate(ultimos_tab, headers=headers, tablefmt="grid", floatfmt=".2f"))




def print_req_6(control):
    print("\n=== Requerimiento 6 ===")
    try:
        barrio = input("Ingrese el barrio de origen: ")
        hora_inicial = int(input("Ingrese la hora inicial (0-23): "))
        hora_final = int(input("Ingrese la hora final (0-23): "))
        n = int(input("Ingrese el número de elementos a mostrar: "))

        result = logic.req_6(control["model"]["catalog"]["trips"], control["model"]["catalog"]["neighborhoods"], barrio, hora_inicial, hora_final, n)

        if "mensaje" in result:
            print(result["mensaje"])
            return

        print(f"\nTotal de viajes: {result['total_viajes']}")
        print(f"Distancia promedio: {result['distancia_promedio']:.2f} km")
        print(f"Duración promedio: {result['duracion_promedio']:.2f} minutos")
        print(f"Barrio destino más visitado: {result['barrio_destino_mas_visitado']}")
        print(f"Método de pago más usado: {result['metodo_mas_usado']}")
        print(f"Método de pago con mayor recaudo: {result['metodo_mayor_recaudo']}")
        print(f"Tiempo de ejecución: {result['tiempo_ms']:.2f} ms")

        # Mostrar tabla con los primeros barrios destino
        print("\nTop barrios destino:")
        tabla = result["primeros"]["elements"]
        print(tabulate(tabla, headers="keys", tablefmt="grid", floatfmt=".2f"))

    except Exception as e:
        print("Error al ejecutar el requerimiento 6:", e)



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

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
