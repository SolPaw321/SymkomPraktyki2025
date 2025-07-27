from dataclasses import dataclass

"""
Dataclass for mesh utility global params.
"""


@dataclass
class MeshUtilParams:
    min_size: float = 90.0
    max_size: float = 100.0
    generate_quads: bool = True
