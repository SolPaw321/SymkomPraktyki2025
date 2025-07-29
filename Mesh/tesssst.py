import os
import tempfile

from ansys.meshing import prime
from ansys.meshing.prime.graphics import PrimePlotter





multizone_control = model.control_data.create_multi_zone_control()





volume_scope = prime.ScopeDefinition(
    model=model,
    entity_type=prime.ScopeEntity.VOLUME,
    evaluation_type=prime.ScopeEvaluationType.ZONES,
    part_expression="*",
    label_expression="*",
    zone_expression="solid1",
)

multizone_control.set_volume_scope(volume_scope)

surface_scope = prime.ScopeDefinition(
    model=model,
    entity_type=prime.ScopeEntity.FACEZONELETS,
    evaluation_type=prime.ScopeEvaluationType.ZONES,
    part_expression="*",
    label_expression="*",
    zone_expression="*",
)

multizone_control.set_surface_scope(surface_scope)







sizing_params = prime.MultiZoneSizingParams(model)
sizing_params.max_size = 1
sizing_params.min_size = 0.04
sizing_params.growth_rate = 1.2
multizone_control.set_multi_zone_sizing_params(sizing_params)
parts = model.parts
autoMesher = prime.AutoMesh(model)
autoMeshParams = prime.AutoMeshParams(model)
autoMeshParams.multi_zone_control_ids = [multizone_control.id]

for p in parts:
    result = autoMesher.mesh(p.id, autoMeshParams)
    print(result)




# Surface mesh with triangular elements of uniform size
surfer_params = prime.SurferParams(model=model, constant_size=1.0)
surfer_result = prime.Surfer(model).mesh_topo_faces(
    part.id, topo_faces=part.get_topo_faces(), params=surfer_params
)



