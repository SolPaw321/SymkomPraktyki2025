from dataclasses import dataclass


@dataclass
class MeshUtilParams:
    min_size: float = 0.1
    max_size: float = 1.0
    generate_quads: bool = True
