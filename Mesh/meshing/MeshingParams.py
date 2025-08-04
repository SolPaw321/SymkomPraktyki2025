from Mesh.default_params.SizingParams import *
from Mesh.default_params.MeshUtilParams import *
from Mesh.default_params.PrismParams import *


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
        self._boi_s_d_p = BoiSizingParams()

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
    def boi_s_d_p(self) -> BoiSizingParams:
        """
        Get body of influence sizing params.

        Return:
            BoiSizingParams: body of influence default sizing params
        """
        return self._boi_s_d_p

    @property
    def prism_d_p(self) -> PrismParams:
        """
        Get prism sizing params.

        Return:
            PrismParams: prism default sizing params
        """
        return self._prism_d_p

    def set_mesh_util_d_p(self,
                          min_size: float | None = None,
                          max_size: float | None = None):
        """
        Set default mesh util params.

        Args:
            min_size (float | None): minimum size of mesh element
            max_size (float | None): maximum size of mesh element
        """
        self._mesh_util_d_p = MeshUtilParams(
            min_size=min_size if min_size else self._mesh_util_d_p.min_size,
            max_size=max_size if max_size else self._mesh_util_d_p.max_size
        )

    @global_s_d_p.setter
    def global_s_d_p(self,
                     min_: float | None = None,
                     max_: float | None = None,
                     growth_rate_: float | None = None):
        """
        Set default global params.

        Args:
            min_ (float | None): Minimum value of global sizing parameters.
            max_ (float | None): Maximum value of global sizing parameters.
            growth_rate_ (float | None): Growth rate of global sizing parameters
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
            max_ (float | None): Maximum size used for computing edge and face size using boi size control.
            growth_rate_ (float | None): Growth rate used for transitioning from one element size to neighbor element size
        """
        self._boi_s_d_p = BoiSizingParams(
            max=max_ if max_ else self._boi_s_d_p.max,
            growth_rate=growth_rate_ if growth_rate_ else self._boi_s_d_p.growth_rate
        )

    @prism_d_p.setter
    def prism_d_p(self,
                  n_layers_: int | None = None,
                  first_height_: float | None = None,
                  growth_rate_: float | None = None):
        """
         Set default prism params.

         Args:
            n_layers_ (int | None): default number of layers
            first_height_ (float | None): default first height
            growth_rate_ (float | None): default growth rate
         """
        self._prism_d_p = PrismParams(
            n_layers=n_layers_ if n_layers_ else self._prism_d_p.n_layers,
            first_height=first_height_ if first_height_ else self._prism_d_p.first_height,
            growth_rate=growth_rate_ if growth_rate_ else self._prism_d_p.growth_rate
        )
