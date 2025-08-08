# Instalation
Project instalation using:
```bash
git clone git+https://github.com/SolPaw321/SymkomPraktyki2025.git
```

Dependencies:
```bash
pip install ansys-geometry-core[all]==0.11.0
pip install ansys-meshing-prime[all]==0.9.0
pip install ansys-fluent-core==0.33.0
```

# Important note before use
The geometry allows for the generation of a vertical-axis wind turbine model in both 3D and 2D versions.

Full meshing currently works only for the previously generated 3D model. Work on this is ongoing.

The airflow simulation has not been completed. There is an unresolved issue with extremely high velocities resulting from fluid rotation.

# Usage
The model is generated in Discovery within the file ...
```bash
Geometry/main.py
```

The mesh is created in the file ...
```bash
Mesh/main.py
```

The simulation is performed in Fluent using the file ...
```bash
Fluent/main.py
```

# User Modification Options
### Geometry
The user can:
- Choose the model variant (`2D` or `3D`)
- Generate blade profiles using a built-in function that calculates the points, or upload a custom model to:
  - `Geometry/airfoil_model/2D/` for 2D models
  - `Geometry/airfoil_model/3D/` for 3D models
- Set the number of blades
- Define the angle of attack
- Specify the radius of the circle on which the blades are arranged
- Set the width of the ring in which the blades are immersed









