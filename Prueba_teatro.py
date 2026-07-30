from Logica_teatro import Teatro
from sala import Sala

teatro = Teatro(
    "Teatro Centro",
    "Santa Marta"
)

sala1 = Sala(
    "Sala 1",
    "A",
    12000
)

teatro.agregar_sala(sala1)

resultado = teatro.buscar_sala("Sala 1")

print("Sala encontrada:")
print(resultado.nombre)
print(resultado.tamano)
print(resultado.precio_base)