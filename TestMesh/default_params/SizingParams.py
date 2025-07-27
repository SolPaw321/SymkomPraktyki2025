from dataclasses import dataclass


"""
Dataclasses for global sizing params by sizing type.
"""


@dataclass
class GlobalSizingParams:
    min: float = 90.0
    max: float = 100.0
    growth_rate: float = 1.1


@dataclass
class CurvatureSizingParams:
    min: float = 90.0
    max: float = 100.0
    normal_angle: float = 18.0
    growth_rate: float = 1.1


@dataclass
class BoiSizingParams:
    max: float = 100.0
    growth_rate: float = 1.1


@dataclass
class ProximitySizingParams:
    min: float = 90.0
    max: float = 100.0
    growth_rate: float = 1.1
    elements_per_gap: float = 3.0
    ignore_orientation: bool = True
    ignore_self_proximity: bool = False


@dataclass
class MeshedSizingParams:
    growth_rate: float = 1.1
