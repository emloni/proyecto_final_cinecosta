import numpy as np
from sala import Sala
from Logica_teatro import Teatro


# ======================================================================
# Datos de prueba
# ======================================================================
# Se crean 3 salas y se les asignan mapas de ocupación e ingresos
# manualmente (sin pasar por CSV), para poder verificar los resultados
# a mano con números sencillos.
#
# Sala 1 (tamaño A, 8x10 = 80 sillas): ocupación constante = 5, ingreso constante = 50000
# Sala 2 (tamaño A, 8x10 = 80 sillas): ocupación constante = 3, ingreso constante = 30000
# Sala 3 (tamaño B, 10x12 = 120 sillas): no se le construyen los mapas (para probar errores)

sala1 = Sala("Sala 1", "A", 12000)
sala1.mapa_ocupacion = np.full((sala1.filas, sala1.sillas_por_fila), 5)
sala1.mapa_ingresos = np.full((sala1.filas, sala1.sillas_por_fila), 50000.0)
sala1.ocupacion_construida = True
sala1.ingresos_construidos = True

sala2 = Sala("Sala 2", "A", 12000)
sala2.mapa_ocupacion = np.full((sala2.filas, sala2.sillas_por_fila), 3)
sala2.mapa_ingresos = np.full((sala2.filas, sala2.sillas_por_fila), 30000.0)
sala2.ocupacion_construida = True
sala2.ingresos_construidos = True

sala3 = Sala("Sala 3", "B", 15000)
# sala3 se deja SIN construir sus mapas a propósito, para probar los errores


# ======================================================================
# Prueba 1: agregar_sala y buscar_sala
# ======================================================================
def test_agregar_y_buscar_sala():
    print("Prueba 1: agregar_sala y buscar_sala")

    teatro = Teatro("Teatro Centro", "Barranquilla")
    teatro.agregar_sala(sala1)
    teatro.agregar_sala(sala2)
    teatro.agregar_sala(sala3)

    assert len(teatro.salas) == 3, "El teatro debería tener 3 salas"

    encontrada = teatro.buscar_sala("Sala 1")
    assert encontrada is sala1, "buscar_sala debería devolver el objeto Sala 1"

    no_existe = teatro.buscar_sala("Sala Fantasma")
    assert no_existe is None, "buscar_sala debería devolver None si no existe"

    print("  OK: se agregaron y encontraron las salas correctamente\n")
    return teatro


# ======================================================================
# Prueba 2: no se puede agregar algo que no sea una Sala
# ======================================================================
def test_agregar_sala_tipo_invalido():
    print("Prueba 2: agregar_sala con un objeto que no es Sala")

    teatro = Teatro("Teatro Norte", "Santa Marta")
    try:
        teatro.agregar_sala("esto no es una sala")
        assert False, "Debería haber lanzado TypeError"
    except TypeError as error:
        print(f"  OK: se lanzó TypeError como se esperaba -> {error}\n")


# ======================================================================
# Prueba 3: no se puede agregar dos veces la misma sala
# ======================================================================
def test_agregar_sala_duplicada():
    print("Prueba 3: agregar_sala con una sala ya agregada")

    teatro = Teatro("Teatro Norte", "Santa Marta")
    teatro.agregar_sala(sala1)
    try:
        teatro.agregar_sala(sala1)
        assert False, "Debería haber lanzado ValueError"
    except ValueError as error:
        print(f"  OK: se lanzó ValueError como se esperaba -> {error}\n")


# ======================================================================
# Prueba 4: obtener_salas_por_tamano
# ======================================================================
def test_obtener_salas_por_tamano(teatro):
    print("Prueba 4: obtener_salas_por_tamano")

    salas_a = teatro.obtener_salas_por_tamano("A")
    salas_b = teatro.obtener_salas_por_tamano("b")  # en minúscula a propósito

    assert len(salas_a) == 2, "Debería haber 2 salas de tamaño A"
    assert len(salas_b) == 1, "Debería haber 1 sala de tamaño B"
    assert sala1 in salas_a and sala2 in salas_a, "sala1 y sala2 deben estar en el resultado"

    print("  OK: se filtraron correctamente las salas por tamaño\n")


# ======================================================================
# Prueba 5: comparar_ingresos_por_tamano - caso con menos de 2 salas
# ======================================================================
def test_comparar_ingresos_menos_de_dos_salas(teatro):
    print("Prueba 5: comparar_ingresos_por_tamano con menos de 2 salas del mismo tamaño")

    try:
        teatro.comparar_ingresos_por_tamano("B")
        assert False, "Debería haber lanzado ValueError (solo hay 1 sala tamaño B)"
    except ValueError as error:
        print(f"  OK: se lanzó ValueError como se esperaba -> {error}\n")


