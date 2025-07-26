from TestMesh.Client import Client
from TestMesh.meshing.MeshingParams import MeshingParams
import ansys.meshing.prime as prime
from ansys.meshing.prime.graphics.plotter import PrimePlotter
from ansys.meshing.prime.core.sizecontrol import SizeControl
from TestMesh.misc.PATHS import Model_stp_file
from ansys.meshing.prime.lucid.mesh_util import Mesh
from ansys.meshing.prime import ScopeDefinition


class Meshing(Client, MeshingParams):
    def __init__(self):
        Client.__init__(self)
        MeshingParams.__init__(self)

        self._model = self.client.model
        self._mesh_util = prime.lucid.Mesh(model=self._model)

        self.__set_global_sizing_params()

    def __set_global_sizing_params(self):
        dict_ = self.global_s_d_p.__dict__
        self._model.set_global_sizing_params(
            prime.GlobalSizingParams(
                model=self._model,
                **dict_
            )
        )

    def diagnostic(self):
        print("Diagnosing...")
        self._mesh_util.connect_faces(tolerance=0.02)

        # Diagnostics
        surf_diagnostic = prime.SurfaceSearch(self._model)
        surf_report = surf_diagnostic.get_surface_diagnostic_summary(
            prime.SurfaceDiagnosticSummaryParams(
                self._model,
                compute_free_edges=True,
                compute_self_intersections=True,
            )
        )
        print(f"Total number of free edges present is {surf_report.n_free_edges}")

    def read_geometry(self):
        print("Reading...")
        self._mesh_util.read(file_name=str(Model_stp_file))
        # file_io = prime.FileIO(model=self._model)
        # default_params = prime.ImportCadParams(model=self._model)
        # results = file_io.import_cad(str(Model_stp_file), default_params=default_params)
        # print(results)

    def create_surface_mesh(self,
                            part_expression: str = "*",
                            entity_expression: str = "*"):
        scope = prime.lucid.SurfaceScope(
            part_expression=part_expression,
            entity_expression=entity_expression  # ,
            # scope_evaluation_type=prime.ScopeEvaluationType.LABELS,
        )

        dict_ = self.mesh_util_d_p.__dict__
        self._mesh_util.surface_mesh(**dict_, scope=scope)

    def create_surface_mesh_with_size_control(self,
                                              part_expression: str = "*",
                                              label_expression: str = "*",
                                              size_control_names: str = "*",
                                              generate_quads: bool = False) -> prime.ScopeDefinition:
        scope = prime.ScopeDefinition(
            model=self._model,
            part_expression=part_expression,
            label_expression=label_expression
        )
        self._mesh_util.surface_mesh_with_size_controls(
            size_control_names=size_control_names,
            generate_quads=generate_quads
        )
        return scope

    def create_curvature_sizing_control(self,
                                        suggested_name: str,
                                        min_local: float | None = None,
                                        max_local: float | None = None,
                                        normal_angle_local: float | None = None,
                                        growth_rate_local: float | None = None) -> SizeControl:
        size_control = self._model.control_data.create_size_control(prime.SizingType.CURVATURE)
        size_control.set_curvature_sizing_params(
            prime.CurvatureSizingParams(
                model=self._model,
                min=min_local if min_local else self.curvature_s_d_p.min,
                max=max_local if max_local else self.curvature_s_d_p.max,
                normal_angle=normal_angle_local if normal_angle_local else self.curvature_s_d_p.normal_angle,
                growth_rate=growth_rate_local if growth_rate_local else self.curvature_s_d_p.growth_rate
            )
        )
        size_control.set_suggested_name(suggested_name)
        # self.wrap_sizing_control(size_control)
        return size_control

    def create_boi_sizing_control(self,
                                  suggested_name: str,
                                  max_local: float | None = None,
                                  growth_rate_local: float | None = None) -> SizeControl:
        size_control = self._model.control_data.create_size_control(prime.SizingType.BOI)
        size_control.set_boi_sizing_params(
            prime.BoiSizingParams(
                model=self._model,
                max=max_local if max_local else self.boi_s_d_p.max,
                growth_rate=growth_rate_local if growth_rate_local else self.boi_s_d_p.growth_rate
            )
        )
        size_control.set_suggested_name(suggested_name)
        # self.wrap_sizing_control(size_control)
        return size_control

    def create_proximity_sizing_control(self,
                                        suggested_name: str,
                                        min_local: float | None = None,
                                        max_local: float | None = None,
                                        growth_rate_local: float | None = None,
                                        elements_per_gap_local: float | None = None,
                                        ignore_orientation_local: bool | None = None,
                                        ignore_self_proximity_local: bool | None = None) -> SizeControl:
        size_control = self._model.control_data.create_size_control(prime.SizingType.PROXIMITY)
        size_control.set_proximity_sizing_params(
            prime.ProximitySizingParams(
                model=self._model,
                min=min_local if min_local else self.proximity_s_d_p.min,
                max=max_local if max_local else self.proximity_s_d_p.max,
                growth_rate=growth_rate_local if growth_rate_local else self.proximity_s_d_p.growth_rate,
                elements_per_gap=elements_per_gap_local if elements_per_gap_local else self.proximity_s_d_p.elements_per_gap,
                ignore_orientation=ignore_orientation_local if ignore_self_proximity_local else self.proximity_s_d_p.ignore_orientation,
                ignore_self_proximity=ignore_self_proximity_local if ignore_self_proximity_local else self.proximity_s_d_p.ignore_self_proximity,
            )
        )
        size_control.set_suggested_name(suggested_name)

        # self.wrap_sizing_control(size_control)
        return size_control

    def create_meshed_sizing_control(self,
                                     suggested_name: str,
                                     growth_rate_local_: float | None = None):
        size_control = self._model.control_data.create_size_control(prime.SizingType.MESHED)
        size_control.set_meshed_sizing_params(
            prime.MeshedSizingParams(
                model=self._model,
                growth_rate=growth_rate_local_ if growth_rate_local_ else self._meshed_s_d_p.growth_rate
            )
        )
        size_control.set_suggested_name(suggested_name)
        return size_control

    def create_surfer(self, size_control):
        size_field = prime.SizeField(self._model)
        res = size_field.compute_volumetric(
            size_control_ids=[size_control.id],
            volumetric_sizefield_params=prime.VolumetricSizeFieldComputeParams(
                self._model,
                enable_multi_threading=False
            )

        )

        surfer_params = prime.SurferParams(
            model=self._model,
            size_field_type=prime.SizeFieldType.VOLUMETRIC
        )

        part = self._model.get_part_by_name("fluid-2")

        surfer_result = prime.Surfer(self._model).mesh_topo_faces(
            part_id=part.id,
            topo_faces=part.get_topo_faces(),
            params=surfer_params
        )

    def set_scope(self,
                  size_control: SizeControl,
                  part_expression: str = "*",
                  label_expression: str = "*"):
        size_control.set_scope(
            prime.ScopeDefinition(
                model=self._model,
                part_expression=part_expression,
                label_expression=label_expression
            )
        )

    def wrap_sizing_control(self,
                            size_controls: list[SizeControl] | SizeControl,
                            ):
        if type(size_controls) == SizeControl:
            size_controls = [size_controls]

        self._mesh_util.wrap(
            min_size=0.2,
            max_size=1.0,
            input_parts="*",
            use_existing_features=True,
            recompute_remesh_sizes=True,
            remesh_size_controls=size_controls,
        )

    def construct_scope(self, part_expression: str | None):
        return prime.ScopeDefinition(
            model=self._model,
            part_expression=part_expression
        )

    def plot(self, scope: prime.ScopeDefinition | None = None):
        display = PrimePlotter()
        display.plot(self._model, scope=scope)
        display.show()

    def get_all_parts(self):
        return [part.name for part in self._model.parts]

    def get_all_labels(self):
        return [part.get_labels() for part in self._model.parts]

    def all_parts_summary_results(self):
        for part in self._model.parts:
            print(part.get_summary(prime.PartSummaryParams(model=self._model)))
