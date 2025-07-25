from TestMesh.Meshing import Meshing


meshing = Meshing()
meshing.create_size_control("CURVATURE")
meshing.create_size_control("BOI")
meshing.plot()
meshing.exit()