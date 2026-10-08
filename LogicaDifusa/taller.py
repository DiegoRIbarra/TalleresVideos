"""Taller práctico: lógica difusa en Python.

Instalación:
    pip install scikit-fuzzy numpy scipy networkx matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def mostrar_operaciones_difusas() -> None:
    """Demuestra unión, intersección y complemento difusos."""
    alto = 0.8
    pesado = 0.4

    print("OR  (unión):        ", max(alto, pesado))
    print("AND (intersección): ", min(alto, pesado))
    print("NOT (complemento):  ", round(1 - alto, 2))


def crear_sistema_propina() -> tuple[ctrl.ControlSystem, ctrl.Consequent]:
    """Crea las variables lingüísticas y las reglas del sistema."""
    comida = ctrl.Antecedent(np.arange(0, 11, 1), "comida")
    servicio = ctrl.Antecedent(np.arange(0, 11, 1), "servicio")
    propina = ctrl.Consequent(np.arange(0, 26, 1), "propina")

    comida.automf(names=["mala", "regular", "buena"])
    servicio.automf(names=["mala", "regular", "buena"])

    propina["baja"] = fuzz.trimf(propina.universe, [0, 0, 13])
    propina["media"] = fuzz.trimf(propina.universe, [0, 13, 25])
    propina["alta"] = fuzz.trimf(propina.universe, [13, 25, 25])

    r1 = ctrl.Rule(
        servicio["mala"] | comida["mala"],
        propina["baja"],
    )
    r2 = ctrl.Rule(servicio["regular"], propina["media"])
    r3 = ctrl.Rule(
        servicio["buena"] | comida["buena"],
        propina["alta"],
    )

    return ctrl.ControlSystem([r1, r2, r3]), propina


def calcular_propina(
    sistema: ctrl.ControlSystem,
    comida: float,
    servicio: float,
) -> float:
    """Calcula el porcentaje de propina para una comida y servicio."""
    simulacion = ctrl.ControlSystemSimulation(sistema)
    simulacion.input["comida"] = comida
    simulacion.input["servicio"] = servicio
    simulacion.compute()
    return simulacion.output["propina"]


def mostrar_resultado_principal(
    sistema: ctrl.ControlSystem,
    propina: ctrl.Consequent,
) -> ctrl.ControlSystemSimulation:
    """Calcula el caso principal y muestra su resultado gráfico."""
    simulacion = ctrl.ControlSystemSimulation(sistema)
    simulacion.input["comida"] = 6.5
    simulacion.input["servicio"] = 9.8
    simulacion.compute()

    print("Propina sugerida:", round(simulacion.output["propina"], 2), "%")

    # La gráfica muestra la combinación de reglas y el valor defuzzificado.
    propina.view(sim=simulacion)
    plt.savefig("propina.png")
    plt.show()

    return simulacion


def mostrar_reto(sistema: ctrl.ControlSystem) -> None:
    """Calcula los cuatro casos opcionales del taller."""
    print("\nComida | Servicio | Propina")
    for comida, servicio in [(2, 3), (5, 5), (9, 9), (2, 9)]:
        propina = calcular_propina(sistema, comida, servicio)
        print(f"{comida:^6} | {servicio:^8} | {propina:.2f} %")


def main() -> None:
    """Ejecuta todos los ejercicios del taller."""
    print("---------- EJERCICIO 1: Operaciones difusas ----------")
    mostrar_operaciones_difusas()

    print("\n---------- EJERCICIO 2: Inferencia difusa ----------")
    sistema, propina = crear_sistema_propina()
    mostrar_resultado_principal(sistema, propina)

    print("\n---------- RETO: casos de la tabla ----------")
    mostrar_reto(sistema)


if __name__ == "__main__":
    main()
