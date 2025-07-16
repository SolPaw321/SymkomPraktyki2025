from typing import List, Union

import numpy as np

from ansys.geometry.core.math import Point2D
from ansys.geometry.core import launch_modeler
from ansys.geometry.core.sketch import Sketch
def naca_airfoil_4digits(number: Union[int, str], n_points: int = 200) -> list[Point2D]:
    """
    Generate a NACA 4-digits airfoil.

    Parameters
    ----------
    number : int or str
        NACA 4-digit number.
    n_points : int
        Number of points to generate the airfoil. The default is ``200``.
        Number of points in the upper side of the airfoil.
        The total number of points is ``2 * n_points - 1``.

    Returns
    -------
    list[Point2D]
        List of points that define the airfoil.
    """
    # Check if the number is a string
    if isinstance(number, str):
        number = int(number)

    # Calculate the NACA parameters
    m = number // 1000 * 0.01
    p = number // 100 % 10 * 0.1
    t = number % 100 * 0.01

    # Generate the airfoil
    points = []
    for i in range(n_points):

        # Make it a exponential distribution so the points are more concentrated
        # near the leading edge
        x = (1 - np.cos(i / (n_points - 1) * np.pi)) / 2

        # Check if it is a symmetric airfoil
        if p == 0 and m == 0:
            # Camber line is zero in this case
            yc = 0
            dyc_dx = 0
        else:
            # Compute the camber line
            if x < p:
                yc = m / p**2 * (2 * p * x - x**2)
                dyc_dx = 2 * m / p**2 * (p - x)
            else:
                yc = m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * x - x**2)
                dyc_dx = 2 * m / (1 - p) ** 2 * (p - x)

        # Compute the thickness
        yt = 5 * t * (0.2969 * x**0.5
                      - 0.1260 * x
                      - 0.3516 * x**2
                      + 0.2843 * x**3
                      - 0.1015 * x**4)

        # Compute the angle
        theta = np.arctan(dyc_dx)

        # Compute the points (upper and lower side of the airfoil)
        xu = x - yt * np.sin(theta)
        yu = yc + yt * np.cos(theta)
        xl = x + yt * np.sin(theta)
        yl = yc - yt * np.cos(theta)

        # Append the points
        points.append(Point2D([xu, yu]))
        points.insert(0, Point2D([xl, yl]))

        # Remove the first point since it is repeated
        if i == 0:
            points.pop(0)

    return points


NACA_AIRFOIL = "0012"
# Create a sketch
sketch = Sketch()

# Generate the points of the airfoil
points = naca_airfoil_4digits(NACA_AIRFOIL)

# Create the segments of the airfoil
for i in range(len(points) - 1):
    sketch.segment(points[i], points[i + 1])

# Close the airfoil
sketch.segment(points[-1], points[0])

# Launch the modeler
modeler = launch_modeler()

# Create the design
design = modeler.create_design(f"NACA_Airfoil_{NACA_AIRFOIL}")

# Extrude the airfoil
design.extrude_sketch("Airfoil", sketch, 1)

# Plot the design
design.plot()