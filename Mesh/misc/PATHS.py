from pathlib import Path
from Geometry.misc.PATHS import RESULTS_MODEL_2D as GEOMETRY_MODEL_2D
from Geometry.misc.PATHS import RESULTS_MODEL_3D as GEOMETRY_MODEL_3D


ANSYS_PRIME = r"D:\ansys_student\ANSYS Inc\ANSYS Student\v252\meshing\Prime"

TEST_MESH = Path(__file__).resolve().parent.parent

RESULTS = TEST_MESH / "results"

MESH_2D = RESULTS / "mesh_2d"
MESH_3D = RESULTS / "mesh_3d"

RESULTS.mkdir() if not RESULTS.is_dir() else None
MESH_2D.mkdir() if not MESH_2D.is_dir() else None
MESH_3D.mkdir() if not MESH_3D.is_dir() else None
