from dataclasses import dataclass

"""
Dataclass for prism global params.
"""


@dataclass
class PrismParams:
    n_layers: int = 30
    first_height: float = 0.4
    growth_rate: float = 1.1
