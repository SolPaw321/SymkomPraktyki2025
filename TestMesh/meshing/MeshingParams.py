from TestMesh.default_params.SizingParams import *
from TestMesh.default_params.MeshUtilParams import *


class MeshingParams:
    def __init__(self):
        self._mesh_util_d_p = MeshUtilParams()
        self._global_s_d_p = GlobalSizingParams()
        self._curvature_s_d_p = CurvatureSizingParams()
        self._boi_s_d_p = BoiSizingParams()
        self._proximity_s_d_p = ProximitySizingParams()
        self._meshed_s_d_p = MeshedSizingParams()

    @property
    def mesh_util_d_p(self):
        print(self._mesh_util_d_p)
        return self._mesh_util_d_p

    @property
    def global_s_d_p(self):
        return self._global_s_d_p

    @property
    def curvature_s_d_p(self):
        print(self._curvature_s_d_p)
        return self._curvature_s_d_p

    @property
    def proximity_s_d_p(self):
        return self._proximity_s_d_p

    @property
    def boi_s_d_p(self):
        print(self._boi_s_d_p)
        return self._boi_s_d_p

    @property
    def meshed_s_d_p(self):
        return self._meshed_s_d_p

    @mesh_util_d_p.setter
    def mesh_util_d_p(self,
                      min_size: float | None = None,
                      max_size: float | None = None,
                      generate_quads: bool | None = None):
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
        self._proximity_s_d_p = ProximitySizingParams(
            min=min_ if min_ else self._proximity_s_d_p.min,
            max=max_ if max_ else self._proximity_s_d_p.max,
            growth_rate=growth_rate_ if growth_rate_ else self._proximity_s_d_p.growth_rate,
            elements_per_gap=elements_per_gap_ if elements_per_gap_ else self._proximity_s_d_p.elements_per_gap,
            ignore_orientation=ignore_orientation_ if ignore_orientation_ else self._proximity_s_d_p.ignore_orientation,
            ignore_self_proximity=ignore_self_proximity_ if ignore_self_proximity_ else self._proximity_s_d_p.ignore_self_proximity
        )

    @mesh_util_d_p.setter
    def mesh_util_d_p(self,
                      growth_rate_: float | None = None):
        self._meshed_s_d_p = MeshedSizingParams(
            growth_rate=growth_rate_ if growth_rate_ else self._meshed_s_d_p.growth_rate
        )
