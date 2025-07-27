from pathlib import Path

GEOMETRY = Path(__file__).resolve().parent.parent

RESULTS = GEOMETRY / "results"

AIRFOIL_MODEL = GEOMETRY / "airfoil_model" #/ "airfoil6412.step"

AIRFOIL_MODEL_2D = AIRFOIL_MODEL / "2D"
AIRFOIL_MODEL_3D = AIRFOIL_MODEL / "3D"

RESULTS.mkdir() if not RESULTS.is_dir() else None
AIRFOIL_MODEL.mkdir() if not AIRFOIL_MODEL.is_dir() else None
AIRFOIL_MODEL_2D.mkdir() if not AIRFOIL_MODEL_2D.is_dir() else None
AIRFOIL_MODEL_3D.mkdir() if not AIRFOIL_MODEL_3D.is_dir() else None
