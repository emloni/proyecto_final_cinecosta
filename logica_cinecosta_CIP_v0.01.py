import csv


class sala:
    def __init__(self, nombre_sala, tamaño):
        self.nombre_sala = nombre_sala
        
        if tamaño == 'A':
            self.filas, self.sillas_por_fila = 8, 10
        elif tamaño == 'B':
            self.filas, self.sillas_por_fila = 10, 12
        elif tamaño == 'C':
            self.filas, self.sillas_por_fila = 12, 14
        else:
            raise ValueError(f"Tamaño de sala '{tamaño}' inválido.")
        
        self.tamaño = (self.filas, self.sillas_por_fila)
        
class teatro:
    def __init__(self, nombre_teatro, ciudad):
        self.nombre_teatro = nombre_teatro
        self.ciudad = ciudad
        self.salas = [] # Agrupa las salas de este teatro
        
class empresa:
    def __init__(self, nombre_empresa):
        self.nombre_empresa = nombre_empresa
        self.teatros = []

    def leer_archivo(self, ruta_archivo):
        with open(ruta_archivo, mode="r", encoding="utf-8" ) as archivo:
            lector = csv.DictReader(archivo)
            for filas in lector:
                    nombre = filas["nombre_teatro"]
                    ciudad = filas["ciudad"]
                    
                    teatro_existe = False
                    
                    for t in self.teatros:
                        if t.nombre_teatro == nombre and t.ciudad == ciudad:
                            teatro_existe = True
                            break
                    if not teatro_existe:
                        self.teatros.append(teatro(nombre, ciudad)) 
