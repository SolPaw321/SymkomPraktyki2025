from ansys.geometry.core.sketch import Sketch
from ansys.geometry.core.math import Point2D
from ansys.geometry.core.misc import Distance, Angle
from numpy import array


class SketchController:
    """
    SketchController is a class for creating sketches.
    """
    def __init__(self, name: str):
        self.sketch = Sketch()
        self.name = name

        self.scale_factor = 20

    @staticmethod
    def __validate_points(points):
        """
        Validate points parameter.

        Args:
            points (list[Point2D]): List of points to sketch
        """
        if not all(isinstance(x, Point2D) for x in points):
            raise TypeError(f"\'points\' list should contains Points2D")

    def add_circle(self, center: Point2D,
                   radius: Distance | float | int):  # -> ?
        """
        Add a circle to the sketch.

        Args:
            center (Point2D): center of circle, default=Point2D([0, 0])
            radius (Distance): radius of circle, default=Distance(1)
        """
        if isinstance(radius, float | int):
            radius = Distance(radius)
        return self.sketch.circle(center, radius)

    def add_circle_using_arc(self, center: Point2D,
                             radius: Distance | float | int):
        """
        Add a circle to Sketch, using ''arc'' function instead of ''Circle'' class.

        Args:
            center (Point2D): center of circle, default=Point2D([0, 0])
            radius (Distance): radius of circle, default=Distance(1)
        """
        start = Point2D([radius.value.m, 0])
        self.sketch.arc_from_start_center_and_angle(start, center, Angle(360))

    def add_ring(self, center: Point2D,
                 radius: Distance | int | float,
                 spread: Distance | int | float):
        """
        Add a ring in which airfoils ''swim''.

        Args:
            center (Point2D): the center for circles
            radius (Distance | int | float): radius of center circle
            spread (Distance | int | float): spread of the ring
        """
        inner_radius = Distance(radius.value + spread.value / 2.0)
        outer_radius = Distance(radius.value - spread.value / 2.0)

        self.add_circle_using_arc(center, inner_radius)
        self.add_circle_using_arc(center, outer_radius)

    def add_points(self, points: list[Point2D]):
        """
        Add list of points to the sketch.

        Args:
            points (list[Point2D]): list of points to add
        """
        self.__validate_points(points)

        for i in range(len(points) - 1):
            self.sketch.segment(points[i], points[i + 1])
        self.sketch.segment(points[-1], points[0])

    def add_env(self):
        """
        Add environment (the rest of world).
        """
        scale_factor = self.scale_factor

        corners = array([array([-1, -1]),
                         array([-1, 1]),
                         array([2, 1]),
                         array([2, -1])]) * scale_factor
        corners = [Point2D(arr) for arr in corners]

        (
            self.sketch.segment(corners[0], corners[1])
            .segment_to_point(corners[2]).segment_to_point(corners[3])
            .segment_to_point(corners[0])
        )

    def add_boi(self, center: Point2D):
        """
        Add body of influence in Sketch.

        Args:
            center (Point2D): center of circle using for arc
        """
        scale_factor = self.scale_factor / 3

        corners = array([array([-1, -1]),
                         array([-1, 1]),
                         array([3, 1]),
                         array([3, -1])]) * scale_factor
        corners = [Point2D(arr) for arr in corners]
        (
            self.sketch.arc(corners[0], corners[1], center, clockwise=True)
            .segment_to_point(corners[2])
            .segment_to_point(corners[3])
            .segment_to_point(corners[0])
        )

    def plot(self):
        """
        Plot all added elements.
        """
        self.sketch.plot()

    def get(self) -> tuple[str, Sketch, Distance]:
        """
        Return:
            tuple[str, Sketch, Distance]: name, Sketch and high
        """
        return self.name, self.sketch, Distance(0.1)
