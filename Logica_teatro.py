import os
import csv
from datetime import datetime
import numpy as np

from sala import Sala

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

            
    def obtener_salas_por_tamano(self, tamano):
        tamano = tamano.upper()
 
        salas_filtradas = [sala for sala in self.salas if sala.tamano == tamano]

        return salas_filtradas

    def comparar_ingresos_por_tamano(self, tamano):
        
        salas = self.obtener_salas_por_tamano(tamano)

        if len(salas) < 2:
            raise ValueError(f"El teatro '{self.nombre}' no tiene al menos dos salas de "
                f"tamaño '{tamano}' con mapas de ingresos disponibles.")

        mapas = []
        for sala in salas:
            if not sala.ingresos_construidos:
                raise ValueError(
                    f"La sala '{sala.nombre}' no tiene mapa de ingresos construido."
                )
            mapas.append(sala.mapa_ingresos)

        estructura = np.array(mapas)  

        ingresos_totales_por_sala = {sala.nombre: float(mapa.sum()) for sala, mapa in zip(salas, mapas)}

        sala_mayor_ingreso = max(ingresos_totales_por_sala, key=ingresos_totales_por_sala.get)

        mapa_promedio = estructura.mean(axis=0)

        return {
            "estructura": estructura,
            "ingresos_totales_por_sala": ingresos_totales_por_sala,
            "sala_mayor_ingreso": sala_mayor_ingreso,
            "mapa_ingresos_promedio": mapa_promedio,
        }

    def ocupacion_promedio(self):
        if not self.salas:
            raise ValueError(f"El teatro '{self.nombre}' no tiene salas registradas.")

        suma_total = 0
        total_sillas = 0

        for sala in self.salas:
            if not sala.ocupacion_construida:
                raise ValueError(
                    f"La sala '{sala.nombre}' no tiene mapa de ocupación construido."
                )
            suma_total += sala.mapa_ocupacion.sum()
            total_sillas += sala.mapa_ocupacion.size

        return round(float(suma_total / total_sillas), 2)

    def ingreso_promedio(self):
        if not self.salas:
            raise ValueError(f"El teatro '{self.nombre}' no tiene salas registradas.")

        suma_total = 0
        total_sillas = 0

        for sala in self.salas:
            if not sala.ingresos_construidos:
                raise ValueError(
                    f"La sala '{sala.nombre}' no tiene mapa de ingresos construido."
                )
            suma_total += sala.mapa_ingresos.sum()
            total_sillas += sala.mapa_ingresos.size

        return round(float(suma_total / total_sillas), 2)
