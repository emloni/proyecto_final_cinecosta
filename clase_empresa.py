from logica_cinecosta_CIP import Teatro,Sala
import csv

class Empresa:
    def __init__(self, nombre_empresa):
        self.nombre_empresa = nombre_empresa
        self.lectura_archivo = None
        self.teatros = []
        

    def leer_archivo(self, ruta_archivo):
        with open(ruta_archivo, mode="r", encoding="utf-8" ) as archivo:
            lector = csv.DictReader(archivo)
            self.lectura_archivo = list(lector)
    
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