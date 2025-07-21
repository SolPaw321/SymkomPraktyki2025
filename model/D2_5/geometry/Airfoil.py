from beartype import beartype as check_input_types
from ansys.geometry.core.math import Point2D
from numpy import sin, cos, arctan, pi


class Airfoil:
    """
    Airfoil class description.
    """
    @check_input_types
    def __init__(self, number: str | int, n_points: str | int = 200):
        self.__validate_number(number)
        self.__validate_n_points(n_points)
        self.number = int(number)
        self.n_points = int(n_points)

        self.m, self.p, self.t = None, None, None
        self.__calculate_naca_digits()

        self._points = []

    @staticmethod
    def __validate_number(number):
        """
        Validate "number" parameter.

        Args:
            number (str | int): The number of points that make up a NACA airfoil.

        Raise:
            TypeError: number is not str or int
            ValueError: number is not 4-digit
        """
        if not isinstance(number, str | int):
            raise TypeError(f"\'number\' parameter should be str or int, got {type(number)}")
        if not len(str(number)) == 4:
            raise ValueError(f"expected 4 digit (eq. 1234), got {len(str(number))} {number}")

    @staticmethod
    def __validate_n_points(n_points):
        """
        Validate "n_points" parameter.

        Args:
            n_points (str | int): The number of points that make up a NACA airfoil.

        Raise:
            TypeError: n_points is not str or int
            ValueError: n_points is not positive
        """
        if not isinstance(n_points, str | int):
            raise TypeError(f"\'n_points\' parameter should be str or int, got {type(n_points)}")
        if not int(n_points) > 0:
            raise ValueError(f"\'n_points\' parameter should be positive, got {n_points}")

    def __calculate_naca_digits(self):
        """
        Calculate NACA 4 digits.
        """
        self.m = self.number // 1000 * 0.01
        self.p = self.number // 100 % 10 * 0.1
        self.t = self.number % 100 * 0.01

    def generate_points(self) -> list[Point2D]:
        """
            Generate a NACA 4-digits airfoil.

            Return:
                list[Point2D]: List of points that define the airfoil
            """
        for i in range(self.n_points):

            # Make it an exponential distribution so the points are more concentrated
            # near the leading edge
            x = (1 - cos(i / (self.n_points - 1) * pi)) / 2

            # Check if it is a symmetric airfoil
            if self.p == 0 and self.m == 0:
                # Camber line is zero in this case
                yc = 0
                dyc_dx = 0
            else:
                # Compute the camber line
                if x < self.p:
                    yc = self.m / self.p ** 2 * (2 * self.p * x - x ** 2)
                    dyc_dx = 2 * self.m / self.p ** 2 * (self.p - x)
                else:
                    yc = self.m / (1 - self.p) ** 2 * ((1 - 2 * self.p) + 2 * self.p * x - x ** 2)
                    dyc_dx = 2 * self.m / (1 - self.p) ** 2 * (self.p - x)

            # Compute the thickness
            yt = 5 * self.t * (0.2969 * x ** 0.5
                               - 0.1260 * x
                               - 0.3516 * x ** 2
                               + 0.2843 * x ** 3
                               - 0.1015 * x ** 4)

            # Compute the angle
            theta = arctan(dyc_dx)

            # Compute the points (upper and lower side of the airfoil)
            xu = x - yt * sin(theta)
            yu = yc + yt * cos(theta)
            xl = x + yt * sin(theta)
            yl = yc - yt * cos(theta)

            # Append the points
            self._points.append(Point2D([xu, yu]))
            self._points.insert(0, Point2D([xl, yl]))

            # Remove the first point since it is repeated
            if i == 0:
                self._points.pop(0)
        return self._points

    @property
    def points(self) -> list[Point2D]:
        """
        Return List of points that define the airfoil.

        Args:
            list[Point2D]: List of points that define the airfoil
        """
        return self._points

    @points.setter
    def points(self, points: list[Point2D]):
        """
        Set new points.

        Args:
            points (list[Point2D]): list of new points to set
        """
        self._points = points
