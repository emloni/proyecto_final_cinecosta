import os
from logica_cinecosta import Empresa

# 1. Inicializar la empresa globalmente para la sesión
cinecosta = Empresa("Cinecosta S.A.")

# Variable para controlar el bucle del menú
continuar = True

while continuar:
    # Dibujar el menú en la consola
    print("\n=======================================================")
    print("      SISTEMA DE GESTIÓN OPERATIVA - CINECOSTA          ")
    print("=======================================================")
    print(" 1. [HU-01] Cargar Infraestructura (Teatros y Salas)")
    print(" 2. [HU-02] Cargar Ocupación Mensual (Archivo de Entradas)")
    print(" 3. [HU-03] Calcular Estadísticas de una Sala")
    print(" 4. [EXTRA] Ver Mapa Visual de Ocupación (NumPy)")
    print(" 5. Salir del Programa")
    print("=======================================================")
    
    opcion = input("Seleccione una opción (1-5): ").strip()
    
    # -----------------------------------------------------------------
    # OPCIÓN 1: Cargar Infraestructura
    # -----------------------------------------------------------------
    if opcion == "1":
        print("\n--- [HU-01] CARGA DE INFRAESTRUCTURA ---")
        archivo = input("Ingrese el nombre/ruta del archivo CSV (ej: infraestructura.csv): ").strip()
        cinecosta.cargar_infraestructura_csv(archivo)
        
    # -----------------------------------------------------------------
    # OPCIÓN 2: Cargar Ocupación Mensual
    # -----------------------------------------------------------------
    elif opcion == "2":
        print("\n--- [HU-02] CARGA DE ENTRADAS MENSUALES ---")
        archivo = input("Ingrese el nombre/ruta del archivo CSV (ej: entradas_mes.csv): ").strip()
        teatro = input("Nombre del Teatro: ").strip()
        ciudad = input("Ciudad del Teatro: ").strip()
        sala = input("Nombre de la Sala (ej: Sala 1): ").strip()
        
        cinecosta.cargar_ocupacion_mensual_csv(archivo, teatro, ciudad, sala)
        
    # -----------------------------------------------------------------
    # OPCIÓN 3: Calcular Estadísticas descriptivas
    # -----------------------------------------------------------------
    elif opcion == "3":
        print("\n--- [HU-03] ESTADÍSTICAS DE LA SALA ---")
        teatro = input("Nombre del Teatro: ").strip()
        ciudad = input("Ciudad del Teatro: ").strip()
        sala = input("Nombre de la Sala: ").strip()
        
        cinecosta.calcular_estadisticas_sala(teatro, ciudad, sala)
        
    # -----------------------------------------------------------------
    # OPCIÓN 4: Ver Mapa de Ocupación NumPy en Consola
    # -----------------------------------------------------------------
    elif opcion == "4":
        print("\n--- VISUALIZACIÓN DE MATRIZ NUMPY ---")
        teatro = input("Nombre del Teatro: ").strip()
        ciudad = input("Ciudad del Teatro: ").strip()
        sala = input("Nombre de la Sala: ").strip()
        
        # Generar llave de búsqueda idéntica a la lógica
        id_teatro = f"{teatro}-{ciudad}"
        
        # Validación de existencia antes de imprimir
        if id_teatro in cinecosta.teatros and sala in cinecosta.teatros[id_teatro].salas:
            objeto_sala = cinecosta.teatros[id_teatro].salas[sala]
            print(f"\nMatriz actual de NumPy para {sala} ({teatro}):")
            print(objeto_sala.mapa_ocupacion)
        else:
            print("[ERROR] El teatro o la sala no se encuentran cargados en el sistema.")
            
    # -----------------------------------------------------------------
    # OPCIÓN 5: Salir
    # -----------------------------------------------------------------
    elif opcion == "5":
        print("\nGracias por utilizar el sistema de Cinecosta. ¡Hasta luego!")
        continuar = False
        
    # Control de opción inválida
    else:
        print("\n[ERROR] Opción no válida. Por favor, digite un número entre 1 y 5.")

    print("\n" + "-"*40)