from pathlib import Path

GEOMETRY = Path(__file__).resolve().parent.parent

RESULTS = GEOMETRY / "results"

AIRFOIL_MODEL = GEOMETRY / "airfoil_model"

AIRFOIL_MODEL_2D = AIRFOIL_MODEL / "2D"
AIRFOIL_MODEL_3D = AIRFOIL_MODEL / "3D"

RESULTS_MODEL_2D = RESULTS / "model_2D"
RESULTS_MODEL_3D = RESULTS / "model_3D"

RESULTS.mkdir() if not RESULTS.is_dir() else None
AIRFOIL_MODEL.mkdir() if not AIRFOIL_MODEL.is_dir() else None
AIRFOIL_MODEL_2D.mkdir() if not AIRFOIL_MODEL_2D.is_dir() else None
AIRFOIL_MODEL_3D.mkdir() if not AIRFOIL_MODEL_3D.is_dir() else None
RESULTS_MODEL_2D.mkdir() if not RESULTS_MODEL_2D.is_dir() else None
RESULTS_MODEL_3D.mkdir() if not RESULTS_MODEL_3D.is_dir() else None
