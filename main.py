from model.D2_5.geometry.SketchController import SketchController
from model.D2_5.geometry.ModelerController import ModelerController
from model.D2_5.geometry.misc.points import *
from ansys.geometry.core.math import Point2D
from ansys.geometry.core.misc import UNITS, Distance, Angle
from ansys.geometry.core.misc.measurements import DEFAULT_UNITS

"""
File ready to run.
"""


def main():
    # --- DEFAULT UNITS --- #
    DEFAULT_UNITS.LENGTH = UNITS.millimeter  # not working for sketch.plot()
    DEFAULT_UNITS.ANGLE = UNITS.degree

    # --- PARAMETERS --- #
    n_airfoils = 3
    naca_code = "0012"
    center = Point2D([0, 0])
    radius = Distance(5)
    angle_of_attack_deg = Angle(90.0)
    spread = Distance(0.4)
    file_name = "model"

    modeler = ModelerController("Wind Turbine")

    # --- Airfoils --- #
    airfoil_sketches = []
    for i in range(n_airfoils):
        sketch = SketchController(f"NACA_airfoil_{i+1}")

        angle = Angle(360.0 * i / n_airfoils)
        foil = Airfoil(naca_code)
        foil.generate_points()
        placed_foil = translate_airfoil_on_circle(foil, center, radius, angle, angle_of_attack_deg)
        sketch.add_points(placed_foil.points)

        airfoil_sketches.append(sketch)

    modeler.add_component_and_named_selection("NACA", airfoil_sketches, "Airfoils")

    # --- Ring with cuts --- #

    ring_sketch = SketchController("Ring")
    ring_sketch.add_ring(center, radius, spread)

    modeler.add_component_and_named_selection("Ring", ring_sketch, "Ring")
    modeler.cut("Ring", "NACA")

    # --- Inner circle --- #

    inner_radius = Distance(radius.value.m - spread.value.m / 2.0)
    inner_circle_sketch = SketchController("Inner Circle")
    inner_circle_sketch.add_circle(center, inner_radius)

    modeler.add_component_and_named_selection("Inner Circle", inner_circle_sketch, "Inner Circle")

    # --- Environment -- #

    env_sketch = SketchController("Env")
    env_sketch.add_env()

    modeler.add_component_and_named_selection("Env", env_sketch, "Env")
    modeler.cut("Env", "Inner Circle")
    modeler.cut("Env", "Ring")
    modeler.cut("Env", "NACA")

    # --- Boy of influence --- #

    boi_sketch = SketchController("BoI")
    boi_sketch.add_boi(center)

    modeler.add_component_and_named_selection("BoI", boi_sketch, "BoI")

    # -- Plot in Discovery -- #
    modeler.save(file_name)
    modeler.plot()
    modeler.close()


if __name__ == "__main__":
    main()
