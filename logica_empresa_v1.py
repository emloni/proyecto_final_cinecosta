from clase_teatro import Teatro
from sala import Sala
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
 
    def desempeno_por_teatro(self):
        if not self.teatros:
            raise ValueError(
                f"La empresa '{self.nombre_empresa}' no tiene teatros registrados."
            )
 
        desempeno = {}
 
        for teatro in self.teatros:
            try:
                ocupacion = teatro.ocupacion_promedio()
                ingreso = teatro.ingreso_promedio()
            except ValueError as error:
                raise ValueError(
                    f"El teatro '{teatro.nombre}' no tiene mapas construidos para todas sus salas: {error}"
                )
 
            desempeno[teatro.nombre] = {
                "ocupacion_promedio": ocupacion,
                "ingreso_promedio": ingreso,
            }
 
        return desempeno
 
    def teatros_con_mejor_desempeno(self):
        desempeno = self.desempeno_por_teatro()
 
        nombre_mayor_ocupacion = max(
            desempeno, key=lambda nombre: desempeno[nombre]["ocupacion_promedio"]
        )
        nombre_mayor_ingreso = max(
            desempeno, key=lambda nombre: desempeno[nombre]["ingreso_promedio"]
        )
 
        return {
            "desempeno_por_teatro": desempeno,
            "teatro_mayor_ocupacion": (
                nombre_mayor_ocupacion,
                desempeno[nombre_mayor_ocupacion]["ocupacion_promedio"],
            ),
            "teatro_mayor_ingreso": (
                nombre_mayor_ingreso,
                desempeno[nombre_mayor_ingreso]["ingreso_promedio"],
            ),
        }
