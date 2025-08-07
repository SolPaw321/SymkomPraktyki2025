from ansys.fluent.core import launch_fluent, FluentMode, Dimension, Precision, Solver
from Fluent.misc.PATHS import MESH_3D, WORK_DIR


class Session:
    """
    This class is used to manage the Fluent session.
    """
    def __init__(self, processor_count: int = 2):
        """
        Session class constructor.

        Args:
            processor_count (int): Number of processors. The default is None, in which case 1 processor is used.
                                   In job scheduler environments the total number of allocated cores is clamped
                                   to value of processor_count.
        """
        # initialize solver session
        self._session: Solver = self.__session(processor_count=processor_count)
        print("Successfully launched")

        # initialize workflow and task
        self._workflow = self.__workflow()
        self._tasks = self.__task()

        # import mesh
        self.__import_mesh()

    @property
    def session(self) -> Solver:
        """
        Get the Solver session

        Return:
            Solver: the Solver session
        """
        return self._session

    @staticmethod
    def __session(processor_count: int = 2) -> Solver:
        """
        Run the Solver session with given parameters.

        Return:
            Solver: the Solver session
        """
        return launch_fluent(
            cleanup_on_exit=True,
            mode=FluentMode.SOLVER,
            precision=Precision.DOUBLE,
            processor_count=processor_count,
            dimension=Dimension.THREE,
            cwd=str(WORK_DIR),
            py=True,
            ui_mode="gui"
        )

    def __workflow(self):
        """
        Initialize Watertight Geometry workflow.

        Return:
            The workflow
        """
        workflow = self._session.workflow
        workflow.InitializeWorkflow(WorkflowType='Watertight Geometry')
        return workflow

    def __task(self):
        """
        Get a task.

        Return:
            The task
        """
        tasks = self._workflow.TaskObject
        return tasks

    def __import_mesh(self):
        """
        Import mesh.h5 file.
        """
        print("Reading .msh.h5 file...")
        file_path = str(MESH_3D / "wind_turbine.msh.h5")
        self._session.settings.file.read_mesh(file_name=file_path)
        print("Read success")

    def exit(self):
        """
        Exit the Fluent session.
        """
        self._session.exit()
