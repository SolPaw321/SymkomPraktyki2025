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

    # --- USER PARAMETERS --- #
    n_airfoils = 3
    naca_code = "0012"
    center = Point2D([0, 0])
    radius = Distance(5)
    angle_of_attack_deg = Angle(90.0)
    spread = Distance(0.4)
    model_type = "2D"  # "2D" pr "3D"
    file_name = f"model_{model_type}"

    modeler = ModelerController("Wind_Turbine", model_type)
    # --- Ring without cuts --- #

    ring_sketch = SketchController("Ring")
    ring_sketch.add_ring(center, radius, spread)

    modeler.add_component("Ring", ring_sketch)
    modeler.add_named_selection("Ring", "fluid-2")

    # --- Inner circle --- #

    inner_radius = Distance(radius.value.m - spread.value.m / 2.0)
    inner_circle_sketch = SketchController("InnerCircle")
    inner_circle_sketch.add_circle_using_arc(center, inner_radius)

    modeler.add_component("InnerCircle", inner_circle_sketch)
    modeler.add_named_selection("InnerCircle", "fluid-3")

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

    modeler.add_component("NACA", airfoil_sketches)

    # --- Env --- #
    env_sketch = SketchController("Env")
    outer_radius = Distance(radius.value.m + spread.value.m / 2.0)
    env_sketch.add_env(center, outer_radius)

    modeler.add_component("Env", env_sketch)
    modeler.add_named_selection("Env", "fluid-1")
    # modeler.cut("Env", "InnerCircle")
    # modeler.cut("Env", "Ring")

    # --- Create named selections: wall, inlet, outlet
    modeler.add_inlet_and_outlet()
    modeler.add_wall()

    # --- Body of influence --- #
    boi_sketch = SketchController("BoI")
    boi_sketch.add_boi(center)

    modeler.add_component("BoI", boi_sketch)
    modeler.add_named_selection("BoI", "boi")

    # --- Remove NACA --- #
    modeler.delete_component("NACA")

    # -- Plot in Discovery -- #
    modeler.save(file_name)
    modeler.plot()
    modeler.close()


if __name__ == "__main__":
    main()
