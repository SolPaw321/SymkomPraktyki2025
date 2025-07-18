
import ansys.meshing.prime as prime
from Mesh.Size_fields import setup_mesh_controls_for_part


def create_prime_client(ip="127.0.0.1", port=50055):
    """
    Create and return a Prime client for meshing operations.
    
    """
    return prime.Client(ip=ip, port=port)


def read_geometry(client, geometry_file):
    """
    Read geometry file into the Prime model.
   
    """
    model = client.model
    model.read(geometry_file)
    return model


def prepare_mesh_faces(model):
    """
    Get all faces from the geometry model and prepare a list for meshing.
   
    """
    faces = model.get_faces()
    part_face_list = [(None, face) for face in faces]
    return part_face_list


def set_global_mesh_sizing(mesh, mesh_size):
    """
    Set global mesh sizing parameters for the model.
   
    """
    mesh.set_global_sizing_params(prime.GlobalSizingParams(mesh, min=mesh_size*0.1, max=mesh_size*5.0))


def mesh_and_export(lucid, part_face_list, mesh_type, output_file):
    """
    Generate mesh for all faces and export to Fluent file.
   
    """
    for part, face in part_face_list:
        if mesh_type == "hex":
            lucid.generate_surface_mesh(face, generate_quads=True)
        else:
            lucid.generate_surface_mesh(face, generate_quads=False)
    if not output_file.lower().endswith('.cas'):
        output_file = output_file.rsplit('.', 1)[0] + '.cas'
    lucid.write(output_file)
    print(f"Mesh saved to Fluent file: {output_file}")


def generate_mesh_from_geometry_file(geometry_file, mesh_type="hex", mesh_size=0.01, output_file="mesh.cas", ip="127.0.0.1", port=50055):
    """
    Main workflow: Load geometry from file, set mesh controls, generate mesh, and export.
    
    """
    client = create_prime_client(ip, port)
    model = read_geometry(client, geometry_file)
    lucid = prime.lucid.Mesh(model=model)
    set_global_mesh_sizing(model, mesh_size)
    part_face_list = prepare_mesh_faces(model)
    # Optionally set mesh controls for each face (if API allows)
    # for part, face in part_face_list:
    #     setup_mesh_controls_for_part(model, lucid, part, face, mesh_size)
    mesh_and_export(lucid, part_face_list, mesh_type, output_file)
    client.exit()
