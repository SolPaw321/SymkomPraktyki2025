from TestMesh.default_params.SizingParams import *
from TestMesh.default_params.MeshUtilParams import *
from TestMesh.default_params.PrismParams import *


class MeshingParams:
    """
    Class for describe all meshing default params.
    """

    def __init__(self):
        # initialize mesh util params
        # *_d_p == default_params
        self._mesh_util_d_p = MeshUtilParams()

        # initialize sizing params
        # *_s_d_p == sizing_default_params
        self._global_s_d_p = GlobalSizingParams()
        self._curvature_s_d_p = CurvatureSizingParams()
        self._proximity_s_d_p = ProximitySizingParams()
        self._boi_s_d_p = BoiSizingParams()
        self._meshed_s_d_p = MeshedSizingParams()

        # initialize prism params
        # *_d_p == default_params
        self._prism_d_p = PrismParams()

    @property
    def mesh_util_d_p(self) -> MeshUtilParams:
        """
        Get mesh util params.

        Return:
            MeshUtilParams: mesh utility default params
        """
        return self._mesh_util_d_p

    @property
    def global_s_d_p(self) -> GlobalSizingParams:
        """
        Get global sizing params.

        Return:
            GlobalSizingParams: global default sizing params
        """
        return self._global_s_d_p

    @property
    def curvature_s_d_p(self) -> CurvatureSizingParams:
        """
        Get curvature sizing params.

        Return:
            CurvatureSizingParams: curvature default sizing params
        """
        return self._curvature_s_d_p

    @property
    def proximity_s_d_p(self) -> ProximitySizingParams:
        """
        Get proximity sizing params.

        Return:
            ProximitySizingParams: proximity default sizing params
        """
        return self._proximity_s_d_p

    @property
    def boi_s_d_p(self) -> BoiSizingParams:
        """
        Get body of influence sizing params.

        Return:
            BoiSizingParams: body of influence default sizing params
        """
        return self._boi_s_d_p

    @property
    def meshed_s_d_p(self) -> MeshedSizingParams:
        """
        Get meshed sizing params.

        Return:
            MeshedSizingParams: meshed default sizing params
        """
        return self._meshed_s_d_p

    @property
    def prism_d_p(self) -> PrismParams:
        """
        Get prism sizing params.

        Return:
            PrismParams: prism default sizing params
        """
        return self._prism_d_p

    @mesh_util_d_p.setter
    def mesh_util_d_p(self,
                      min_size: float | None = None,
                      max_size: float | None = None,
                      generate_quads: bool | None = None):
        """
        Set default mesh util params.

        Args:
            min_size (float | None):
            max_size (float | None):
            generate_quads (bool | None):
        """
        self._mesh_util_d_p = MeshUtilParams(
            min_size=min_size if min_size else self._mesh_util_d_p.min_size,
            max_size=max_size if max_size else self._mesh_util_d_p.max_size,
            generate_quads=generate_quads if generate_quads else self._mesh_util_d_p.generate_quads
        )

    @global_s_d_p.setter
    def global_s_d_p(self,
                     min_: float | None = None,
                     max_: float | None = None,
                     growth_rate_: float | None = None):
        """
        Set default global params.

        Args:
            min_ (float | None):
            max_ (float | None):
            growth_rate_ (float | None):
        """
        self._global_s_d_p = GlobalSizingParams(
            min=min_ if min_ else self._global_s_d_p.min,
            max=max_ if max_ else self._global_s_d_p.max,
            growth_rate=growth_rate_ if growth_rate_ else self._global_s_d_p.growth_rate
        )

    @curvature_s_d_p.setter
    def curvature_s_d_p(self,
                        min_: float | None = None,
                        max_: float | None = None,
                        normal_angle_: float | None = None,
                        growth_rate_: float | None = None):
        """
        Set default curvature params.

        Args:
               min_ (float | None): default minimum size used for computing edge and face size using curvature size control
               max_ (float | None): default maximum size used for computing edge and face size using curvature size control
               normal_angle_ (float | None): default maximum allowable angle at which one element edge may span
               growth_rate_ (float | None): default growth rate used for transitioning from one element size to neighbor element size
        """
        self._curvature_s_d_p = CurvatureSizingParams(
            max=max_ if max_ else self._curvature_s_d_p.max,
            min=min_ if min_ else self._curvature_s_d_p.min,
            normal_angle=normal_angle_ if normal_angle_ else self._curvature_s_d_p.normal_angle,
            growth_rate=growth_rate_ if growth_rate_ else self._curvature_s_d_p.growth_rate
        )

    @boi_s_d_p.setter
    def boi_s_d_p(self,
                  max_: float | None = None,
                  growth_rate_: float | None = None):
        """
        Set default body of influence params.

        Args:
            max_ (float | None):
            growth_rate_ (float | None):
        """
        self._boi_s_d_p = BoiSizingParams(
            max=max_ if max_ else self._boi_s_d_p.max,
            growth_rate=growth_rate_ if growth_rate_ else self._boi_s_d_p.growth_rate
        )

    @proximity_s_d_p.setter
    def proximity_s_d_p(self,
                        min_: float | None = None,
                        max_: float | None = None,
                        growth_rate_: float | None = None,
                        elements_per_gap_: float | None = None,
                        ignore_orientation_: bool | None = None,
                        ignore_self_proximity_: bool | None = None):
        """
        Set default proximity params.

        Args:
            min_ (float | None):
            max_ (float | None):
            growth_rate_ (float | None):
            elements_per_gap_ (float | None):
            ignore_orientation_ (bool | None):
            ignore_self_proximity_ (bool | None):
        """
        self._proximity_s_d_p = ProximitySizingParams(
            min=min_ if min_ else self._proximity_s_d_p.min,
            max=max_ if max_ else self._proximity_s_d_p.max,
            growth_rate=growth_rate_ if growth_rate_ else self._proximity_s_d_p.growth_rate,
            elements_per_gap=elements_per_gap_ if elements_per_gap_ else self._proximity_s_d_p.elements_per_gap,
            ignore_orientation=ignore_orientation_ if ignore_orientation_ else self._proximity_s_d_p.ignore_orientation,
            ignore_self_proximity=ignore_self_proximity_ if ignore_self_proximity_ else self._proximity_s_d_p.ignore_self_proximity
        )

    @meshed_s_d_p.setter
    def meshed_s_d_p(self,
                     growth_rate_: float | None = None):
        """
        Set default meshed params.

        Args:
            growth_rate_ (float | None):
        """
        self._meshed_s_d_p = MeshedSizingParams(
            growth_rate=growth_rate_ if growth_rate_ else self._meshed_s_d_p.growth_rate
        )

    @prism_d_p.setter
    def prism_d_p(self,
                  n_layers_: int | None = None,
                  first_height_: float | None = None,
                  growth_rate_: float | None = None):
        """
         Set default prism params.

         Args:
             n_layers_ (int | None):
             first_height_ (float | None):
             growth_rate_ (float | None):
         """
        self._prism_d_p = PrismParams(
            n_layers=n_layers_ if n_layers_ else self._prism_d_p.n_layers,
            first_height=first_height_ if first_height_ else self._prism_d_p.first_height,
            growth_rate=growth_rate_ if growth_rate_ else self._prism_d_p.growth_rate
        )
