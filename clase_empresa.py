from sala_HU_4 import Sala
from Logica_teatro import Teatro
import csv

class Empresa:
    def __init__(self, nombre):
        self.nombre = nombre
        self.regristros = None
        self.teatros = []
        

    def leer_archivo(self, ruta_archivo):
        try:
            with open(ruta_archivo, mode="r", encoding="utf-8" ) as archivo:
                lector = csv.DictReader(archivo)
                self.lectura_archivo = list(lector)
        except OSError:
            raise FileNotFoundError("No se pudo abrir el archivo.")
        except ValueError:
            raise ValueError("Archivo con formato no válido.")

    
    def agregar_teatro(self):
        for fila in self.lectura_archivo:
            nombre = fila["nombre_teatro"]
            ciudad = fila["ciudad"]
            
            teatro_existe = False
            
            for t in self.teatros:
                if t.nombre_teatro == nombre and t.ciudad == ciudad:
                    teatro_existe = True
                    break
            if not teatro_existe:
                self.teatros.append(Teatro(nombre, ciudad))

    def cargar_salas(self):
        for fila in self.lectura_archivo:
            nombre_teatro = fila["nombre_teatro"]
            nombre_sala = fila["nombre_sala"]
            tamaño_sala = fila["tamaño_sala"]
            precio_base = fila["precio_base"]
                
            if precio_base <= 0:
                raise ValueError("el precio base debe ser un valor numerico mayor a cero")
            for t in self.teatros:
                if t.nombre_teatro == nombre_teatro:
                    t.salas.append(Sala(nombre_sala, tamaño_sala, precio_base))