# ======================================================================
# Prueba 6: comparar_ingresos_por_tamano - caso exitoso
# ======================================================================
def test_comparar_ingresos_por_tamano(teatro):
    print("Prueba 6: comparar_ingresos_por_tamano con 2 salas tamaño A")

    resultado = teatro.comparar_ingresos_por_tamano("A")

    # sala1: 80 sillas a 50000 c/u -> ingreso total = 4,000,000
    # sala2: 80 sillas a 30000 c/u -> ingreso total = 2,400,000
    assert resultado["ingresos_totales_por_sala"]["Sala 1"] == 4_000_000.0
    assert resultado["ingresos_totales_por_sala"]["Sala 2"] == 2_400_000.0

    # Sala 1 tiene más ingresos, debe ser la identificada como mayor
    assert resultado["sala_mayor_ingreso"] == "Sala 1"

    # La estructura combinada debe tener forma (2 salas, 8 filas, 10 columnas)
    assert resultado["estructura"].shape == (2, 8, 10)

    # El mapa promedio en cualquier celda debe ser (50000 + 30000) / 2 = 40000
    valor_esperado = (50000.0 + 30000.0) / 2
    assert np.allclose(resultado["mapa_ingresos_promedio"], valor_esperado)

    print("  OK: ingresos totales, sala con mayor ingreso y mapa promedio correctos\n")


# ======================================================================
# Prueba 7: ocupacion_promedio e ingreso_promedio - caso exitoso
# ======================================================================
def test_promedios_teatro():
    print("Prueba 7: ocupacion_promedio e ingreso_promedio (solo con sala1 y sala2)")

    teatro = Teatro("Teatro Centro", "Barranquilla")
    teatro.agregar_sala(sala1)
    teatro.agregar_sala(sala2)

    # sala1: 80 sillas ocupación=5 -> suma=400
    # sala2: 80 sillas ocupación=3 -> suma=240
    # total sillas = 160, suma total = 640 -> promedio = 640/160 = 4.0
    assert teatro.ocupacion_promedio() == 4.0

    # sala1: 80 sillas ingreso=50000 -> suma=4,000,000
    # sala2: 80 sillas ingreso=30000 -> suma=2,400,000
    # total sillas = 160, suma total = 6,400,000 -> promedio = 40000.0
    assert teatro.ingreso_promedio() == 40000.0

    print("  OK: ocupacion_promedio = 4.0, ingreso_promedio = 40000.0\n")


# ======================================================================
# Prueba 8: error cuando una sala no tiene sus mapas construidos
# ======================================================================
def test_promedios_con_sala_sin_construir():
    print("Prueba 8: ocupacion_promedio con una sala sin mapa construido")

    teatro = Teatro("Teatro Norte", "Santa Marta")
    teatro.agregar_sala(sala3)  # sala3 no tiene mapas construidos

    try:
        teatro.ocupacion_promedio()
        assert False, "Debería haber lanzado ValueError"
    except ValueError as error:
        print(f"  OK: se lanzó ValueError como se esperaba -> {error}\n")


# ======================================================================
# Prueba 9: error cuando el teatro no tiene salas
# ======================================================================
def test_promedios_sin_salas():
    print("Prueba 9: ocupacion_promedio en un teatro sin salas")

    teatro_vacio = Teatro("Teatro Vacío", "Cartagena")

    try:
        teatro_vacio.ocupacion_promedio()
        assert False, "Debería haber lanzado ValueError"
    except ValueError as error:
        print(f"  OK: se lanzó ValueError como se esperaba -> {error}\n")


# ======================================================================
# Ejecución de todas las pruebas
# ======================================================================
if __name__ == "__main__":
    teatro_principal = test_agregar_y_buscar_sala()
    test_agregar_sala_tipo_invalido()
    test_agregar_sala_duplicada()
    test_obtener_salas_por_tamano(teatro_principal)
    test_comparar_ingresos_menos_de_dos_salas(teatro_principal)
    test_comparar_ingresos_por_tamano(teatro_principal)
    test_promedios_teatro()
    test_promedios_con_sala_sin_construir()
    test_promedios_sin_salas()

    print("=" * 50)
    print("TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
    print("=" * 50)
