from pathlib import Path

GEOMETRY = Path(__file__).resolve().parent.parent

RESULTS = GEOMETRY / "results"

RESULTS.mkdir() if not RESULTS.is_dir() else None

AIRFOIL_MODEL = GEOMETRY / "airfoil_model" / "airfoil6412.step"
