import os
import tempfile
import ansys.meshing.prime as prime
from ansys.meshing.prime.graphics.plotter import PrimePlotter
from ansys.meshing.prime import Model



# 1. Uruchomienie klienta
client = prime.launch_prime(prime_root=r"C:\Program Files\ANSYS Inc\v251\meshing\Prime")
model = client.model

# 2. Zaimportuj model CAD
file_io = prime.FileIO(model=model)
params = prime.ImportCadParams(model=model)
results = file_io.import_cad(r"C:\Users\Symkom\Downloads\M6412.step", params=params)
# results = file_io.import_cad(r"C:\Users\Symkom\ANSW2\SymkomPraktyki2025\model\D2_5\geometry\results\model_2D\Wind_Turbine.stp", params=params)

# 3. Pobierz pierwszą część
part = model.parts[0]

display = PrimePlotter()
display.plot(model)
display.show()

print(model)


mesh_util = prime.lucid.Mesh(model=model)
mesh_util.read(file_name="m6412")

target_part = model.get_part(0)
target = target_part.get_topo_faces(0)
print(target)