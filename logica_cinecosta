import os
import csv
from datetime import datetime
import numpy as np

def cargar_archivo_csv(ruta_archivo):
    verificar_archivo_existe(ruta_archivo)

    with open(ruta_archivo, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)


def verificar_archivo_existe(ruta):
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"El archivo '{ruta}' no existe.")

TIPOS_DE_SALA = {"A" : {"filas" : 8, "sillas" : 10},
                 "B" : {"filas" : 10, "sillas" : 12},
                 "C" : {"filas" : 12, "sillas" : 14}}

class Sala:
    def __init__(self, nombre, tamano, precio_base):
        self.nombre = nombre
        self.tamano = tamano
        self.precio_base = precio_base
        self.filas = TIPOS_DE_SALA[tamano]["filas"]
        self.sillas = TIPOS_DE_SALA[tamano]["sillas"]
    
    def __init__(self, tipo_sala):
        if tipo_sala not in TIPOS_DE_SALA:
            
            raise ValueError(f"tipo de sala invalido: {tipo_sala}. Debe ser uno de {list(TIPOS_DE_SALA.keys())}.")
    try:
        precio_base = float(precio_base)
    except (TypeError, ValueError):
        raise ValueError("El precio base debe ser un valor numérico.")

    if precio_base <= 0:
        raise ValueError("El precio base debe ser mayor que cero.")
    


class teatro:
    def __init__(self, nombre, ciudad):
        self.nombre = nombre
        self.ciudad = ciudad
        self.salas = {}
        
        def agregar_sala(self,sala):
            if sala.nombre in self.salas:
                raise ValueError(f"La sala '{sala.nombre}' ya está registrada en el teatro '{self.nombre}'.")
            self.salas.append(sala)
