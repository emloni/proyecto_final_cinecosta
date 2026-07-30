import csv
import os
import numpy as np


class Sala:
    def __init__(self, nombre, tamano, precio_base):
        self.nombre = nombre
        self.tamano = tamano.upper()
        self.precio_base = float(precio_base)

        if self.precio_base <= 0:
            raise ValueError(f"El precio base debe ser mayor que cero (sala '{self.nombre}').")

        if self.tamano == 'A':
            self.filas, self.sillas_por_fila = 8, 10
        elif self.tamano == 'B':
            self.filas, self.sillas_por_fila = 10, 12
        elif self.tamano == 'C':
            self.filas, self.sillas_por_fila = 12, 14
        else:
            raise ValueError(f"Tamaño de sala '{tamano}' inválido. Debe ser A, B o C.")

        self.mapa_ocupacion = np.zeros((self.filas, self.sillas_por_fila), dtype=int)
        self.mapa_ingresos = np.zeros((self.filas, self.sillas_por_fila), dtype=float)
        self.mapa_zonas = self._generar_mapa_zonas()
        self.ocupacion_construida = False
        self.ingresos_construidos = False

    # ------------------------------------------------------------------
    # HU-Cinecosta-01 (parte de sala): distribución de zonas por tamaño
    # ------------------------------------------------------------------
    def _generar_mapa_zonas(self):
        """
        Asigna la zona de cada silla según el ESQUEMA por fila completa
        definido en el enunciado (no depende de la columna):

          A (8 filas):  E=1-3   P=4-5   I=6-7    U=8
          B (10 filas): E=1-4   P=5-6   I=7-9    U=10
          C (12 filas): E=1-5   P=6-7   I=8-11   U=12
        """
        rangos_por_tamano = {
            'A': {'E': (0, 3), 'P': (3, 5), 'I': (5, 7), 'U': (7, 8)},
            'B': {'E': (0, 4), 'P': (4, 6), 'I': (6, 9), 'U': (9, 10)},
            'C': {'E': (0, 5), 'P': (5, 7), 'I': (7, 11), 'U': (11, 12)},
        }
        rangos = rangos_por_tamano[self.tamano]

        zonas = np.empty((self.filas, self.sillas_por_fila), dtype='<U1')
        for zona, (inicio, fin) in rangos.items():
            zonas[inicio:fin, :] = zona
        return zonas

    # ------------------------------------------------------------------
    # HU-Cinecosta-02: mapa de ocupación mensual desde CSV
    # ------------------------------------------------------------------
    def cargar_ocupacion(self, ruta_csv):
        """
        Cada registro del CSV trae 9 campos, en este orden:
        teatro, sala, fecha, numero_funcion, hora, fila, silla, edad, sexo
        (sin encabezado). Acumula 1 por cada vez que aparece la silla.
        """
        if not os.path.exists(ruta_csv):
            raise FileNotFoundError(
                f"No se encontró el archivo de entradas vendidas en la ruta: {ruta_csv}"
            )

        registros_invalidos = []

        with open(ruta_csv, newline='', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            for numero_linea, fila_csv in enumerate(lector, start=1):
                if not fila_csv:
                    continue
                try:
                    fila = int(fila_csv[5])
                    silla = int(fila_csv[6])
                except (IndexError, ValueError):
                    registros_invalidos.append((numero_linea, fila_csv))
                    continue

                fila_idx = fila - 1
                silla_idx = silla - 1

                if not (0 <= fila_idx < self.filas) or not (0 <= silla_idx < self.sillas_por_fila):
                    registros_invalidos.append((numero_linea, fila_csv))
                    continue

                self.mapa_ocupacion[fila_idx, silla_idx] += 1

        if registros_invalidos:
            print(f"Se encontraron {len(registros_invalidos)} registro(s) inválidos "
                  f"en '{ruta_csv}' (fila o silla fuera de rango):")
            for numero_linea, fila_csv in registros_invalidos:
                print(f"  Línea {numero_linea}: {fila_csv}")

        self.ocupacion_construida = True
        return self.mapa_ocupacion

    # ------------------------------------------------------------------
    # HU-Cinecosta-03: estadísticos del mapa de ocupación
    # ------------------------------------------------------------------
    def estadisticos_ocupacion(self):
        if not self.ocupacion_construida:
            raise ValueError("El mapa de ocupación mensual debe construirse antes de calcular estadísticos.")

        mapa = self.mapa_ocupacion
        promedio = round(float(np.mean(mapa)), 2)
        desviacion = round(float(np.std(mapa)), 2)

        idx_max = np.unravel_index(np.argmax(mapa), mapa.shape)
        idx_min = np.unravel_index(np.argmin(mapa), mapa.shape)

        return {
            'promedio': promedio,
            'desviacion_estandar': desviacion,
            'maximo': int(mapa[idx_max]),
            'silla_maxima': (int(idx_max[0]) + 1, int(idx_max[1]) + 1),  # (fila, silla) en base 1
            'minimo': int(mapa[idx_min]),
            'silla_minima': (int(idx_min[0]) + 1, int(idx_min[1]) + 1),
        }

    # ------------------------------------------------------------------
    # HU-Cinecosta-04: mapa de ingresos
    # ------------------------------------------------------------------
    def precios_por_asiento(self, factores_zona):
        precios = np.zeros((self.filas, self.sillas_por_fila), dtype=float)
        for zona, factor in factores_zona.items():
            precios[self.mapa_zonas == zona] = self.precio_base * float(factor)
        return precios

    def construir_mapa_ingresos(self, factores_zona):
        if not self.ocupacion_construida:
            raise ValueError("El mapa de ocupación mensual debe construirse antes de calcular los ingresos.")

        precios = self.precios_por_asiento(factores_zona)
        if precios.shape != self.mapa_ocupacion.shape:
            raise ValueError("Las dimensiones del mapa de ingresos deben coincidir exactamente con las del mapa de ocupación.")

        self.mapa_ingresos = self.mapa_ocupacion.astype(float) * precios
        self.ingresos_construidos = True
        return self.mapa_ingresos
