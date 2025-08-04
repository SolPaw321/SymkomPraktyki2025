from dataclasses import dataclass


"""
Dataclasses for global sizing params by sizing type.
"""


@dataclass
class GlobalSizingParams:
    min: float = 0.01
    max: float = 2000.0
    growth_rate: float = 1.1


@dataclass
class CurvatureSizingParams:
    min: float = None
    max: float = None
    normal_angle: float = 18.0
    growth_rate: float = 1.1


@dataclass
class BoiSizingParams:
    max: float = 100.0
    growth_rate: float = 1.1
