from ansys.geometry.core import launch_modeler
from model.D2_5.geometry.SketchController import SketchController
from model.D2_5.geometry.misc.PATHS import RESULTS
from ansys.geometry.core.designer.component import Component
from ansys.geometry.core.designer import Body
from ansys.geometry.core.sketch import Sketch
from ansys.geometry.core.misc import Distance, Angle
from ansys.geometry.core.designer.face import Face
from ansys.geometry.core.designer.edge import Edge
from model.D2_5.geometry.misc.PATHS import AIRFOIL_MODEL
from ansys.geometry.core.math import Point2D, Point3D, UnitVector3D, Vector3D
from numpy.linalg import norm


class ModelerController:
    """
    ModelerController is a class for create, run and save modeler environment (Discovery).
    """

    def __init__(self, design_name: str, model_type: str, launch_airfoil_from_file: bool):
        self.modeler = launch_modeler(mode="Discovery", **{"timeout": 500})
        print(self.modeler)

        self._design_name = design_name
        self._model_type = model_type.upper()
        self._launch_airfoil_from_file =launch_airfoil_from_file
        self._design = self.__design()

        self._components: dict[str, Component] = dict()
        self._sketches: dict[str, list[Sketch]] = dict()

        self._distance = Distance(0.1)

    def __design(self):
        if self._launch_airfoil_from_file:
            if self._model_type == "3D":
                print("Model type: 2D")
            self._model_type = "2D"
            return None
        return self.modeler.create_design(self._design_name)

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

    def __extrude(self, component: Component, name: str, sketch: Sketch):
        if self._model_type == "3D":
            component.extrude_sketch(name, sketch, self._distance)
        else:
            component.create_surface(name, sketch)

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
            self.__extrude(component, name, sketch)

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
        env_component = self._components["fluid-1"]

        env_body = env_component.bodies[0]

        env_: list[Face] | list[Edge] = env_body.faces if self._model_type == "3D" else env_body.edges

        inlet_: list[Face] | list[Edge] = []
        outlet_: list[Face] | list[Edge] = []
        for element in env_:
            if self._model_type == "3D":
                if element.normal().x < 0:
                    inlet_.append(element)
                elif element.normal().x > 0:
                    outlet_.append(element)
            else:
                if element.start.x < 0 and element.end.x < 0:
                    inlet_.append(element)
                elif element.start.x > 0 and element.end.x > 0:
                    outlet_.append(element)

        if self._model_type == "3D":
            self._design.create_named_selection("inlet", faces=inlet_)
            self._design.create_named_selection("outlet", faces=outlet_)
        else:
            self._design.create_named_selection("inlet", edges=inlet_)
            self._design.create_named_selection("outlet", edges=outlet_)

    def add_wall(self):
        """
        This method subtracts NACA airfoil from ring and creates named selection ''wall''.
        """
        airfoil_component = self._components["NACA"]
        ring_component = self._components["fluid-2"]

        ring_body = ring_component.bodies[0]

        ring_elements_old = ring_body.faces if self._model_type == "3D" else ring_body.edges
        ring_element_id = [element.id for element in ring_elements_old]

        ring_body.subtract(airfoil_component.bodies, keep_other=True)

        ring_elements_new = ring_body.faces if self._model_type == "3D" else ring_body.edges

        wall_: list[Face] | list[Edge] = [element for element in ring_elements_new if element.id not in ring_element_id]

        if self._model_type == "3D":
            self._design.create_named_selection("wall", faces=wall_)
        else:
            self._design.create_named_selection("wall", edges=wall_)

    def cut(self, cake_name: str,
            knife_name: str):
        """
        Cut ''cake_name'' component with ''knife_name'' sketch.

        Args:
            cake_name (str): name of component to cut
            knife_name (str): name of cutting sketch
        """
        base_component = self._components[cake_name]
        cutter_component = self._components[knife_name]

        base_bodies = base_component.bodies
        for base_body in base_bodies:
            base_body.subtract(cutter_component.bodies, keep_other=True)

    def delete_component(self, component_name: str):
        """
        Delete Component from Design.

        Args:
            component_name (str): Component name
        """
        if component_name == "NACA":
            self._design.delete_component(self._components["NACA"])
            self._components.pop("NACA")
        else:
            self._design.delete_component(self._components[component_name])
            self._components.pop(component_name)
            self._sketches.pop(component_name)

    def load_airfoils(self, center: Point2D,
                      radius: Distance,
                      angle_of_attack_deg: Angle,
                      n_airfoils: int):
        center = Point3D([center.x.m, center.y.m, 0])

        self._design = self.modeler.open_file(AIRFOIL_MODEL)
        self._design.set_name = self._design_name

        # self._design.components[0].set_name = "NACA"
        component = self._design.components[0]
        component.set_name = "NACA"
        self._components["NACA"] = component
        airfoil = component.bodies[0]
        airfoil.scale(0.1)

        airfoil_center = self.__find_center_of_airfoil(airfoil)
        unit_vector = UnitVector3D(-1 * airfoil_center.position)
        distance = norm(airfoil_center.position)
        airfoil.translate(unit_vector, distance)

        airfoil.rotate(center, UnitVector3D([0, 0, 1]), angle_of_attack_deg)

        radius_float = radius.value.m
        airfoil.translate(
            UnitVector3D(Vector3D([radius_float, 0, 0])),
            radius
        )

        for i in range(n_airfoils):
            if i == 0:
                airfoil_copy = airfoil
                airfoil_copy.set_name = f"Airfoil_{i}"
            else:
                airfoil_copy = airfoil.copy(component, f"Airfoil_{i}")

            angle = Angle(i * 360.0 / n_airfoils)
            airfoil_copy.rotate(center, UnitVector3D([0, 0, 1]), angle)

    @staticmethod
    def __find_center_of_airfoil(airfoil: Body):
        airfoil_vertices = airfoil.vertices

        leading_edge = airfoil_vertices[0]
        trailing_edge = airfoil_vertices[0]
        for vertex in airfoil_vertices:
            if vertex.x < leading_edge.x:
                leading_edge = vertex
            elif vertex.x > trailing_edge.x:
                trailing_edge = vertex

        return (leading_edge + trailing_edge) / 2

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
