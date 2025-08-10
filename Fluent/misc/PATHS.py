from pathlib import Path
from config import ANSYS_PATH

FLUENT = Path(__file__).resolve().parent.parent

MESH = FLUENT.parent / "Mesh"

MESH_3D = MESH / 'results' / 'mesh_3d'

WORK_DIR = FLUENT / "work_directory"

FLUENT_PATH = Path(ANSYS_PATH) / Path("fluent")
