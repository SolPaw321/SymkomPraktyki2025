import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
import os
from Fluent.misc.PATHS import MESH_3D, WORK_DIR


class Session:
    def __init__(self, type_: str, connect: bool = False):
        self._session = self.__session(connect, type_)
        print("Successfully launched")
        self._solver_session = None

        # self._session = pyfluent.connect_to_fluent()

        self._workflow = self.__workflow()
        self._tasks = self.__task()
        self.__import_geometry()

    @property
    def session(self):
        return self._session

    @staticmethod
    def __session(connect, type_):
        if connect:
            print("Connectiong...")
            return pyfluent.connect_to_fluent(server_info_file_name=r"")

        if type_ == "meshing":
            print("Launching meshing...")
            mode = pyfluent.FluentMode.MESHING
        else:
            print("Launching solver...")
            mode = pyfluent.FluentMode.SOLVER

        return pyfluent.launch_fluent(
            cleanup_on_exit=True,
            mode=mode,
            precision=pyfluent.Precision.DOUBLE,
            processor_count=2,
            dimension=pyfluent.Dimension.THREE,
            cwd=str(WORK_DIR),
            py=True,
            ui_mode="gui"
        )

    def __workflow(self):
        workflow = self._session.workflow
        workflow.InitializeWorkflow(WorkflowType='Watertight Geometry')
        return workflow

    def __task(self):
        tasks = self._workflow.TaskObject
        return tasks

    def __import_geometry(self):
        print("Reading msh file...")
        # self._session.PMFileManagement.
        # self._session.upload(MESH_3D / "wind_turbine.msh")
        file_path = str(MESH_3D / "wind_turbine.msh.h5")
        self.session.settings.file.read_mesh(file_name=file_path)
        print("Read success")


    def exit(self):
        self.session.exit()
