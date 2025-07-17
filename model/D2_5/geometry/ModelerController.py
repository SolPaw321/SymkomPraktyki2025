from ansys.geometry.core import launch_modeler
from model.D2_5.geometry.SketchController import SketchController


class ModelerController:
    """
    ModelerController is a class for create, run and save modeler environment (Discovery).
    """
    def __init__(self, design_name: str):
        self.modeler = launch_modeler(mode="Discovery")
        print(self.modeler)

        self.design_name = design_name
        self.design = self.modeler.create_design(self.design_name)

        self.components = dict()
        self.sketches = dict()

        self.distance = None

    def add_component_and_named_selection(self, component_name: str,
                                          sketch_controllers: list[SketchController] | SketchController,
                                          named_selection_name: str):
        """
        Create new component from sketch (or sketches) and name selection.

        Args:
            component_name (str): name of new component
            sketch_controllers (list[SketchController] | SketchController): sketch (or sketches) to model
            named_selection_name (str): name of new named selection
        """
        if type(sketch_controllers) == SketchController:
            sketch_controllers = [sketch_controllers]

        component = self.design.add_component(component_name)

        sketches = []
        for sketch_controller in sketch_controllers:
            name, sketch, distance = sketch_controller.get()
            component.extrude_sketch(name, sketch, distance)

            sketches.append(sketch)
            self.distance = distance

        self.components[component_name] = component
        self.sketches[component_name] = sketches

        self.design.create_named_selection(named_selection_name, bodies=component.bodies)

    def cut(self, cake_name: str, knife_name: str):
        """
        Cut ''cake_name'' component with ''knife_name'' sketch.

        Args:
            cake_name (str): name of component to cut
            knife_name (str): name of cutting sketch
        """
        base_component = self.components[cake_name]
        cutter_sketches = self.sketches[knife_name]

        for i in range(len(cutter_sketches)):
            base_component.extrude_sketch(f"cut_{i+1}", cutter_sketches[i], self.distance, cut=True)

    def plot(self):
        """
        Plot the design.
        """
        self.design.plot()

    def close(self):
        """
        Close environment.
        """
        self.modeler.close()
