from ansys.geometry.core import launch_modeler
from model.D2_5.geometry.SketchController import SketchController
from model.D2_5.geometry.misc.PATHS import RESULTS
from ansys.geometry.core.designer.component import Component
from ansys.geometry.core.sketch import Sketch
from ansys.geometry.core.misc import Distance


class ModelerController:
    """
    ModelerController is a class for create, run and save modeler environment (Discovery).
    """

    def __init__(self, design_name: str):
        self.modeler = launch_modeler(mode="Discovery", **{"timeout": 500})
        print(self.modeler)

        self._design_name = design_name
        self._design = self.modeler.create_design(self._design_name)

        self._components: dict[str, Component] = dict()
        self._sketches: dict[str, list[Sketch]] = dict()

        self._distance = Distance(0.1)

    @property
    def components(self) -> dict[str, Component]:
        """
        Return dict of all Components.
        """
        return self._components

    @property
    def sketches(self) -> dict[str, list[Sketch]]:
        """
        Return dict of all Sketches
        :return:
        """
        return self._sketches

    def add_component(self, component_name: str,
                      sketch_controllers: list[SketchController] | SketchController):
        """
        Create new component from sketch (or _sketches) and name selection.

        Args:
            component_name (str): name of new component
            sketch_controllers (list[SketchController] | SketchController): sketch (or _sketches) to model
            named_selection_name (str): name of new named selection
        """
        if type(sketch_controllers) == SketchController:
            sketch_controllers = [sketch_controllers]

        component = self._design.add_component(component_name)

        sketches = []
        for sketch_controller in sketch_controllers:
            name, sketch = sketch_controller.get()
            component.extrude_sketch(name, sketch, self._distance)

            sketches.append(sketch)

        self._components[component_name] = component
        self._sketches[component_name] = sketches

    def add_named_selection(self,
                            component_name: str,
                            named_selection_name: str):
        """
        Create named selection from Component and add to Design.

        Args:
            component_name (str): Component name
            named_selection_name (str): named selection name
        """
        component = self._components[component_name]
        self._design.create_named_selection(named_selection_name, bodies=component.bodies)

    def add_inlet_and_outlet(self):
        env_component = self._components["Env"]

        env_faces = env_component.bodies[0].faces

        inlet_faces = []
        outlet_faces = []
        for face in env_faces:
            if face.normal().x < 0:
                inlet_faces.append(face)
            elif face.normal().x > 0:
                outlet_faces.append(face)

        self._design.create_named_selection("inlet", faces=inlet_faces)
        self._design.create_named_selection("outlet", faces=outlet_faces)

    def add_wall(self):
        """
        This method subtracts NACA airfoil from ring and creates named selection ''wall''.
        """
        airfoil_component = self._components["NACA"]
        ring_component = self._components["Ring"]

        ring_body = ring_component.bodies[0]
        ring_faces_id = [face.id for face in ring_body.faces]

        for airfoil_body in airfoil_component.bodies:
            ring_body.subtract(airfoil_body, keep_other=True)

        wall_faces = [face for face in ring_body.faces if face.id not in ring_faces_id]

        self._design.create_named_selection("wall", faces=wall_faces)

    def cut(self, cake_name: str,
            knife_name: str):
        """
        Cut ''cake_name'' component with ''knife_name'' sketch.

        Args:
            cake_name (str): name of component to cut
            knife_name (str): name of cutting sketch
        """
        base_component = self._components[cake_name]
        cutter_sketches = self._sketches[knife_name]

        for i in range(len(cutter_sketches)):
            base_component.extrude_sketch(f"cut_{i + 1}", cutter_sketches[i], self._distance, cut=True)

    def delete_component(self, component_name: str):
        """
        Delete Component from Design.

        Args:
            component_name (str): Component name
        """
        self._design.delete_component(self._components[component_name])
        self._components.pop(component_name)
        self._sketches.pop(component_name)

    def plot(self):
        """
        Plot the _design.
        """
        self._design.plot()

    def save(self, file_name: str):
        """
        Save your project.

        Args:
            file_name (str): name of your file
        """
        self._design.export_to_step(RESULTS / file_name)
        print(f"File exported to: {RESULTS / file_name}")

    def close(self):
        """
        Close environment.
        """
        self.modeler.close()
