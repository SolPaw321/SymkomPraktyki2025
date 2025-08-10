from dataclasses import dataclass

"""
Dataclass for mesh utility global params.
"""


@dataclass
class MeshUtilParams:
    min_size: float = 30.0
    max_size: float = 80.0
