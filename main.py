from ansys.geometry.core import launch_modeler
from ansys.geometry.core.math import Plane, Point3D, Point2D
from ansys.geometry.core.misc import UNITS, Distance
from ansys.geometry.core.sketch import Sketch

# Define a sketch
origin = Point3D([0, 0, 10])
plane = Plane(origin, direction_x=[1, 0, 0], direction_y=[0, 1, -1])

# Create a sketch
sketch = Sketch(plane)
sketch.circle(Point2D([1, 1]), 30 * UNITS.m)
sketch.ellipse(Point2D([1, 5]), 5 * UNITS.m, 2 * UNITS.m)
sketch.plot()
