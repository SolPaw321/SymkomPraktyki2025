from model.D2.geometry.VisualiseSketch import VisualiseSketch
from model.D2.geometry.misc.points import *
from ansys.geometry.core.math import Point2D
from ansys.geometry.core.misc import UNITS, Distance, Angle
from ansys.geometry.core.misc.measurements import DEFAULT_UNITS


def main():
    # --- DEFAULT UNITS --- #
    DEFAULT_UNITS.LENGTH = UNITS.millimeter  # not working for sketch.plot()

    # --- PARAMETERS --- #
    n_airfoils = 3
    naca_code = "0012"
    center = Point2D([0, 0])
    radius = Distance(1)
    angle_of_attack_deg = Angle(90.0)

    visual = VisualiseSketch()
    for i in range(n_airfoils):
        angle = Angle(360 * i / n_airfoils)
        foil = Airfoil(naca_code)
        foil.generate_points()
        placed_foil = translate_airfoil_on_circle(foil, center, radius, angle, angle_of_attack_deg)
        visual.add_points(placed_foil.points)

    visual.add_circle(center, radius)
    visual.plot()


if __name__ == "__main__":
    main()
