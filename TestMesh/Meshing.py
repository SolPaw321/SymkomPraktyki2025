from Client import Client
import ansys.meshing.prime as prime
from ansys.meshing.prime.graphics.plotter import PrimePlotter
from ansys.meshing.prime.core.sizecontrol import SizeControl
from misc.PATHS import Model_stp_file


class Meshing(Client):
    def __init__(self):
        Client.__init__(self)

        self._model = self.__model()
        self._mesh_util = self.__mesh_util()

        part = self._model.get_part_by_name("")
        #part.get_face

    def __mesh_util(self):
        mesh_util = prime.lucid.Mesh(model=self._model)
        print("Reading...")
        # mesh_util.read(file_name=str(Model_stp_file), cad_reader_route=prime.CadReaderRoute.DISCOVERY)
        file_io = prime.FileIO(model=self._model)
        params = prime.ImportCadParams(model=self._model)
        results = file_io.import_cad(str(Model_stp_file), params=params)
        print(results)

        mesh_util.surface_mesh(min_size=5, max_size=20)

        return mesh_util

    def __model(self):
        return self.client.model

    def create_surfer(self):
        raise NotImplemented("")
        # surfer_params = prime.SurferParams(model=self._model, constant_size=1.0)
        #surfer_result = prime.Surfer(self._model).mesh_topo_faces(
        #    part.id, topo_faces=part.get_topo_faces(), params=surfer_params
        #)

    def create_size_control(self, type_: str):
        if type_.upper() == "CURVATURE":
            size_control = self._model.control_data.create_size_control(prime.SizingType.CURVATURE)
            size_control.set_curvature_sizing_params(
                prime.CurvatureSizingParams(model=self._model, min=0.2, max=1.0, normal_angle=18.0)
            )
            size_control.set_suggested_name("curve_global")
        elif type_.upper() == "PROXIMITY":
            size_control = self._model.control_data.create_size_control(prime.SizingType.PROXIMITY)
            size_control.set_proximity_sizing_params(
                prime.ProximitySizingParams(
                    model=self._model,
                    min=0.1,
                    max=2.0,
                    growth_rate=1.2,
                    elements_per_gap=3.0,
                    ignore_orientation=True,
                    ignore_self_proximity=False,
                )
            )
            size_control.set_suggested_name("prox_control")
        elif type_.upper() == "BOI":
            size_control = self._model.control_data.create_size_control(prime.SizingType.BOI)
            size_control.set_boi_sizing_params(
                prime.BoiSizingParams(model=self._model, max=20.0, growth_rate=1.2)
            )
            size_control.set_suggested_name("BOI_control")
            size_control.set_scope(prime.ScopeDefinition(model=self._model))
        else:
            raise NotImplemented("")

        size_control.set_scope(prime.ScopeDefinition(self._model))

    def create_surface_mesh(self):
        raise NotImplemented("")

    def get_all_parts(self):
        print(part.name for part in self._model.parts)

    def plot(self):
        display = PrimePlotter()
        display.plot(self._model)
        display.show()


if __name__ == "__main__":
    meshing = None
    try:
        meshing = Meshing()
        meshing.create_size_control("CURVATURE")
        meshing.create_size_control("BOI")
        meshing.plot()
        meshing.exit()
    except Exception as e:
        print(e)
    finally:
        meshing.exit() if meshing else None
        print("Finally")
