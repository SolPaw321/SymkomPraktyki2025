from ansys.geometry.core.sketch import Sketch
from ansys.geometry.core.math import Point2D
from ansys.geometry.core.misc import Distance


class VisualiseSketch:
    """
    VisualiseSketch is a class for visualisation sketch.
    """
    def __init__(self):
        self.sketch = Sketch()

    @staticmethod
    def __validate_points(points):
        """
        Validate points parameter.

        :param:
            points (list[Point2D]): List of points to sketch
        """
        if not all(isinstance(x, Point2D) for x in points):
            raise TypeError(f"\'points\' list should contains Points2D")

    def add_circle(self, center: Point2D = Point2D([0, 0]), radius: Distance | float | int = Distance(1)):
        """
        Add a circle to the sketch.

        :param:
            center (Point2D): center of circle, default=Point2D([0, 0])
            radius (Distance): radius of circle, default=Distance(1)
        """
        if isinstance(radius, float | int):
            radius = Distance(radius)
        self.sketch.circle(center, radius)

    def add_points(self, points: list[Point2D]):
        """
        Add list of points to the sketch.

        :param:
            points (list[Point2D]): list of points to add
        """
        self.__validate_points(points)

        for i in range(len(points) - 1):
            self.sketch.segment(points[i], points[i+1])
        self.sketch.segment(points[-1], points[0])

    def plot(self):
        """
        Plot all added elements.

        """
        self.sketch.plot()
