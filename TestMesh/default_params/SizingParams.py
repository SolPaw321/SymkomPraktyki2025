from dataclasses import dataclass


@dataclass
class GlobalSizingParams:
    min: float = 0.1
    max: float = 1.0
    growth_rate: float = 1.1


@dataclass
class CurvatureSizingParams:
    min: float = 0.1
    max: float = 0.9
    normal_angle: float = 18.0
    growth_rate: float = 1.1


@dataclass
class BoiSizingParams:
    max: float = 0.1
    growth_rate: float = 1.1


@dataclass
class ProximitySizingParams:
    min: float = 0.1
    max: float = 0.9
    growth_rate: float = 1.1
    elements_per_gap: float = 3.0
    ignore_orientation: bool = True
    ignore_self_proximity: bool = False


@dataclass
class MeshedSizingParams:
    growth_rate: float = 1.1
