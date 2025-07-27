from dataclasses import dataclass

"""
Dataclass for prism global params.
"""


@dataclass
class PrismParams:
    n_layers: int = 5
    first_height: float = 0.5
    growth_rate: float = 1.2
