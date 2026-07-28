from logica_cinecosta import *
import csv
import numpy as np


print("=====================================================================")
print("     VERIFICADOR COMPLETO DE RUTAS Y REQUISITOS (HU-01 A HU-03)       ")
print("=====================================================================\n")

# Inicializamos el sistema principal
cinecosta = Empresa("Cinecosta")

# =====================================================================
# CAMINO 1: ÉXITO TOTAL (Carga perfecta y visualización de mapas)
# =====================================================================
print(">>> CAMINO 1: Verificación de Flujo Exitoso")

# 1. Cargar infraestructura y ocupación desde los archivos que creaste a mano
cinecosta.cargar_infraestructura_csv('teatros.csv')
cinecosta.cargar_ocupacion_mensual_csv('entradas_mes.csv', 'Teatro Centro', 'Barranquilla', 'Sala 1')

# 2. Acceso directo a la matriz NumPy para mostrar el mapa en consola
# Entramos a los diccionarios de la jerarquía: Empresa -> Teatro -> Sala -> Matriz NumPy
# CORRECCIÓN: Asegúrate de poner el nombre exacto del teatro, el guion (-) y la ciudad
sala_1 = cinecosta.teatros['Teatro Centro-Barranquilla'].salas['Sala 1']

print("\n[MAPA VISUAL NUMPY] Sala 1 (Teatro Centro):")
print(sala_1.mapa_ocupacion)


# 3. Ejecutar el cálculo estadístico de la HU-03
cinecosta.calcular_estadisticas_sala('Teatro Centro', 'Barranquilla', 'Sala 1')


print("\n" + "="*70 + "\n")


# =====================================================================
# CAMINO 2: VALIDACIÓN DE ERRORES DE INFRASTRUCTURA (HU-01)
# =====================================================================
print(">>> CAMINO 2: Prueba de Errores de Infraestructura (Requisitos 3, 4 y 6)")
print("Al cargar un archivo con fallas, el sistema informará en consola:")

# Forzar la lectura del archivo que contiene tamaños falsos o precios negativos
cinecosta.cargar_infraestructura_csv('infra_con_errores.csv')


print("\n" + "="*70 + "\n")


# =====================================================================
# CAMINO 3: VALIDACIÓN DE ERRORES EN ENTRADAS MENSUALES (HU-02)
# =====================================================================
print(">>> CAMINO 3: Prueba de Errores de Ocupación (Requisitos 2 y 5)")

print("\n[Sub-camino C1] Forzando registro en sala que NO existe en el sistema:")
cinecosta.cargar_ocupacion_mensual_csv('entradas_mes.csv', 'Teatro Falso', 'Bogota', 'Sala Fantasma')

print("\n[Sub-camino C2] Forzando ubicación fuera de los límites de la sala:")
# Forzar la lectura del archivo que tiene filas o sillas fuera de rango (como la Fila 99)
cinecosta.cargar_ocupacion_mensual_csv('entradas_limites.csv', 'Teatro Centro', 'Barranquilla', 'Sala 1')


print("\n" + "="*70 + "\n")


# =====================================================================
# CAMINO 4: VALIDACIÓN DE REQUISITO DE DESEMPATE (HU-03 - Criterio 6)
# =====================================================================
print(">>> CAMINO 4: Validación de Desempates Secuenciales en NumPy")
print("Si dos sillas tienen el mismo valor extremo (como el mínimo 0),")
print("NumPy seleccionará estrictamente la primera celda en el recorrido:")

cinecosta.calcular_estadisticas_sala('Teatro Centro', 'Barranquilla', 'Sala 1')

print("\n=====================================================================")
print("              TODAS LAS VALIDACIONES COMPLETADAS                     ")
print("=====================================================================")
