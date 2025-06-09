import time
from InquirerPy import inquirer
import threading
from ir import preprocess, seeker
from evaluation import evaluar_sistema

def animar_texto(texto, velocidad):
    """
    Imprime el texto en la consola con un efecto de animación.
    
    :param texto: El texto a animar.
    :param velocidad: La velocidad de la animación (en segundos entre caracteres).
    """
    for char in texto:
        print(char, end='', flush=True)
        time.sleep(velocidad)
    print()

def spinner(stop_event, start_message="Cargando...", end_message="Carga completa!"):
    """
    Muestra un spinner de carga en la consola hasta que stop_event esté activo.
    """
    spinner_chars = ['|', '/', '-', '\\']
    i = 0
    while not stop_event.is_set():
        print(f'\r{spinner_chars[i % len(spinner_chars)]} {start_message}', end='', flush=True)
        time.sleep(0.2)
        i += 1
    print()
    print(f'✅ {end_message}')

def menu_principal():
    """
    Muestra el menú principal de la aplicación.
    """
    opciones = [
        "Preprocesamiento",
        "Búsqueda",
        "Evaluación",
        "Salir"
    ]
    
    respuesta = inquirer.select(
        message="Seleccione una opción:",
        choices=opciones
    ).execute()
    
    return respuesta

def menu_preprocesamiento():
    """
    Muestra el menú de preprocesamiento.
    """
    while True:
        opciones = [
            "Preprocesar corpus",
            "Eliminar corpus preprocesado",
            "Volver al menú principal"
        ]
        respuesta = inquirer.select(
            message="Preprocesamiento:",
            choices=opciones
        ).execute()
        
        if respuesta == "Preprocesar corpus":
            stop_event = threading.Event()
            spinner_thread = threading.Thread(target=spinner, args=(stop_event, "Preprocesando corpus...", "Corpus preprocesado con éxito!"))
            spinner_thread.start()
            preprocess()
            stop_event.set()
            spinner_thread.join()
        elif respuesta == "Eliminar corpus preprocesado":
            stop_event = threading.Event()
            spinner_thread = threading.Thread(target=spinner, args=(stop_event, "Eliminando corpus preprocesado...", "Corpus eliminado!"))
            spinner_thread.start()
            try:
                import os
                os.remove("preprocessed.pkl")
            except FileNotFoundError:
                print("\r⚠️  No se encontró el archivo preprocesado.")
            stop_event.set()
            spinner_thread.join()
        elif respuesta == "Volver al menú principal":
            break

def menu_busqueda():
    """
    Muestra el menú de búsqueda.
    """
    while True:
        opciones = [
            "Ingresar consulta",
            "Volver al menú principal"
        ]
        respuesta = inquirer.select(
            message="Búsqueda:",
            choices=opciones
        ).execute()
        
        if respuesta == "Ingresar consulta":
            method = inquirer.select(
                message="Seleccione el método de búsqueda:",
                choices=["TF-IDF", "BM25"]
            ).execute()
            print(f"\r🔍 Método seleccionado: {method}")
            consulta = ingresar_consulta()
            stop_event = threading.Event()
            spinner_thread = threading.Thread(target=spinner, args=(stop_event, "Buscando documentos...", "Búsqueda completada!"))
            spinner_thread.start()
            seeker(consulta, method=method)
            stop_event.set()
            spinner_thread.join()
        elif respuesta == "Volver al menú principal":
            break

def menu_evaluacion():
    """
    Muestra el menú de evaluación.
    """
    opciones = [
        "Evaluar sistema",
        "Volver al menú principal"
    ]
    
    respuesta = inquirer.select(
        message="Evaluación:",
        choices=opciones
    ).execute()
    
    if respuesta == "Evaluar sistema":
        metodo = inquirer.select(
            message="Seleccione el método de evaluación:",
            choices=["TF-IDF", "BM25"]
        ).execute()
        stop_event = threading.Event()
        spinner_thread = threading.Thread(target=spinner, args=(stop_event, "Evaluando sistema...", "Evaluación completada!"))
        spinner_thread.start()
        evaluar_sistema(metodo=metodo)
        stop_event.set()
        spinner_thread.join()
    elif respuesta == "Volver al menú principal":
        return

def ingresar_consulta():
    """
    Solicita al usuario que ingrese una consulta de búsqueda.
    """
    consulta = inquirer.text(
        message="Ingrese su consulta de búsqueda:"
    ).execute()
    
    return consulta

def main():
    """Función principal.
    """
    texto = "🔍 SISTEMA DE BÚSQUEDA DE DOCUMENTOS 🔍"
    velocidad = 0.07
    animar_texto(texto, velocidad)
    print("🚀 Bienvenidos 🚀")

    while True:
        print("Menu principal:")
        opcion = menu_principal()
        if opcion == "Preprocesamiento":
            menu_preprocesamiento()
        elif opcion == "Búsqueda":
            menu_busqueda()
        elif opcion == "Evaluación":
            menu_evaluacion()
        elif opcion == "Salir":
            animar_texto("Saliendo del sistema. ¡Hasta luego!", 0.04)
            break

if __name__ == "__main__":
    main()