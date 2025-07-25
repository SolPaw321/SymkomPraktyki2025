import os
import tempfile
import ansys.meshing.prime as prime
from ansys.meshing.prime.graphics.plotter import PrimePlotter
from geomdl.construct import extract_surfaces

# 1. Uruchomienie klienta
client = prime.launch_prime(prime_root=r"C:\Program Files\ANSYS Inc\v251\meshing\Prime")
model = client.model

# 2. Zaimportuj model CAD
file_io = prime.FileIO(model=model)
params = prime.ImportCadParams(model=model)
results = file_io.import_cad(r"C:\Users\Symkom\Downloads\M6412.step", params=params)
# results = file_io.import_cad(r"C:\Users\Symkom\ANSW2\SymkomPraktyki2025\model\D2_5\geometry\results\model_2D\Wind_Turbine.stp", params=params)

# 3. Pobierz pierwszą część
# part = model.parts[0]

display = PrimePlotter()
display.plot(model)
display.show()

print(model)



#--------------------------# 2d

#
# mesh_util = prime.lucid.Mesh(model=model)
#
# mesh_util.surface_mesh(min_size=0.2, max_size=20)
#
# mesh_util.volume_mesh(
#     volume_fill_type=prime.VolumeFillType.TET,
#     prism_surface_expression="* !inlet !outlet",
#     prism_layers=8,
# )
# ----------------------------------------------



# Set the global sizing parameters after importing the model

model.set_global_sizing_params(
    prime.GlobalSizingParams(model=model, min=1, max=12, growth_rate=1.1)
)

model.delete_volumetric_size_fields(model.get_active_volumetric_size_fields())
part = model.parts[0]




sweeper = prime.VolumeSweeper(model)
stacker_params = prime.MeshStackerParams(
    model=model, direction=[0.0, 0.0, 1.0], max_offset_size=10, delete_base=True
)

print(stacker_params)




createbase_results = sweeper.create_base_face(
    part_id=part.id, topo_volume_ids=part.get_topo_volumes(), params=stacker_params
)

base_faces = createbase_results.base_face_ids




size_field = prime.SizeField(model)
res = size_field.compute_volumetric(
    size_control_ids=createbase_results.size_control_ids,
    volumetric_sizefield_params=prime.VolumetricSizeFieldComputeParams(model),
)
surfer_params = prime.SurferParams(
    model=model, size_field_type=prime.SizeFieldType.VOLUMETRIC, generate_quads=True, min_size=0.1, max_size=10, project_on_geometry=True
)
meshbase_result = prime.Surfer(model).mesh_topo_faces(
    part_id=part.id, topo_faces=base_faces, params=surfer_params
)

print(surfer_params)
# - model=powierzchnia z profilami
# - BOI



stackbase_results = sweeper.stack_base_face(
    part_id=part.id,
    base_face_ids=base_faces,
    topo_volume_ids=part.get_topo_volumes(),
    params=stacker_params,
)

pl = PrimePlotter()
pl.plot(model, update=True)
pl.show()

# -------------------------------------------------------------
extract_surfaces(pvol=model)


client.exit()