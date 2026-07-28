import csv
import numpy as np

class Sala:
    def __init__(self, nombre, tamano, precio_base):
        self.nombre = nombre
        self.tamano = tamano.upper()
        self.precio_base = float(precio_base)
        
        # [HU-01] Dimensiones estrictas por tipo de sala (Páginas 1 y 2)
        if self.tamano == 'A':
            self.filas, self.sillas_por_fila = 8, 10
        elif self.tamano == 'B':
            self.filas, self.sillas_por_fila = 10, 12
        elif self.tamano == 'C':
            self.filas, self.sillas_por_fila = 12, 14
        else:
            raise ValueError(f"Tamaño de sala '{tamano}' inválido.")
            
        # [HU-02] Inicializar el mapa de ocupación mensual con ceros usando NumPy
        self.mapa_ocupacion = np.zeros((self.filas, self.sillas_por_fila), dtype=int)

class Teatro:
    def __init__(self, nombre, city):
        self.nombre = nombre
        self.city = city
        self.salas = {} # Agrupa las salas de este teatro

class Empresa:
    def __init__(self, nombre):
        self.nombre = nombre
        self.teatros = {} # Jerarquía superior: Agrupa los teatros

    # =========================================================================
    # HU-01: CARGAR INFRAESTRUCTURA DE LA EMPRESA
    # =========================================================================
    def cargar_infraestructura_csv(self, ruta_archivo):
        try:
            with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                next(lector) # Saltar fila de encabezados
                
                for num_fila, fila in enumerate(lector, start=2):
                    try:
                        teatro_nom = fila[0].strip()
                        ciudad = fila[1].strip()
                        sala_nom = fila[2].strip()
                        tamano = fila[3].strip().upper()
                        precio_base = float(fila[4])
                        
                        if tamano not in ['A', 'B', 'C']:
                            raise ValueError(f"Tamaño '{tamano}' inválido.")
                        if precio_base <= 0:
                            raise ValueError("El precio base debe ser mayor a cero.")
                            
                        id_teatro = f"{teatro_nom}-{ciudad}"
                        if id_teatro not in self.teatros:
                            self.teatros[id_teatro] = Teatro(teatro_nom, ciudad)
                            
                        self.teatros[id_teatro].salas[sala_nom] = Sala(sala_nom, tamano, precio_base)
                    except (ValueError, IndexError) as e:
                        print(f"[REPORTE HU-01] Registro inválido en Fila {num_fila}: {e}")
            print(f">> Estructura de la empresa '{self.nombre}' cargada.")
        except FileNotFoundError:
            print(f"[REPORTE HU-01] El archivo '{ruta_archivo}' no existe.")

    # =========================================================================
    # HU-02: CONSTRUIR MAPA DE OCUPACIÓN MENSUAL¿
    # =========================================================================
    def cargar_ocupacion_mensual_csv(self, ruta_archivo, teatro_nom, ciudad, sala_nom):
        id_teatro = f"{teatro_nom}-{ciudad}"
        
        # Criterio de Aceptación 2: Validar si la sala existe previamente en la empresa
        if id_teatro not in self.teatros or sala_nom not in self.teatros[id_teatro].salas:
            print(f"[REPORTE HU-02] Error: La sala '{sala_nom}' no está en la infraestructura.")
            return
            
        sala = self.teatros[id_teatro].salas[sala_nom]
        
        try:
            with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                next(lector) # Saltar fila de encabezados
                
                for num_fila, fila in enumerate(lector, start=2):
                    try:
                        # Mapeo posicional de las 9 columnas del archivo de entradas
                        csv_teatro = fila[0].strip()
                        csv_sala = fila[1].strip()
                        # Nota: Las columnas 2, 3, 4, 7 y 8 corresponden a fecha, consecutivo, hora, edad y sexo.
                        # No modifican la matriz directamente, pero se leen de forma implícita.
                        
                        # Filtramos únicamente los registros asociados a este teatro y sala específicos
                        if csv_teatro == teatro_nom and csv_sala == sala_nom:
                            # Ajuste de índices: De base 1 (CSV) a base 0 (Matriz NumPy)
                            f_idx = int(fila[5]) - 1
                            s_idx = int(fila[6]) - 1
                            
                            # Criterio de Aceptación 5: Validar que esté dentro de las dimensiones de la sala
                            if 0 <= f_idx < sala.filas and 0 <= s_idx < sala.sillas_por_fila:
                                sala.mapa_ocupacion[f_idx, s_idx] += 1
                            else:
                                print(f"[REPORTE HU-02] Fila {num_fila}: Asiento [Fila {f_idx+1}, Silla {s_idx+1}] fuera de rango.")
                    except (ValueError, IndexError) as e:
                        print(f"[REPORTE HU-02] Registro corrupto o incompleto en Fila {num_fila}: {e}")
            print(f">> Mapa de ocupación mensual generado para {sala_nom}.")
        except FileNotFoundError:
            print(f"[REPORTE HU-02] El archivo '{ruta_archivo}' no existe.")

    # =========================================================================
    # HU-03: CALCULAR ESTADÍSTICOS DESCRIPTIVOS
    # =========================================================================
    def calcular_estadisticas_sala(self, teatro_nom, ciudad, sala_nom):
        id_teatro = f"{teatro_nom}-{ciudad}"
        if id_teatro not in self.teatros or sala_nom not in self.teatros[id_teatro].salas:
            print("[REPORTE HU-03] Sala no encontrada.")
            return

        sala = self.teatros[id_teatro].salas[sala_nom]
        mapa = sala.mapa_ocupacion # Matriz NumPy
        
        # Cálculos directos usando NumPy (Criterios 2, 3, 4 y 5)
        promedio = np.mean(mapa)
        desviacion = np.std(mapa)
        max_ocupacion = np.max(mapa)
        min_ocupacion = np.min(mapa)
        
        # Criterio de Aceptación 6: Desempate por primera ocurrencia secuencial usando argwhere
        pos_max = np.argwhere(mapa == max_ocupacion)[0] + 1
        pos_min = np.argwhere(mapa == min_ocupacion)[0] + 1

        print(f"\n================ METRICAS DE OPERACIÓN: {sala_nom} ================")
        print(f"Ocupación Promedio por Silla: {promedio:.2f}")
        print(f"Desviación Estándar:           {desviacion:.2f}")
        print(f"Ocupación Máxima:              {max_ocupacion} en (Fila {pos_max[0]}, Silla {pos_max[1]})")
        print(f"Ocupación Mínima:              {min_ocupacion} en (Fila {pos_min[0]}, Silla {pos_min[1]})")
        print("===============================================================")
