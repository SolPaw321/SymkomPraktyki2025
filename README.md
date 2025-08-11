# Info
### Topic: Wind Turbine Modeling

Objective: To develop a detailed tutorial in the form of a PowerPoint presentation demonstrating the process of preparing geometry, meshing, and conducting parametric simulations of a vertical-axis wind turbine (VAWT) in the PyAnsys environment, with the aim of performing calculations in an automated manner.

### Format
Presentation prepared using the provided Symkom template.

### Structure
The tutorial should present all stages in sequence and include:
- Required Python code with commentary and essential notes from the user’s perspective
- Screenshots of the generated geometry
- Screenshots of the generated computational mesh

The code snippet on each slide should correspond directly to the visuals and commentary presented.

Steps to include: Modeling of a VAWT where the user can control:
- Number of blades
- Blade pitch angle
- Airfoil profile type
- Blade length
- Distance of blades from the center

The turbine’s center should be positioned at the origin of the coordinate system, with the airfoil extruded along the Z-axis. The geometry should include an additional volume with a refinement field (Body of Influence). The recommended meshing algorithm is Sweep/Multizone.

Simulation in Fluent should involve parametric analysis for varying:
- Geometries
- Wind inlet velocities
- Turbine rotational speeds

During the analysis, the user should have access to reports from each simulation showing residuals, torque and power on the turbine, rotational speed, and mass balance. Based on the simulations, the user should be able to assess their reliability and perform the necessary post-processing, with the option to preview the velocity magnitude contour in the domain every n iterations.

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
pip install numpy==2.2.6
```

This project is working with 25R2 ANSYS environment.

# Important note before use
The geometry allows for the generation of a vertical-axis wind turbine model in both 3D and 2D versions. Also, we do not recommend changing the names of components.

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
- Generate blade profiles using a built-in function that calculates the points from provided NACA 4-digit code, or upload a custom model to:
  - `Geometry/airfoil_model/2D/` for 2D models
  - `Geometry/airfoil_model/3D/` for 3D models
- Set the number of blades
- Define the angle of attack
- Specify the radius of the circle on which the blades are arranged
- Set the width (spread) of the ring in which the blades are immersed

All of the above options are available in the file `Geometry/main.py`.


### Meshing
The user can:
- modify default parameters for global, curvature, and BOI sizing, e.g., minimum and maximum cell size, growth rate
  - manualy in `Mesh/default_params/SizingParams.py` file
  - using setters, e.g. `Meshing.set_curvature_s_d_p(...)`
- modify default prism control parameters, such as number of layers, first layer height, and growth rate
  - manualy in `Mesh/default_params/PrismParams.py` file
  - using setter `Meshing.set_prism_s_d_p(...)`
- modify default parameters for the `prime.lucid.Mesh` module
  - manualy in `Mesh/default_params/MeshUtilParams.py`
  - using setter `Meshing.set_mesh_util_d_p(...)`
- override all the above parameters locally using dedicated functions, e.g. `Meshing.create_curvature_size_control(name, min_local=10.0, max_local=100.0)`


### Fluent
Currently supports only inlet velocity and rpm.

# Presentation
Link: [Google Slieds](https://docs.google.com/presentation/d/1TS15-3GZw-e-8NaHIuEBRMNa9NwjnkPU/edit?usp=sharing&ouid=101068504685084610320&rtpof=true&sd=true)

# TODO
- #### Resolve the issue of unrealistically high velocities in the Fluent simulation (bug probably related to topology sharing in Fluent stage)
- Create a complete mesh for the 2D model (prism layers or multizones)
- Implement parameter checks (e.g., the maximum number of blades allowed for a given circle radius to prevent blade overlap)
- Validate the size of the blade model provided by the user
- Finalize validation of user input data
- Implement checks for user-defined names
- Allow the user to select the meshing method (TET, HEX, POLY, or quadratic)
- Add the option to generate user-defined reports and plots (UDF)
- Finalize parameterization of initial conditions selected by the user
- Add single file to run geometry, meshing and simulation in a single run
- Allow the user to select number of processor in Fluent (default is 2) to speed up simulation process
- Add some unittesting with examples












