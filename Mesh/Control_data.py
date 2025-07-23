import os
import tempfile
import ansys.meshing.prime as prime
from ansys.meshing.prime.graphics.plotter import PrimePlotter

# 1. Uruchomienie klienta
client = prime.launch_prime(prime_root=r"C:\Program Files\ANSYS Inc\v251\meshing\Prime")
model = client.model

# 2. Zaimportuj model CAD
file_io = prime.FileIO(model=model)
params = prime.ImportCadParams(model=model)
results = file_io.import_cad(r"C:\Users\Symkom\Downloads\T1.step", params=params)
# results = file_io.import_cad(r"C:\Users\Symkom\ANSW2\SymkomPraktyki2025\model\D2_5\geometry\results\model_2D\Wind_Turbine.stp", params=params)

# 3. Pobierz pierwszą część
part = model.parts[0]

display = PrimePlotter()
display.plot(model)
display.show()

print(model)



#--------------------------# 2d
mesh_util = prime.lucid.Mesh(model=model)




size_control = model.control_data.create_size_control(prime.SizingType.CURVATURE)
size_control.set_curvature_sizing_params(
    prime.CurvatureSizingParams(model=model, min=0.2, max=2.0, growth_rate=1.2)
)
size_control.set_suggested_name("curv_control")
size_control.set_scope(prime.ScopeDefinition(model=model))




size_control = model.control_data.create_size_control(prime.SizingType.PROXIMITY)
size_control.set_proximity_sizing_params(
    prime.ProximitySizingParams(
        model=model,
        min=0.1,
        max=2.0,
        growth_rate=1.2,
        elements_per_gap=3.0,
        ignore_orientation=True,
        ignore_self_proximity=False,
    )
)
size_control.set_suggested_name("prox_control")
size_control.set_scope(prime.ScopeDefinition(model=model))




size_control = model.control_data.create_size_control(prime.SizingType.BOI)
size_control.set_boi_sizing_params(
    prime.BoiSizingParams(model=model, max=20.0, growth_rate=1.2)
)
size_control.set_suggested_name("BOI_control")
size_control.set_scope(prime.ScopeDefinition(model=model))


mesh_util.surface_mesh_with_size_controls(size_control_names=("BOI_control"))
#-----------------------# 3d


# automesh_params = prime.AutoMeshParams(
#     model=model,
#     max_size=0.3,
#     volume_fill_type=prime.VolumeFillType.TET,
#     tet=prime.TetParams(model=model, quadratic=True),
# )
#
# print(automesh_params)
#
# prime.AutoMesh(model).mesh(part_id=part.id, automesh_params=automesh_params)
#
# # Volume control
# volume_control = model.control_data.create_volume_control()
# volume_scope = prime.ScopeDefinition(
#     model=model, evaluation_type=prime.ScopeEvaluationType.ZONES, zone_expression="*"
# )
# volume_control.set_scope(volume_scope)
# volume_control.set_params(
#     prime.VolumeControlParams(
#         model=model, cell_zonelet_type=prime.CellZoneletType.FLUID
#     )
# )
#
# # Volume mesh
# automesh_params = prime.AutoMeshParams(
#     model=model,
#     size_field_type=prime.SizeFieldType.VOLUMETRIC,
#     volume_fill_type=prime.VolumeFillType.TET,
#     volume_control_ids=[volume_control.id],
# )
# prime.AutoMesh(model).mesh(part_id=part.id, automesh_params=automesh_params)

# --------------------CHECK



client.exit()
