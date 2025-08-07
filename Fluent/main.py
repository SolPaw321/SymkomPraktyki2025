from Solver import SolverMode
from time import sleep

solver = SolverMode()
solver.set_general_settings()
solver.select_model()
solver.define_boundary_condition()
solver.named_expressions()
solver.report_definitions()
solver.define_cell_zone_conditions()
solver.run()

sleep(1000000)
# solver.exit()
