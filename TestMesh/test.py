import os
import tempfile

import ansys.meshing.prime as prime
from ansys.meshing.prime.graphics import PrimePlotter
from misc.PATHS import ANSYS_Prime

prime_client = prime.launch_prime(prime_root=ANSYS_Prime, timeout=120)
model = prime_client.model
mesh_util = prime.lucid.Mesh(model=model)

f1_rw_drs = prime.examples.download_f1_rw_drs_stl()
f1_rw_enclosure = prime.examples.download_f1_rw_enclosure_stl()
f1_rw_end_plates = prime.examples.download_f1_rw_end_plates_stl()
f1_rw_main_plane = prime.examples.download_f1_rw_main_plane_stl()

print("Reading...")
for file_name in [
    f1_rw_drs,
    f1_rw_enclosure,
    f1_rw_end_plates,
    f1_rw_main_plane
]:
    mesh_util.read(file_name, append=True)

print([part.name for part in model.parts])
print([part.get_labels() for part in model.parts])

# Define global sizes
model.set_global_sizing_params(prime.GlobalSizingParams(model, min=4, max=32, growth_rate=1.2))

# Create label per part
for part in model.parts:
    part.add_labels_on_zonelets([part.name.split(".")[0]], part.get_face_zonelets())

# Merge parts
merge_params = prime.MergePartsParams(model, merged_part_suggested_name="f1_car_rear_wing")
merge_result = model.merge_parts([part.id for part in model.parts], merge_params)
part = model.get_part_by_name(merge_result.merged_part_assigned_name)

print([part.name for part in model.parts])
print([part.get_labels() for part in model.parts])

# Connect faces
mesh_util.connect_faces(part.name, face_labels="*", target_face_labels="*", tolerance=0.02)

# Diagnostics
surf_diag = prime.SurfaceSearch(model)
surf_report = surf_diag.get_surface_diagnostic_summary(
    prime.SurfaceDiagnosticSummaryParams(
        model,
        compute_free_edges=True,
        compute_self_intersections=True,
    )
)
print(f"Total number of free edges present is {surf_report.n_free_edges}")



# display the rear wing geometry without the enclosure
scope = prime.ScopeDefinition(model, part_expression="* !*enclosure*")
display = PrimePlotter()
display.plot(model, scope)
display.show()

prime_client.exit()