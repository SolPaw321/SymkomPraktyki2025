from ansys.geometry.core import launch_modeler
from Geometry.SketchController import SketchController
from Geometry.misc.PATHS import RESULTS
from ansys.geometry.core.designer.component import Component
from ansys.geometry.core.designer import Body, Design, SharedTopologyType
from ansys.geometry.core.sketch import Sketch
from ansys.geometry.core.misc import Distance, Angle
from ansys.geometry.core.designer.face import Face
from ansys.geometry.core.designer.edge import Edge
from Geometry.misc.PATHS import AIRFOIL_MODEL_2D, AIRFOIL_MODEL_3D
from ansys.geometry.core.math import Point2D, Point3D, UnitVector3D, Vector3D
from numpy.linalg import norm
from ansys.geometry.core.tools.prepare_tools import PrepareTools


class ModelerController:
    """
    ModelerController is a class for create, run and save modeler environment (Discovery).

    """

    def __init__(self, design_name: str, model_type: str, launch_airfoil_from_file: bool):
        self.__validate_model_type(model_type)
        self.modeler = launch_modeler(mode="Discovery", **{"timeout": 500})
        print(self.modeler)

        self._design_name = design_name
        self._model_type = model_type.upper()
        self._launch_airfoil_from_file = launch_airfoil_from_file
        self._design = self.__design()

        self._components: dict[str, Component] = dict()
        self._sketches: dict[str, list[Sketch]] = dict()

        self._distance = Distance(1) if self._model_type == "3D" else Distance(0)

    @staticmethod
    def __validate_model_type(model_type: str):
        """
        Validate model_type.

        """
        if model_type.upper() not in ("2D", "3D"):
            raise ValueError(f"model type should be 2D or 3D")

    def __design(self) -> Design | None:
        """
        Initialize the main design.

        Returns:
             Design: the initialized design
        """
        if self._launch_airfoil_from_file:
            return None
        return self.modeler.create_design(self._design_name)

    @property
    def components(self) -> dict[str, Component]:
        """
        Get dictionary of all components.

        Returns:
            dict[str, Component]: the dictionary of all components
        """
        return self._components

    @property
    def sketches(self) -> dict[str, list[Sketch]]:
        """
        Get dictionary of all sketches.

        Returns:
            dict[str, list[Sketch]]: the dictionary of all sketches
        """
        return self._sketches

    def __extrude(self, component: Component,
                  name: str,
                  sketch: Sketch):
        """
        Extrude sketch basing on your Geometry type (2D or 3D).

        Args:
            component (Component): a component for extrude sketch
            name (str): name of your extroduced sketch,
            sketch (Sketch): sketch to be extroduced
        """
        if self._model_type == "3D":
            component.extrude_sketch(name, sketch, self._distance)
        else:
            component.create_surface(name, sketch)

    def add_component(self, component_name: str,
                      sketch_controllers: list[SketchController] | SketchController):
        """
        Create new component from sketch (or sketches).

        Args:
            component_name (str): name of new component
            sketch_controllers (list[SketchController] | SketchController): sketch (or _sketches) to Geometry
        """
        # validate input value
        if type(sketch_controllers) == SketchController:
            sketch_controllers = [sketch_controllers]

        # add component do main design
        component = self._design.add_component(component_name)

        # extrude sketches
        sketches = []
        for sketch_controller in sketch_controllers:
            name, sketch = sketch_controller.get()
            self.__extrude(component, name, sketch)

            sketches.append(sketch)

        # append components and sketches to dictionaries
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
        # get component and add named selection to main design
        component = self._components[component_name]
        self._design.create_named_selection(named_selection_name, bodies=component.bodies)

    def add_symmetry_named_selection(self):
        """
        Add symmetry named selection into your model.

        """
        symmetry_faces = []
        for component in self._design.components:
            for body in component.bodies:
                if body.name not in ('boi', 'NACA'):
                    for face in body.faces:
                        try:
                            if face.normal().z in (-1, 1) or face.normal().y in (-1, 1):
                                symmetry_faces.append(face)
                        except Exception as e:
                            pass

        self._design.create_named_selection('symmetry', faces=symmetry_faces)

    def add_inlet_and_outlet(self,
                             main_component_name: str):
        """
        Add inlet and outlet named selection to your main fluid.

        Args:
            main_component_name (str): name of main fluid component
        """
        # get the main fluid component and body
        env_component = self._components[main_component_name]
        env_body = env_component.bodies[0]

        # get all faces of edges (elements) basing on Geometry type
        env_: list[Face | Edge] = env_body.faces if self._model_type == "3D" else env_body.edges

        inlet_: dict[str, list[Face | Edge]] = dict([])
        outlet_: dict[str, list[Face | Edge]] = dict([])
        # get inlet and outlet elements based on x coordinate
        if self._model_type == "3D":
            inlet_["faces"] = []
            outlet_["faces"] = []
            for element in env_:
                if element.normal() == UnitVector3D([-1, 0, 0]):
                    inlet_["faces"].append(element)
                elif element.normal() == UnitVector3D([1, 0, 0]):
                    outlet_["faces"].append(element)
        else:
            inlet_['edges'] = []
            outlet_["edges"] = []
            for element in env_:
                if element.start.x < 0 and element.end.x < 0:
                    inlet_["edges"].append(element)
                elif element.start.x > 0 and element.end.x > 0:
                    outlet_["edges"].append(element)

        # create named selections of inlet and outlet elements
        self._design.create_named_selection("inlet", **inlet_)
        self._design.create_named_selection("outlet", **outlet_)

    def add_wall(self,
                 naca_name: str,
                 ring_name: str):
        """
        This method subtracts NACA airfoil from ring and
        creates named selection 'wall' from the created faces or edges.

        """
        # get airfoil and naca component
        airfoil_component = self._components[naca_name]
        ring_component = self._components[ring_name]

        # get ring body
        ring_body = ring_component.bodies[0]

        # get elements (faces of edges based od Geometry type) and element ids before subtraction
        ring_elements_old = ring_body.faces if self._model_type == "3D" else ring_body.edges
        ring_element_id = [element.id for element in ring_elements_old]

        # subtract airfoil from ring
        ring_body.subtract(airfoil_component.bodies, keep_other=False)

        # get new ring elements
        ring_elements_new = ring_body.faces if self._model_type == "3D" else ring_body.edges

        # pull out new elements, after subtract
        wall_: list[Face] | list[Edge] = [element for element in ring_elements_new if element.id not in ring_element_id]

        # create named selection 'wall'
        if self._model_type == "3D":
            self._design.create_named_selection("wall", faces=wall_)
        else:
            self._design.create_named_selection("wall", edges=wall_)

    def load_airfoils(self,
                      file_name: str,
                      center: Point2D | Point3D,
                      radius: Distance,
                      angle_of_attack_deg: Angle,
                      n_airfoils: int):
        """
        This method allows you to read your own NACA profile from file (a path is defined in mis/PATHS.py file).
        This method also place your airfoil Geometry into the circe of given radius.

        Args:
            file_name (str): file name of your Geometry
            center (Point2D): the center of the circle
            radius (Distance): the radius of the circle
            angle_of_attack_deg (Angle): angle of attack
            n_airfoils (int): the number of airfoils to place of the circle
        """
        # validate file name
        if not ("." in file_name):
            raise FileExistsError("Add file extension.")

        # refactor some params
        angle_of_attack_deg = Angle(-1 * angle_of_attack_deg.value)
        center = Point3D([center.x.m, center.y.m, 0]) if type(center) == Point2D else center
        path = AIRFOIL_MODEL_3D if self._model_type == "3D" else AIRFOIL_MODEL_2D
        path = path / file_name

        # read your Geometry
        self._design = self.modeler.open_file(path)
        self._design.set_name = self._design_name  # available in 25R2
        self._design.components[0].set_name = "NACA"  # available in 25R2

        comp = self._design.add_component("NACA")

        # get your Geometry as component and add to components dictionary
        component = self._design.components[0]
        self._components["NACA"] = component
        component.set_name = "NACA"  # available in 25R2

        # get your geometry as a body and scale
        airfoil = component.bodies[0]
        airfoil.scale(10) if self._model_type == "3D" else airfoil.scale(100)

        if self._model_type == "3D":
            airfoil_vertices_z = [vertex.z.m for vertex in airfoil.vertices]
            self._distance = Distance(max(airfoil_vertices_z) - min(airfoil_vertices_z))

        # find the geometric center of your Geometry and translate it to the coordinate system center
        airfoil_center = self.__find_center_of_airfoil(airfoil)
        unit_vector = UnitVector3D(-1 * airfoil_center.position)
        unit_vector = UnitVector3D([unit_vector.x, unit_vector.y, 0])
        distance = norm(airfoil_center.position) / 2.0
        airfoil.translate(unit_vector, distance)

        # set the Geometry for attack
        airfoil.rotate(center, UnitVector3D([0, 0, 1]), angle_of_attack_deg)

        # translate your Geometry into circle
        radius_float = radius.value.m
        airfoil.translate(
            UnitVector3D(Vector3D([radius_float, 0, 0])),
            radius
        )

        # add copies of your Geometry to the circle
        for i in range(n_airfoils):
            if i == 0:
                airfoil_copy = airfoil
                airfoil_copy.set_name = f"Airfoil_{i}"
            else:
                airfoil_copy = airfoil.copy(component, f"Airfoil_{i}")

            angle = Angle(i * 360.0 / n_airfoils)
            airfoil_copy.rotate(center, UnitVector3D([0, 0, 1]), angle)

    @staticmethod
    def __find_center_of_airfoil(airfoil: Body) -> Point3D:
        """
        This method finds geometric center of given airfoil.
        The geometric center is defined by the sum of all vertices divided by their number.

        Args:
            airfoil (Body): airfoil Body object

        Returns:
            Point3D: the geometric center of given airfoil
        """
        # Get the list of Vertex (Point3D)
        airfoil_vertices = airfoil.vertices

        # calculate sum of all vertices as leading vectors
        sum_ = Point3D([0, 0, 0])
        for vertex in airfoil_vertices:
            sum_ += vertex

        # divide by number of vertices and return results
        return sum_ / len(airfoil_vertices)

    def share_topology(self):
        """
        Share topology between fluid bodies.

        """
        components = [comp for comp in self._design.components if comp.name in ('fluid-1', 'fluid-2', 'fluid-3')]
        bodies = []
        for comp in components:
            bodies.append(comp.bodies[0])

        self.modeler.prepare_tools.share_topology([body for body in bodies])

    def plot(self):
        """
        Plot the design.

        """
        self._design.plot()

    def save(self, file_name: str):
        """
        Save your project.

        Args:
            file_name (str): name of your file
        """
        print("Exporting to disco...")
        self._design.export_to_fmd(RESULTS / file_name)

        print("Exporting to fmd...")
        self._design.export_to_disco(RESULTS / file_name)

        print(f"Files exported to: {RESULTS / file_name}")

    def close(self):
        """
        Close environment.

        """
        self.modeler.close()

    def delete_unnecessary_components(self):
        """
        Delete unnecessary components from design, like NACA profiles.

        """
        for comp in self._design.components:
            if comp.name not in ("fluid-1", "fluid-2", "fluid-3", "boi"):
                self._design.delete_component(component=comp)
