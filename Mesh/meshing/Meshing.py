from Mesh.Client import PrimeClient
from Mesh.meshing.MeshingParams import MeshingParams
import ansys.meshing.prime as prime
from ansys.meshing.prime import Part
from ansys.meshing.prime.graphics.plotter import PrimePlotter
from ansys.meshing.prime.core.sizecontrol import SizeControl
from Mesh.misc.PATHS import GEOMETRY_MODEL_3D, GEOMETRY_MODEL_2D
from ansys.meshing.prime.lucid.mesh_util import Mesh
from ansys.meshing.prime import ScopeDefinition
from ansys.meshing.prime.core.volumecontrol import VolumeControl
from ansys.meshing.prime.core.prismcontrol import PrismControl
from Mesh.misc.PATHS import MESH_2D, MESH_3D


class Meshing(PrimeClient, MeshingParams):
    def __init__(self, model_type: str):
        self.__validate_model_type(model_type)

        # initialize class inheritance
        PrimeClient.__init__(self)
        MeshingParams.__init__(self)

        self._model_type = model_type.upper()
        self._model = self.client.model
        self._mesh_util: Mesh = prime.lucid.Mesh(model=self._model)

        self.__set_global_sizing_params()

    @staticmethod
    def __validate_model_type(model_type):
        if model_type.upper() != "3D":
            raise NotImplementedError("Meshing for 2D model is not available.")

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
                compute_multi_edges=True,
                compute_duplicate_faces=True
            )
        )
        print(f"Total number of free edges present is {surf_report.n_free_edges}")
        print(f"Total number of multi edges present is {surf_report.n_multi_edges}")
        print(f"Total number of duplicate faces present is {surf_report.n_duplicate_faces}")
        print(f"Total number intersection present is {surf_report.n_self_intersections}")

    def read_geometry(self,
                      file_name: str):
        """
        Read geometry from file.

        Args:
            file_name (str): name of your file (with extension)
        """
        if not ("." in file_name):
            raise FileExistsError("Add extension to your Geometry name.")

        print("Reading...")

        path = GEOMETRY_MODEL_3D if self._model_type == "3D" else GEOMETRY_MODEL_2D
        path = path / file_name

        if file_name.split(".")[1] == "dsco":
            params = prime.ImportCadParams(
                model=self._model, cad_reader_route=prime.CadReaderRoute.DISCOVERY
            )
            prime.FileIO(self._model).import_cad(file_name=str(path), params=params)
        else:
            self._mesh_util.read(
                file_name=str(path)
            )

        for part in self._model.parts:
            part.remove_labels_from_topo_entities([part.name], part.get_topo_faces())

    def create_surface_mesh_with_size_control(self,
                                              part_expression: str | None = "*",
                                              size_control_names: str = "*",
                                              generate_quads: bool = False) -> prime.lucid.SurfaceScope:
        """
        Create surface mesh with size control and set a scope.

        Args:
            part_expression (str): part expression to scope parts while evaluating scope
            size_control_names (str): name pattern for the size controls
            generate_quads (bool): whether to generate a quad dominant mesh

        Return:
            ScopeDefinition: the scope
        """
        scope = prime.lucid.SurfaceScope(
            part_expression=part_expression
        )
        self._mesh_util.surface_mesh_with_size_controls(
            size_control_names=size_control_names,
            generate_quads=generate_quads,
            scope=scope
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

        return size_control

    def create_zones_from_labels(self, part_name: str = "*", label_name: str = "*"):
        """
        Create zones from single label or whole part.

        Args:
            part_name (str): part with at least one label
            label_name (str): label name to create zone
        """
        if label_name == "*":
            # get all labels from part
            part = self._model.get_part_by_name(part_name)
            labels = [label for label in part.get_labels()]
            label_expression = ", ".join(labels)
        else:
            # or simply use given label name
            label_expression = label_name

        # create zones
        self._mesh_util.create_zones_from_labels(label_expression=label_expression)

    def compute_volumes(self, part_expression: str):
        """
        Compute volumes in parts.

        Args:
            part_expression (str): parts for computing volumes.
        """
        self._mesh_util.compute_volumes(
            part_expression=part_expression,
            create_zones_per_volume=False
        )

    def compute_volumetric(self, size_controls: list[SizeControl]):
        """
        Compute volumetric using size controls.

        Args:
            size_controls (list[SizeControl]): list of size controls to compute volumetric
        """
        # initialize size field
        compute_size = prime.SizeField(self._model)

        # initialize params
        vol_sf_params = prime.VolumetricSizeFieldComputeParams(self._model)

        # compute volumetric using size controls
        compute_size.compute_volumetric(
            size_control_ids=[size_control.id for size_control in size_controls],
            volumetric_sizefield_params=vol_sf_params
        )

    def create_volume_control_(self,
                               zone_expression: str) -> VolumeControl:
        """
        Create volume control from zones.

        Args:
            zone_expression (str): zone expression
        Return:
            VolumeControl: created volume control
        """
        # create volume control
        volume_control = self._model.control_data.create_volume_control()

        # set params
        volume_control.set_params(
            prime.VolumeControlParams(
                model=self._model,
                cell_zonelet_type=prime.CellZoneletType.FLUID,
            )
        )

        # set scope
        volume_control.set_scope(
            prime.ScopeDefinition(
                model=self._model,
                evaluation_type=prime.ScopeEvaluationType.ZONES,
                zone_expression=zone_expression
            )
        )

        # return volume control
        return volume_control

    def create_prism_control_(self,
                              label_expression: str,
                              zone_expression: str,
                              n_layers_local: int | None = None,
                              first_height_local: float | None = None,
                              growth_rate_local: float | None = None) -> PrismControl:
        """
        Create prism control.

        Args:
            label_expression (str): label expression for surface scope definition
            zone_expression (str): zone expression for volume scope definition
            n_layers_local (int): local number of layers
            first_height_local (float): local first height
            growth_rate_local (float): local growth rate
        Return:
            PrismControl: created prism control
        """
        # create prism control
        prism_control = self._model.control_data.create_prism_control()

        # set surface scope
        prism_control.set_surface_scope(
            prime.ScopeDefinition(
                model=self._model,
                evaluation_type=prime.ScopeEvaluationType.LABELS,
                entity_type=prime.ScopeEntity.FACEZONELETS,
                label_expression=label_expression
            )
        )

        # set volume scope
        prism_control.set_volume_scope(
            prime.ScopeDefinition(
                model=self._model,
                evaluation_type=prime.ScopeEvaluationType.ZONES,
                entity_type=prime.ScopeEntity.VOLUME,
                zone_expression=zone_expression,
            )
        )

        # set prism control growth parameters
        prism_control.set_growth_params(
            prime.PrismControlGrowthParams(
                model=self._model,
                offset_type=prime.PrismControlOffsetType.UNIFORM,
                n_layers=n_layers_local if n_layers_local else self.prism_d_p.n_layers,
                first_height=first_height_local if first_height_local else self.prism_d_p.first_height,
                growth_rate=growth_rate_local if growth_rate_local else self.prism_d_p.growth_rate
            )
        )

        # return prism control
        return prism_control

    def generate_volume_mesh(self,
                             prism_control: PrismControl,
                             volume_control: VolumeControl,
                             part: Part):
        """
        Generate volume mesh.

        Args:
            prism_control (PrismControl): prism control to generate volume mesh
            volume_control (VolumeControl): volume control to generate volume mesh
            part (Part): part to generate volume mesh
        """
        # create AutoMesh object
        volume_mesh = prime.AutoMesh(self._model)

        # set volume mesh params
        auto_mesh_param = prime.AutoMeshParams(
            model=self._model,
            prism_control_ids=[prism_control.id],
            size_field_type=prime.SizeFieldType.VOLUMETRIC,
            volume_fill_type=prime.VolumeFillType.TET,
            volume_control_ids=[volume_control.id],
        )

        # generate mesh
        volume_mesh.mesh(part.id, auto_mesh_param)

    def set_scope(self,
                  size_control: SizeControl,
                  part_expression: str = "*",
                  label_expression: str = "*"):
        """
        Construct and set a scope on size control.

        Args:
            size_control (SizeControl): size control to construct and set the scope
            part_expression (str): part expression to construct and set the scope
            label_expression (str): label expression to construct and set the scope
        """
        size_control.set_scope(
            prime.ScopeDefinition(
                model=self._model,
                part_expression=part_expression,
                label_expression=label_expression,
                entity_type=prime.ScopeEntity.FACEZONELETS
            )
        )

    def construct_scope(self, part_expression: str = "*") -> ScopeDefinition:
        """
        Construct a scope.

        Args:
            part_expression (str): part expression to construct the scope
        Return:
            ScopeDefinition: constructed scope
        """
        return prime.ScopeDefinition(
            model=self._model,
            part_expression=part_expression
        )

    def plot(self, scope: ScopeDefinition | None = None):
        """
        Plot results with given scope.

        Args:
            scope (ScopeDefinition): the scope to plot with
        """
        display = PrimePlotter()
        display.plot(self._model, scope=scope, update=True)
        display.show()

    def get_part_by_name(self, part_name: str) -> Part:
        """
        Get part by name.

        Args:
            part_name (str): part name
        Return:
            Part: the part
        """
        return self._model.get_part_by_name(part_name)

    def save(self, file_name: str):
        """
        Save mesh into .msh and .cas files.
        Results will be saved in Mesh/results/mesh_3d.

        Args:
            file_name (str): raw file name (without extension)
        """
        # set export mesh fluent params
        params = prime.ExportFluentMeshingMeshParams(
            model=self._model
        )

        # export to mesh
        print("Exporting to msh file...")
        prime.FileIO(self._model).export_fluent_meshing_mesh(
            file_name=str(MESH_3D / f"{file_name}.msh"),
            export_fluent_mesh_params=params
        )

        # set export case fluent params
        params = prime.ExportFluentCaseParams(
            model=self._model
        )

        # export to cas.h5
        print("Exporting to cas.h5 file...")
        prime.FileIO(self._model).export_fluent_case(
            file_name=str(MESH_3D / f"{file_name}.cas.h"),
            export_fluent_case_params=params
        )
