from Mesh.meshing.Meshing import Meshing

# --- User Params --- #
model_type = "3D"
airfoil_model = "airfoil6412.fmd"  # airfoil model (Geometry/results/model_3D)
save_file_name = "wind_turbine"


# --- Initialize Meshing class --- #
meshing = Meshing(model_type)

# --- Read geometry and diagnose --- #
meshing.read_geometry(airfoil_model)
meshing.diagnostic()


# --- Create global curvature sizing control --- #
global_curvature = meshing.create_curvature_sizing_control("global_curvature", min_local=150.0, max_local=3000.0)
meshing.set_scope(global_curvature, part_expression="* !boi", label_expression="*")

# --- Create ring curvature sizing control --- #
ring_curvature = meshing.create_curvature_sizing_control("ring_curvature", min_local=20.0, max_local=200.0)
meshing.set_scope(ring_curvature, part_expression="*fluid-2*", label_expression="wall")

# --- Create body of influence sizing control --- #
boi_sizing = meshing.create_boi_sizing_control("boi_sizing")
meshing.set_scope(boi_sizing, part_expression="boi")

# --- Compute volumetric using curvature sizing controls --- #
meshing.compute_volumetric([global_curvature, ring_curvature])

# --- Create surface mesh with curvature sizing controls --- #
meshing.create_surface_mesh_with_size_control(size_control_names="*")


# --- Create zones from labels  --- #
meshing.create_zones_from_all_labels()

# --- Get a ring part --- #
part = meshing.get_part_by_name("fluid-2")

# --- Compute volume on ring --- #
meshing.compute_volumes(part_expression=part.name)

# --- Create volume and prism control --- #
volume_control = meshing.create_volume_control_(zone_expression="*fluid-*")
prism_control = meshing.create_prism_control_(zone_expression="fluid-2", label_expression="wall")

# --- Generate prism mesh --- #
meshing.generate_volume_mesh(part, prism_control=prism_control, volume_control=volume_control)

# -- Display and save results --- #
meshing.print_all_parts_summary()
scope = meshing.construct_scope("* !boi")
meshing.plot(scope=scope)
meshing.save(save_file_name)
meshing.exit()
