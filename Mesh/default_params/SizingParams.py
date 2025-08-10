from dataclasses import dataclass


"""
Dataclasses for global sizing params by sizing type.
"""


@dataclass
class GlobalSizingParams:
    min: float = 5.0
    max: float = 3000.0
    growth_rate: float = 1.1


@dataclass
class CurvatureSizingParams:
    min: float = 10.0
    max: float = 100.0
    normal_angle: float = 18.0
    growth_rate: float = 1.1


@dataclass
class BoiSizingParams:
    max: float = 250.0
    growth_rate: float = 1.1
