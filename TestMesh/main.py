from Meshing import Meshing


meshing = Meshing()
meshing.get_all_parts()
meshing.create_size_control("CURVATURE")
meshing.create_size_control("BOI")
meshing.plot()
meshing.exit()