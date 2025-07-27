from pathlib import Path


TEST_MESH = Path(__file__).resolve().parent.parent

MODEL = TEST_MESH / 'model'

MODEL_2D = MODEL / '2D'
MODEL_3D = MODEL / '3D'

MODEL.mkdir() if not MODEL.is_dir() else None
MODEL_2D.mkdir() if not MODEL_2D.is_dir() else None
MODEL_3D.mkdir() if not MODEL_3D.is_dir() else None

ANSYS_PRIME = r"D:\programy\ansys\ANSYS Inc\v251\meshing\Prime"
# ANSYS_Prime = r"C:\Program Files\ANSYS Inc\v251\meshing\Prime"  # dafault path
