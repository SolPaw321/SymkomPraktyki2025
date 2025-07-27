from TestMesh.meshing.Meshing import Meshing
from ansys.meshing.prime import ScopeDefinition

meshing = Meshing()
# meshing.create_surface_mesh(part_expression="!boi")
meshing.read_geometry()
meshing.diagnostic()


boi_sizing = meshing.create_boi_sizing_control("boi_sizing")
meshing.set_scope(boi_sizing, part_expression="boi")

curvature_sizing = meshing.create_curvature_sizing_control("fluid_1_3_curvature")
meshing.set_scope(curvature_sizing, part_expression="1,3")

curvature_sizing = meshing.create_curvature_sizing_control("fluid_2_curvature", min_local=30)
meshing.set_scope(curvature_sizing, part_expression="2")

'''proximity_sizing = meshing.create_proximity_sizing_control("global_proximity")
meshing.set_scope(proximity_sizing, part_expression="!boi")

meshed_sizing = meshing.create_meshed_sizing_control("global_meshed")
meshing.set_scope(meshed_sizing, part_expression="!boi")'''

# meshing.create_surface_mesh()
meshing.create_surface_mesh_with_size_control(generate_quads=False)

# meshing.create_surfer(curvature_sizing)

meshing.all_parts_summary_results()

scope = meshing.construct_scope("!boi")
#
meshing.plot(scope)
meshing.exit()
