from Solver import SolverMode
from time import sleep

# --- Run the Fluent session in solver mode --- #
solver = SolverMode(
    processor_count=2,
    inlet_velocity=12,  # m/s
    rpm=10  # rev/min
)

# --- Set general settings --- #
solver.set_general_settings()

# --- Select the SST k-omega model --- #
solver.select_model()

# --- Define boundary conditions (inlet, outlet, symmetry, wall and interface) --- #
solver.define_boundary_condition()

# --- Create named expressions (inlet_velocity, outlet_pressure, rpm, power, efficiency, TSR) --- #
solver.create_named_expressions()

# --- Create reports and plots (mass_balance, total_moment, power, efficiency) --- #
solver.create_report_def_and_plots()

# --- Create cell zone condition (rotation of the ring and inner circle) --- #
solver.define_cell_zone_conditions()

# --- Run initializer --- #
solver.initialize(init_iter=10)

# --- Run simulation --- #
solver.run(run_iter=350)

sleep(10000000)

# --- Exit Fluent session --- #
solver.exit()
