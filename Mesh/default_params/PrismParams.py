from dataclasses import dataclass

"""
Dataclass for prism global params.
"""


@dataclass
class PrismParams:
    n_layers: int = 40
    first_height: float = 0.1
    growth_rate: float = 1.1
