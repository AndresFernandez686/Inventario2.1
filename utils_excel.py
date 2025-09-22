import os
import pandas as pd
import shutil

def listar_archivos_excel(directorio="referencias"):
    """
    Lista todos los archivos Excel (.xlsx) disponibles en el directorio de referencias.
    
    Args:
        directorio (str): Ruta al directorio de referencias
        
    Returns:
        list: Lista con los nombres de los archivos Excel
    """
    archivos = []
    
    if os.path.exists(directorio) and os.path.isdir(directorio):
        for archivo in os.listdir(directorio):
            if archivo.endswith('.xlsx'):
                archivos.append(archivo)
    
    return archivos

def obtener_ruta_excel(nombre_archivo, directorio="referencias"):
    """
    Obtiene la ruta completa de un archivo Excel en el directorio de referencias.
    
    Args:
        nombre_archivo (str): Nombre del archivo Excel
        directorio (str): Directorio donde buscar
        
    Returns:
        str: Ruta completa al archivo o None si no existe
    """
    ruta = os.path.join(directorio, nombre_archivo)
    if os.path.exists(ruta):
        return ruta
    return None

def descargar_excel(nombre_archivo, ruta_destino, directorio="referencias"):
    """
    Descarga (copia) un archivo Excel de la carpeta referencias a la ubicación especificada.
    
    Args:
        nombre_archivo (str): Nombre del archivo a descargar
        ruta_destino (str): Ruta donde guardar el archivo
        directorio (str): Directorio de origen
        
    Returns:
        bool: True si la operación fue exitosa, False en caso contrario
    """
    ruta_origen = obtener_ruta_excel(nombre_archivo, directorio)
    
    if not ruta_origen:
        print(f"Error: El archivo {nombre_archivo} no existe en {directorio}")
        return False
    
    try:
        shutil.copy2(ruta_origen, ruta_destino)
        print(f"Archivo descargado exitosamente en: {ruta_destino}")
        return True
    except Exception as e:
        print(f"Error al descargar el archivo: {str(e)}")
        return False

def exportar_a_excel(datos, ruta_salida):
    """
    Exporta datos a un archivo Excel.
    
    Args:
        datos (pandas.DataFrame): DataFrame con los datos a exportar
        ruta_salida (str): Ruta donde guardar el archivo Excel
        
    Returns:
        bool: True si la exportación fue exitosa, False en caso contrario
    """
    try:
        datos.to_excel(ruta_salida, index=False)
        print(f"Datos exportados exitosamente a: {ruta_salida}")
        return True
    except Exception as e:
        print(f"Error al exportar a Excel: {str(e)}")
        return False
