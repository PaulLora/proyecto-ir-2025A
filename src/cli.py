import time
from InquirerPy import inquirer
import threading

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

def spinner():
    """
    Muestra un spinner de carga en la consola.
    """
    spinner_chars = ['|', '/', '-', '\\']
    for i in range(10):  # Muestra el spinner por 10 iteraciones
        print(f'\r{spinner_chars[i % len(spinner_chars)]} Cargando...', end='', flush=True)
        time.sleep(0.2)
    print('\r✅ Carga completa!')  # Limpia la línea al final

def menu_principal():
    """
    Muestra el menú principal de la aplicación.
    """
    opciones = [
        "Realizar búsqueda",
        "Nueva búsqueda",
        "Salir"
    ]
    
    respuesta = inquirer.select(
        message="Seleccione una opción:",
        choices=opciones
    ).execute()
    
    return respuesta

def ingresar_consulta():
    """
    Solicita al usuario que ingrese una consulta de búsqueda.
    """
    consulta = inquirer.text(
        message="Ingrese su consulta de búsqueda:"
    ).execute()
    
    return consulta

def buscar_documentos(documentos, consulta):
    # Simula una búsqueda que toma tiempo
    resultados = [doc for doc in documentos if consulta.lower() in doc.lower()]
    time.sleep(1.5)  # Simula tiempo de búsqueda
    return resultados

def preprocesar_documentos():
    # Simulación de documentos preprocesados
    return [
        "Este es un documento de Python. Python es un lenguaje de programación muy popular...",
        "Manual de usuario: Para instalar el software, siga estos pasos...",
        "Resumen de datos: Los datos muestran que Python es ampliamente usado...",
        "Guía de instalación: Instale Python desde la página oficial..."
    ]

def obtener_fragmento(documento, consulta):
    """
    Obtiene un fragmento del documento que contiene la consulta.
    
    :param documento: El documento completo.
    :param consulta: La consulta de búsqueda.
    :return: Un fragmento del documento que contiene la consulta.
    """
    if consulta.lower() in documento.lower():
        inicio = documento.lower().index(consulta.lower())
        fin = inicio + len(consulta)
        return documento[max(0, inicio - 30):min(len(documento), fin + 30)]
    return ""

def tarea_busqueda(documentos, consulta, resultados_ref):
    resultados_ref[0] = buscar_documentos(documentos, consulta)

def main():
    """Función principal.
    """
    texto = "🔍 SISTEMA DE BÚSQUEDA DE DOCUMENTOS 🔍"
    velocidad = 0.07
    animar_texto(texto, velocidad)
    print("🚀 Bienvenidos 🚀")

    documentos = preprocesar_documentos()

    while True:
        opcion = menu_principal()        
        if opcion in ["Realizar búsqueda", "Nueva búsqueda"]:
            consulta = ingresar_consulta()
            print(f"🔎 Buscando documentos para: {consulta} ⏳")

            resultados = [None]
            hilo = threading.Thread(target=tarea_busqueda, args=(documentos, consulta, resultados))
            hilo.start()
            while hilo.is_alive():
                spinner()
            hilo.join()

            if resultados[0]:
                print("📄 Documentos encontrados:")
                opciones = [
                    {
                        "name": obtener_fragmento(doc, consulta),  # Lo que se muestra
                        "value": doc                               # El documento completo
                    }
                    for doc in resultados[0]
                ]
                seleccion = inquirer.select(
                    message="Seleccione un documento para ver detalles:",
                    choices=opciones
                ).execute()
                print(f"📝 Seleccionó: {seleccion}")
            else:
                print("❌ No se encontraron documentos.")
        elif opcion == "Salir":
            animar_texto("Saliendo del sistema. ¡Hasta luego!", 0.04)
            break

if __name__ == "__main__":
    main()