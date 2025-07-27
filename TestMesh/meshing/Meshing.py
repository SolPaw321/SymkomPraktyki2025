from TestMesh.Client import PrimeClient
from TestMesh.meshing.MeshingParams import MeshingParams
import ansys.meshing.prime as prime
from ansys.meshing.prime.graphics.plotter import PrimePlotter
from ansys.meshing.prime.core.sizecontrol import SizeControl
from TestMesh.misc.PATHS import MODEL_2D, MODEL_3D
from ansys.meshing.prime.lucid.mesh_util import Mesh
from ansys.meshing.prime import ScopeDefinition
from ansys.meshing.prime.core.volumecontrol import VolumeControl
from ansys.meshing.prime.core.prismcontrol import PrismControl


class Meshing(PrimeClient, MeshingParams):
    def __init__(self):
        # initialize class inheritance
        PrimeClient.__init__(self)
        MeshingParams.__init__(self)

        self._model = self.client.model
        self._mesh_util = prime.lucid.Mesh(model=self._model)

        self.__set_global_sizing_params()

    def __set_global_sizing_params(self):
        """
        Set prime global sizing params.

        """
        dict_ = self.global_s_d_p.__dict__
        self._model.set_global_sizing_params(
            prime.GlobalSizingParams(
                model=self._model,
                **dict_
            )
        )

    def diagnostic(self):
        """
        Diagnose mode by free edges and intersections.

        """
        print("Diagnosing...")
        self._mesh_util.connect_faces(tolerance=0.02)

        # Diagnostics
        surf_diagnostic = prime.SurfaceSearch(self._model)
        surf_report = surf_diagnostic.get_surface_diagnostic_summary(
            prime.SurfaceDiagnosticSummaryParams(
                model=self._model,
                compute_free_edges=True,
                compute_self_intersections=True,
            )
        )
        print(f"Total number of free edges present is {surf_report.n_free_edges}")

    def read_geometry(self,
                      file_name: str):
        """
        Read geometry from file.

        Args:
            file_name (str): name of your file (with extension)
        """
        if not ("." in file_name):
            raise FileExistsError("Add extension to your model name.")

        print("Reading...")

        path = MODEL_3D if self._model_type == "3D" else MODEL_2D
        path += file_name
        self._mesh_util.read(file_name=str(path))

    def create_surface_mesh(self,
                            part_expression: str = "*",
                            entity_expression: str = "*"):
        """
        Create surface mesh and set a scope.

        Args:
            part_expression (str): part expression to scope parts while evaluating scope
            entity_expression (str): label or zone expression to scope entities while evaluating scope
        """
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
        """
        Create surface mesh with size control and set a scope.

        Args:
            part_expression (str): part expression to scope parts while evaluating scope
            label_expression (str): label or zone expression to scope entities while evaluating scope
            size_control_names (str): name pattern for the size controls
            generate_quads (bool): whether to generate a quad dominant mesh

        Return:
            ScopeDefinition: the scope
        """
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
        """
           Create curvature size control and set a scope.

           Args:
               suggested_name (str): local suggested name for the size control
               min_local (float | None): local minimum size used for computing edge and face size using curvature size control
               max_local (float | None): local maximum size used for computing edge and face size using curvature size control
               normal_angle_local (float | None): local maximum allowable angle at which one element edge may span
               growth_rate_local (float | None): local growth rate used for transitioning from one element size to neighbor element size

           Return:
               SizeControl: the curvature size control
           """
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
        """
           Create body of influence size control and set a scope.

           Args:
               suggested_name (str): local suggested name for the size control
               max_local (float | None): local maximum size used for computing edge and face size using boi size control
               growth_rate_local (float | None): local growth rate used for transitioning from one element size to neighbor element size

           Return:
               SizeControl: the body of influence size control
           """
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
        """
           Create proximity size control and set a scope.

           Args:
               suggested_name (str): local suggested name for the size control
               min_local (float | None): local minimum size used for computing edge and face size using proximity size control
               max_local (float | None): local maximum size used for computing edge and face size using proximity size control
               growth_rate_local (float | None): local growth rate used for transitioning from one element size to neighbor element size
               elements_per_gap_local (float | None): the number of elements per gap can be a real value
               ignore_orientation_local (bool | None): the ignore orientation option can be used to ignore the face normal orientation during the proximity calculation
               ignore_self_proximity_local (bool | None): ignore proximity within zonelets

           Return:
               SizeControl: the curvature size control
           """
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

    def compute_volumetric_size_field(self,
                                      curvature_size_control: SizeControl,
                                      curvature_size_control_global: SizeControl):
        compute_size = prime.SizeField(self._model)
        vol_sf_params = prime.VolumetricSizeFieldComputeParams(self._model)
        compute_size.compute_volumetric(
            size_control_ids=[curvature_size_control.id, curvature_size_control_global.id],
            volumetric_sizefield_params=vol_sf_params
        )

    def create_face_zones_per_label(self):
        for part in self._model.parts:
            for label in part.get_labels():
                self._mesh_util.create_zones_from_labels(
                    label_expression=label
                )

    def compute_volumes(self):
        for part in self._model.parts:
            self._mesh_util.compute_volumes(
                part_expression=part.name,
                create_zones_per_volume=True
            )

    def create_volume_control_(self,
                               zone_expression: str) -> VolumeControl:
        volume_control = self._model.control_data.create_volume_control()
        volume_control.set_params(
            prime.VolumeControlParams(
                model=self._model,
                cell_zonelet_type=prime.CellZoneletType.DEAD,
            )
        )
        volume_control.set_scope(
            prime.ScopeDefinition(
                model=self._model,
                evaluation_type=prime.ScopeEvaluationType.ZONES,
                zone_expression=zone_expression
            )
        )
        return volume_control

    def create_prism_control_(self,
                              label_expression: str,
                              zone_expression: str,
                              n_layers_local: int | None = None,
                              first_height_local: float | None = None,
                              growth_rate_local: float | None = None):
        prism_control = self._model.control_data.create_prism_control()
        prism_control.set_surface_scope(
            prime.ScopeDefinition(
                model=self._model,
                evaluation_type=prime.ScopeEvaluationType.LABELS,
                entity_type=prime.ScopeEntity.FACEZONELETS,
                label_expression=label_expression,
            )
        )
        prism_control.set_volume_scope(
            prime.ScopeDefinition(
                model=self._model,
                evaluation_type=prime.ScopeEvaluationType.ZONES,
                entity_type=prime.ScopeEntity.VOLUME,
                zone_expression=zone_expression,
            )
        )
        prism_control.set_growth_params(
            prime.PrismControlGrowthParams(
                model=self._model,
                offset_type=prime.PrismControlOffsetType.UNIFORM,
                n_layers=n_layers_local if n_layers_local else self.prism_d_p.n_layers,
                first_height=first_height_local if first_height_local else self.prism_d_p.first_height,
                growth_rate=growth_rate_local if growth_rate_local else self.prism_d_p.growth_rate
            )
        )
        return prism_control

    def generate_volume_mesh(self,
                             prism_control: PrismControl,
                             volume_control: VolumeControl):
        volume_mesh = prime.AutoMesh(self._model)
        auto_mesh_param = prime.AutoMeshParams(
            model=self._model,
            prism_control_ids=[prism_control.id],
            size_field_type=prime.SizeFieldType.VOLUMETRIC,
            volume_fill_type=prime.VolumeFillType.HEXCOREPOLY,
            volume_control_ids=[volume_control.id],
        )

        for part in self._model.parts:
            volume_mesh.mesh(part.id, auto_mesh_param)

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
                            size_controls: list[SizeControl] | SizeControl,):
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
