from ansys.geometry.core.math import Point2D
from math import radians, cos, sin
from ansys.geometry.core.misc import Distance, Angle
from model.D2_5.geometry.Airfoil import Airfoil


def points_rotation(points: list[Point2D] | Point2D,
                    center: Point2D,
                    angle: Angle) -> list[Point2D] | Point2D:
    """
    Rotate a list of points (or a single point) around center by angle.

    Args:
        points (list[Point2D] | Point2D): list of points or single point to rotate
        center (Point2D): the center of rotation
        angle (Angle): the angle (degrees) to rotate
    Return:
        list[Point2D] | Point2D: list of rotated points or single rotated point
    """
    if isinstance(points, Point2D):
        points = [points]
        list_return = False
    else:
        list_return = True

    new_points = []
    angle_rad = radians(angle.value.m)
    for point in points:
        translated_x = point.x - center.x
        translated_y = point.y - center.y

        rotated_x = translated_x * cos(angle_rad) - translated_y * sin(angle_rad)
        rotated_y = translated_x * sin(angle_rad) + translated_y * cos(angle_rad)

        new_x = rotated_x + center.x
        new_y = rotated_y + center.y

        new_points.append(Point2D([new_x.m, new_y.m]))

    if list_return:
        return new_points
    return new_points[0]


def translate_airfoil_on_circle(foil: Airfoil,
                                center: Point2D,
                                radius: Distance,
                                angle_deg: Angle,
                                angle_of_attack_deg: Angle) -> Airfoil:
    """
    Place an Airfoil on a circle.

    Args:
        foil (Airfoil): Airfoil with list of points
        center (Point2D): center of circle
        radius (Distance): radius of circle
        angle_deg (Angle): interior angle (degrees)
        angle_of_attack_deg (Angle): angle of attack (degrees)
    Return:
        Airfoil: Airfoil with set new points
    """
    points = foil.points
    cx = center.x + radius.value * cos(radians(angle_deg.value.m))
    cy = center.y + radius.value * sin(radians(angle_deg.value.m))
    new_center = Point2D([cx.m, cy.m])

    translated = []
    for p in points:
        local = Point2D([p.x.m - 0.5, p.y.m])

        local_rotated = points_rotation(local, Point2D([0, 0]), angle_of_attack_deg)

        shifted = Point2D([local_rotated.x.m + new_center.x.m, local_rotated.y.m + new_center.y.m])

        final = points_rotation(shifted, new_center, angle_deg)
        translated.append(final)

    foil.points = translated

    return foil
