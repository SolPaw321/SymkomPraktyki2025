from Fluent.Session import Session
from ansys.fluent.core.session_solver import Solver
import ansys.fluent.core as pyfluent


class SolverMode(Session):
    def __init__(self):
        Session.__init__(self, "solver")

        self._density = 1.225
        self._inlet_velocity = 12.0

        self.setup = self.session.settings.setup

        self.general = self.setup.general
        self.solution = self.session.settings.solution


    def set_general_settings(self):
        self.general.solver.type.default_value()
        self.general.solver.time.default_value()
        self.general.solver.velocity_formulation.default_value()

        self.general.solver.type.set_state("pressure-based")
        self.general.solver.velocity_formulation.set_state("absolute")
        self.general.solver.time.set_state("steady")

    def select_model(self):
        viscous = self.setup.models.viscous

        viscous.model.set_state('k-omega')
        viscous.k_omega_model.set_state("sst")
        viscous.options.production_limiter.enabled.set_state(True)
        # viscous.near_wall_treatment.set_state("correlation")

    def define_materials(self):
        pass

    def define_boundary_condition(self):
        self.setup.boundary_conditions.set_zone_type(zone_list=["inlet"], new_type="velocity-inlet")
        inlet = self.setup.boundary_conditions.velocity_inlet["inlet"]
        inlet.turbulence.turbulent_intensity.set_state(0.05)
        inlet.momentum.velocity_magnitude.set_state(12.0)
        inlet.turbulence.turbulent_viscosity_ratio.set_state(10)

        self.setup.boundary_conditions.set_zone_type(zone_list=["outlet"], new_type="pressure-outlet")
        outlet = self.setup.boundary_conditions.pressure_outlet["outlet"]
        outlet.momentum.backflow_reference_frame.set_state("Absolute")
        outlet.momentum.pressure_profile_multiplier.set_state(1.0)
        outlet.momentum.gauge_pressure.set_state(0.0)
        outlet.momentum.backflow_dir_spec_method.set_state("Normal to Boundary")
        #outlet.momentum.backflow_pressure_spec.set_state("intensity-and-viscosity-ratio")
        outlet.turbulence.backflow_turbulent_intensity.set_state(0.05)
        outlet.turbulence.backflow_turbulent_viscosity_ratio.set_state(10)

        #self.setup.boundary_conditions.set_zone_type(zone_list=["symmetry.2", "symmetry.2_7", "symmetry.2_8"], new_type="symmetry")
        #self.setup.boundary_conditions.set_zone_type(zone_list=["symmetry", "symmetry_7", "symmetry_7:014"], new_type="symmetry")
        self.setup.boundary_conditions.set_zone_type(zone_list=["symmetry_symmetry_symmetry", "symmetry_symmetry_symmetry_7", "symmetry_symmetry_symmetry_8"], new_type="symmetry")

        self.setup.boundary_conditions.set_zone_type(zone_list=["wall"], new_type="wall")
        '''wall = self.setup.boundary_conditions.wall["wall"]
        wall.momentum.wall_motion.set_state("stationary-wall")
        wall.momentum.shear_condition.set_state("no-slip")'''

        #self.setup.boundary_conditions.set_zone_type(zone_list=["wall_10", "wall_11", "wall_12"], new_type="interior")
        #self.setup.boundary_conditions.set_zone_type(zone_list=["wall_10", "wall_10:015"], new_type="interior")

        self.setup.mesh_interfaces.interface.create(name="interface_1", zone1="wall_12", zone2="wall_10")
        self.setup.mesh_interfaces.interface.create(name="interface_2", zone1="interface-10", zone2="wall_11")


    def named_expressions(self):
        self.setup.named_expressions.create("rpm")
        rmp = self.setup.named_expressions["rpm"]
        rmp.definition.set_state("10[rev/min]")

        self.setup.named_expressions.create("velocity_inlet")
        velocity_inlet = self.setup.named_expressions["velocity_inlet"]
        velocity_inlet.definition.set_state("12[m/s]")

        self.setup.named_expressions.create("TSR")
        tsr = self.setup.named_expressions["TSR"]
        tsr.definition.set_state("rpm*1[m]/velocity_inlet*1[rad^-1]")

        self.setup.named_expressions.create("Power")
        power = self.setup.named_expressions["Power"]
        power.definition.set_state("rpm*total_moment")

        self.setup.named_expressions.create("Efficiency")
        efficiency = self.setup.named_expressions["Efficiency"]
        efficiency.definition.set_state("power/(0.5*1.225[kg/s]*1[m]*2[m]*velocity_inlet^3)*100*1[m^3 s^-1 rad^-1]")

    def report_definitions(self):
        report_definition = self.solution.report_definitions

        report_definition.flux.create("mass-balance")
        mass_balance = report_definition.flux["mass-balance"]
        mass_balance.boundaries.set_state(("inlet", "outlet"))
        mass_balance.create_report_plot.set_state("mass-balance-rplot")

        report_definition.single_valued_expression.create("power")
        power = report_definition.single_valued_expression["power"]
        power.definition.set_state("Power")
        #power.create_report_plot.set_state("power-rplot")
        #power.create_report_file.set_state("power-rfile")

        report_definition.force.create("total_moment")
        total_moment = report_definition.force["total_moment"]
        #total_moment.report_output_type.set_state("Moment")
        total_moment.zones.set_state("wall")
        #total_moment.create_report_plot.set_state("total_moment-rplot")

        report_definition.single_valued_expression.create("efficiency")
        efficiency = report_definition.single_valued_expression["efficiency"]
        efficiency.definition.set_state("Efficiency")
        #efficiency.create_report_file.set_state("efficiency-rfile")
        #efficiency.create_report_plot.set_state("efficiency-rplot")

    def define_cell_zone_conditions(self):
        fluid_2 = self.setup.cell_zone_conditions.fluid["fluid-2"]
        fluid_2.reference_frame.frame_motion.set_state(True)
        fluid_2.reference_frame.mrf_omega.value.set_state("rpm")

        fluid_3 = self.setup.cell_zone_conditions.fluid["fluid-3"]
        fluid_3.reference_frame.frame_motion.set_state(True)
        fluid_3.reference_frame.mrf_omega.value.set_state("rpm")

    def monitors(self):
        r_plots = self.solution.monitor.report_plots


        # monitor.report_files["mass_balance"]

    def run(self):
        self.solution.run_calculation.pseudo_time_settings.time_step_method.time_step_size_scale_factor.set_state(10)

        self.solution.initialization.hybrid_initialize()
        self.solution.run_calculation.iter_count.set_state(270)
        # self.solution.run_calculation.calculate()
