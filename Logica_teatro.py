import os
import csv
from datetime import datetime
import numpy as np

from sala import Sala


def cargar_archivo_csv(ruta_archivo):
    verificar_archivo_existe(ruta_archivo)

    with open(ruta_archivo, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)


def verificar_archivo_existe(ruta):
    if not os.path.exists(ruta):
        raise FileNotFoundError(
            f"El archivo '{ruta}' no existe."
        )


class Teatro:

    def __init__(self, nombre, ciudad):

        self.nombre = nombre
        self.ciudad = ciudad
        self.salas = []

    def agregar_sala(self, sala):

        if not isinstance(sala, Sala):
            raise TypeError("Error: la sala debe ser de tipo Sala")

        if self.buscar_sala(sala.nombre) is not None:
            raise ValueError("La sala ya fue agregada")

        self.salas.append(sala)


    def buscar_sala(self, nombre_sala):

        for sala in self.salas:

            if sala.nombre == nombre_sala:
                return sala

        return None