from Geometry.SketchController import SketchController
from Geometry.ModelerController import ModelerController
from ansys.geometry.core.math import Point2D
from ansys.geometry.core.misc import UNITS, Distance, Angle
from ansys.geometry.core.misc.measurements import DEFAULT_UNITS

"""
File ready to run.
"""


def main():
    # --- DEFAULT UNITS --- #
    DEFAULT_UNITS.LENGTH = UNITS.meter  # not working for sketch.plot()
    DEFAULT_UNITS.ANGLE = UNITS.degree

    # --- USER PARAMETERS --- #
    n_airfoils = 3
    launch_airfoil_from_file = True
    naca_code = "0012"  # only if launch_airfoil_from_file = False
    file_name = 'airfoil6412.dsco'  # only if launch_airfoil_from_file = True
    center = Point2D([0, 0])
    radius = Distance(2)
    angle_of_attack_deg = Angle(90.0)
    spread = Distance(0.7)
    model_type = "3D"  # "2D" or "3D"
    save_file_name = f"model_{model_type}"
    main_fluid_name = 'fluid-1'
    main_fluid_name_selection = 'fluid-1'
    ring_name = 'fluid-2'
    ring_name_selection = 'fluid-2'
    inner_circle_name = "fluid-3"
    inner_circle_name_selection = "fluid-3"
    naca_name = "NACA"
    boi_name = "boi"
    boi_name_selection = "boi"

    modeler = ModelerController("Wind_Turbine", model_type, launch_airfoil_from_file)

    # --- Airfoils --- #
    if launch_airfoil_from_file:
        # launch ready airfoil model from file
        modeler.load_airfoils(file_name, center, radius, angle_of_attack_deg, n_airfoils)
    else:
        # or generate automatically based on naca_name
        airfoil_sketch = SketchController(naca_name)
        airfoil_sketches = airfoil_sketch.add_airfoils_by_sketch(naca_code, n_airfoils, center, radius, angle_of_attack_deg)
        modeler.add_component(naca_name, airfoil_sketches)

    # --- Ring without cuts --- #
    ring_sketch = SketchController(ring_name)
    ring_sketch.add_ring(center, radius, spread)

    modeler.add_component(ring_name, ring_sketch)
    modeler.add_named_selection(ring_name, ring_name_selection)

    # --- Inner circle --- #
    inner_radius = Distance(radius.value.m - spread.value.m / 2.0)
    inner_circle_sketch = SketchController(inner_circle_name)
    inner_circle_sketch.add_circle_using_arc(center, inner_radius)

    modeler.add_component(inner_circle_name, inner_circle_sketch)
    modeler.add_named_selection(inner_circle_name, inner_circle_name_selection)

    # --- Env --- #
    env_sketch = SketchController(main_fluid_name)
    outer_radius = Distance(radius.value.m + spread.value.m / 2.0)
    env_sketch.add_env(center, outer_radius)

    modeler.add_component(main_fluid_name, env_sketch)
    modeler.add_named_selection(main_fluid_name, main_fluid_name_selection)

    # --- Create named selections: wall, inlet, outlet
    modeler.add_inlet_and_outlet(main_fluid_name)
    modeler.add_wall(naca_name, ring_name)
    modeler.add_symmetry_named_selection()

    # --- Body of influence --- #
    boi_sketch = SketchController(boi_name)
    boi_sketch.add_boi(center)

    modeler.add_component(boi_name, boi_sketch)
    modeler.add_named_selection(boi_name, boi_name_selection)

    # --- Remove NACA --- #
    modeler.delete_unnecessary_components()

    # --- Share Topology --- #
    modeler.share_topology()

    # -- Plot in Discovery  and save -- #
    modeler.plot()
    modeler.save(save_file_name)
    modeler.close()


if __name__ == "__main__":
    main()
