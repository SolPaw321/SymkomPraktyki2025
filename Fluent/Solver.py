from Fluent.Session import Session


class SolverMode(Session):
    """
    The class for managing Fluent settings.
    """
    def __init__(self,
                 processor_count: int = 2,
                 inlet_velocity: float = 10.0,
                 rpm: float = 10.0):
        """
        Solver class constructor.

        Args:
            processor_count (int): Number of processors. The default is None, in which case 1 processor is used.
                                   In job scheduler environments the total number of allocated cores is clamped
                                   to value of processor_count.
            inlet_velocity (float): the inlet velocity in m/s
            rpm (float): rotate per minute
        """
        # initialize session class
        Session.__init__(self, processor_count=processor_count)

        # set inlet velocity and rpm
        self._inlet_velocity = inlet_velocity  # m/s
        self._rpm = rpm  # rev/min

        # some shortcuts
        self.setup = self.session.settings.setup
        self.general = self.setup.general
        self.solution = self.session.settings.solution

    def set_general_settings(self):
        """
        Set general settings, e.g.:
        - type = pressure-based
        - velocity formulation = absolute
        - time = steady
        """
        self.general.solver.type.default_value()
        self.general.solver.time.default_value()
        self.general.solver.velocity_formulation.default_value()

        self.general.solver.type.set_state("pressure-based")
        self.general.solver.velocity_formulation.set_state("absolute")
        self.general.solver.time.set_state("steady")

    def select_model(self):
        """
        Select the SST k-omega model.
        """
        viscous = self.setup.models.viscous

        viscous.model.set_state('k-omega')
        viscous.k_omega_model.set_state("sst")

    def define_boundary_condition(self):
        """
        Define boundary conditions (inlet, outlet, symmetry, wall and interface) with some default parameters.
        """
        # inlet boundary condition
        self.setup.boundary_conditions.set_zone_type(zone_list=["inlet"], new_type="velocity-inlet")
        inlet = self.setup.boundary_conditions.velocity_inlet["inlet"]
        inlet.turbulence.turbulent_intensity.set_state(0.05)
        inlet.momentum.velocity_magnitude.set_state(self._inlet_velocity)
        inlet.turbulence.turbulent_viscosity_ratio.set_state(10)

        # outlet boundary condition
        self.setup.boundary_conditions.set_zone_type(zone_list=["outlet"], new_type="pressure-outlet")
        outlet = self.setup.boundary_conditions.pressure_outlet["outlet"]
        outlet.momentum.backflow_reference_frame.set_state("Absolute")
        outlet.momentum.pressure_profile_multiplier.set_state(1.0)
        outlet.momentum.gauge_pressure.set_state(0.0)
        outlet.momentum.backflow_dir_spec_method.set_state("Normal to Boundary")
        outlet.turbulence.backflow_turbulent_intensity.set_state(0.05)
        outlet.turbulence.backflow_turbulent_viscosity_ratio.set_state(10)

        # symmetry boundary condition
        self.setup.boundary_conditions.set_zone_type(
            zone_list=["symmetry_symmetry_symmetry", "symmetry_symmetry_symmetry_7", "symmetry_symmetry_symmetry_8"],
            new_type="symmetry"
        )

        # wall boundary condition
        self.setup.boundary_conditions.set_zone_type(zone_list=["wall"], new_type="wall")

        # interface boundary condition
        self.setup.mesh_interfaces.interface.create(name="interface_1", zone1="wall_12", zone2="wall_10")
        self.setup.mesh_interfaces.interface.create(name="interface_2", zone1="interface-10", zone2="wall_11")

    def create_named_expressions(self):
        """
        Create named expressions:
        - rpm
        - inlet velocity
        - outlet pressure
        - TSR
        - power
        - efficiency
        """
        # rpm named expression
        self.setup.named_expressions.create("rpm")
        rpm = self.setup.named_expressions["rpm"]
        rpm.definition.set_state(f"{self._rpm}[rev/min]")
        rpm.input_parameter.set_state(True)

        # velocity_inlet named expression
        self.setup.named_expressions.create("velocity_inlet")
        velocity_inlet = self.setup.named_expressions["velocity_inlet"]
        velocity_inlet.definition.set_state(f"{self._inlet_velocity}[m/s]")
        velocity_inlet.input_parameter.set_state(True)

        # pressure_outlet named expression
        self.setup.named_expressions.create("pressure_outlet")
        pressure_outlet = self.setup.named_expressions["pressure_outlet"]
        pressure_outlet.definition.set_state("0[Pa]")
        pressure_outlet.output_parameter.set_state(True)

        # TSR named expression
        self.setup.named_expressions.create("TSR")
        tsr = self.setup.named_expressions["TSR"]
        tsr.definition.set_state("rpm*1[m]/velocity_inlet*1[rad^-1]")

        # Power named expression
        self.setup.named_expressions.create("Power")
        power = self.setup.named_expressions["Power"]
        power.definition.set_state("rpm*total_moment")

        # Efficiency named expression
        self.setup.named_expressions.create("Efficiency")
        efficiency = self.setup.named_expressions["Efficiency"]
        efficiency.definition.set_state("power/(0.5*1.225[kg/s]*1[m]*2[m]*velocity_inlet^3)*100*1[m^3 s^-1 rad^-1]")

    def create_report_def_and_plots(self):
        """
        Create some report definition with report plots:
        - mass balance
        - total moment
        - power
        - efficiency
        """
        # shortcut
        report_definition = self.solution.report_definitions

        # mass-balance report def and plot
        report_definition.flux.create("mass-balance")
        mass_balance = report_definition.flux["mass-balance"]
        mass_balance.boundaries.set_state(("inlet", "outlet"))
        mass_balance.create_report_plot.set_state("mass-balance-rplot")

        # total_moment report def and plot
        report_definition.force.create("total_moment")
        total_moment = report_definition.force["total_moment"]
        total_moment.zones.set_state("wall")
        total_moment.create_report_plot.set_state("total-moment-rplot")

        # power report def and plot
        report_definition.single_valued_expression.create("power")
        power = report_definition.single_valued_expression["power"]
        power.definition.set_state("Power")
        power.create_report_plot.set_state("power-rplot")
        power.create_report_file.set_state("power-rfile")

        # efficiency report def and plot
        report_definition.single_valued_expression.create("efficiency")
        efficiency = report_definition.single_valued_expression["efficiency"]
        efficiency.definition.set_state("Efficiency")
        efficiency.create_report_file.set_state("efficiency-rfile")
        efficiency.create_report_plot.set_state("efficiency-rplot")

    def define_cell_zone_conditions(self):
        """
        Define rotation in the ring and inner circle as a frame and mesh montion.
        """
        # the ring rotation
        fluid_2 = self.setup.cell_zone_conditions.fluid["fluid-2"]
        fluid_2.reference_frame.frame_motion.set_state(True)
        fluid_2.reference_frame.mrf_omega.value.set_state("rpm")

        # the inner circle rotation
        fluid_3 = self.setup.cell_zone_conditions.fluid["fluid-3"]
        fluid_3.reference_frame.frame_motion.set_state(True)
        fluid_3.reference_frame.mrf_omega.value.set_state("rpm")

    def initialize(self, init_iter: int = 10):
        """
        Run initializer.

        Args:
            init_iter (int): the number of iterations to initialize the simulation
        """
        self.solution.run_calculation.pseudo_time_settings.time_step_method.time_step_size_scale_factor.set_state(
            init_iter
        )
        self.solution.initialization.hybrid_initialize()

    def run(self, run_iter: int = 350):
        """
        Run simulation.

        Args:
            run_iter (int): the number of iteration tu run the simulation
        """
        self.solution.run_calculation.iter_count.set_state(run_iter)
        # self.solution.run_calculation.calculate()
