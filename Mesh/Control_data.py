import os
import tempfile
import ansys.meshing.prime as prime
from ansys.meshing.prime.graphics.plotter import PrimePlotter
from ansys.meshing.prime import BoundaryFittedSpline
from six import create_bound_method

# 1. Uruchomienie klienta
client = prime.launch_prime(prime_root=r"C:\Program Files\ANSYS Inc\v251\meshing\Prime")
model = client.model

# 2. Zaimportuj model CAD
file_io = prime.FileIO(model=model)
params = prime.ImportCadParams(model=model)
results = file_io.import_cad(r"C:\Users\Symkom\Downloads\M6412.fmd", params=params)
# results = file_io.import_cad(r"C:\Users\Symkom\ANSW2\SymkomPraktyki2025\model\D2_5\geometry\results\model_2D\Wind_Turbine.stp", params=params)

# 3. Pobierz pierwszą część
# part = model.parts[0]

display = PrimePlotter()
display.plot(model)
display.show()

print(model)

print([part.name for part in model.parts])
print([part.get_labels() for part in model.parts])

#--------------------------#


# Set the global sizing parameters after importing the model

model.set_global_sizing_params(
    prime.GlobalSizingParams(model=model, min=1, max=10, growth_rate=1.1)
)
model.delete_volumetric_size_fields(model.get_active_volumetric_size_fields())
part = model.parts[1]

# sweep

sweeper = prime.VolumeSweeper(model)
stacker_params = prime.MeshStackerParams(
    model=model, direction=[0.0, 0.0, 1.0], max_offset_size=10, delete_base=True
)

print(stacker_params)

# Base result

createbase_results = sweeper.create_base_face(
    part_id=part.id, topo_volume_ids=part.get_topo_volumes(), params=stacker_params
)
base_faces = createbase_results.base_face_ids


# Volumetric sizing
size_field = prime.SizeField(model)
res = size_field.compute_volumetric(
    size_control_ids=createbase_results.size_control_ids,
    volumetric_sizefield_params=prime.VolumetricSizeFieldComputeParams(model),
)

surfer_params = prime.SurferParams(
    model=model, size_field_type=prime.SizeFieldType.VOLUMETRIC, generate_quads=True
)
meshbase_result = prime.Surfer(model).mesh_topo_faces(
    part_id=part.id, topo_faces=base_faces, params=surfer_params
)

print(surfer_params)

stackbase_results = sweeper.stack_base_face(
    part_id=part.id,
    base_face_ids=base_faces,
    topo_volume_ids=part.get_topo_volumes(),
    params=stacker_params,
)
# ---------------------------------------------------------------------

# size_control = model.control_data.create_size_control(prime.SizingType.BOI)
# size_control.set_boi_sizing_params(
#     prime.BoiSizingParams(model=model, max=3.0, growth_rate=1.3)
# )
# size_control.set_suggested_name("BOI_control")
# size_control.set_scope(prime.ScopeDefinition(model=model, part_expression="fluid-2"))

# ,part_expression="fluid-2"
# label_expression="*wall*"


# ---------------------CURV------------------------------


# size_control = model.control_data.create_size_control(prime.SizingType.CURVATURE)
# size_control.set_curvature_sizing_params(
#     prime.CurvatureSizingParams(model=model, min=0.1, max=1.0, growth_rate=1.3,use_cad_curvature=True)
# )
# size_control.set_suggested_name("curv_control")
# size_control.set_scope(prime.ScopeDefinition(model=model,label_expression="*wall*"))


# ---------------------PROX-------------------------------------------

# size_control = model.control_data.create_size_control(prime.SizingType.PROXIMITY)
# size_control.set_proximity_sizing_params(
#     prime.ProximitySizingParams(
#         model=model,
#         min=0.1,
#         max=2.0,
#         growth_rate=1.3,
#         elements_per_gap=6.0,
#         ignore_orientation=True,
#         ignore_self_proximity=False,
#     )
# )
# size_control.set_suggested_name("prox_control")
# size_control.set_scope(prime.ScopeDefinition(model=model,label_expression="*wall*"))
#
#
#
#
#
#
# size_field = prime.SizeField(model)
# res = size_field.compute_volumetric(
#     size_control_ids=[size_control.id],
#     volumetric_sizefield_params=prime.VolumetricSizeFieldComputeParams(
#         model, enable_multi_threading=False
#     ),
# )
#
# surfer_params = prime.SurferParams(
#     model=model,
#     size_field_type=prime.SizeFieldType.VOLUMETRIC,
#     generate_quads=True,
#     project_on_geometry=True
# )
#
# surfer_result = prime.Surfer(model).mesh_topo_faces(
#     part_id=model.parts[0].id,
#     topo_faces=model.parts[0].get_topo_faces(),
#     params=surfer_params,
# )

mesh_util = prime.lucid.Mesh(model=model)
mesh_util.surface_mesh(min_size=5, max_size=20)
mesh_util.volume_mesh(
    volume_fill_type=prime.VolumeFillType.TET,
    prism_surface_expression="* !walls",
    prism_layers=3,
)


# boundary_fitted_spline = BoundaryFittedSpline(model = model)
# results = boundary_fitted_spline.create_boundary_fitted_spline(part_id=model.parts[0].id, cell_zonelet_ids=model.zo(), boundary_fitted_spline_params)

# -------------------------------------------------------------

pl = PrimePlotter()
pl.plot(model, update=True)
pl.show()




client.exit()
