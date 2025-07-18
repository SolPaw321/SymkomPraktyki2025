
import ansys.meshing.prime as prime


# Set soft sizing (local mesh refinement) for a part

def get_refined_size(mesh_size):

    """Return refined mesh size for local controls."""

    return mesh_size * 0.2

def create_soft_size_control(mesh):

    """Create and return a soft sizing control object."""

    return mesh.control_data.create_size_control(prime.SizingType.SOFT)

def create_soft_size_params(mesh, max_size):

    """Create and return soft sizing parameters object."""

    return prime.SoftSizingParams(model=mesh, max=max_size)

def get_wire_label(wire):

    """Return label of wire if it exists, else None."""

    return wire.label if hasattr(wire, 'label') else None

def get_scope_for_wire(mesh, part, wire_label):

    """Return scope for wire label or for all edges if label is None."""

    if wire_label:
        return prime.ScopeDefinition(mesh, part_expression=part.name, label_expression=wire_label)
    else:
        return prime.ScopeDefinition(mesh, part_expression=part.name, entity_type=prime.ScopeEntity.EDGE)

def set_soft_sizing(mesh, part, wire, mesh_size):

    """Set soft sizing (local mesh refinement) for a part."""

    refined_size = get_refined_size(mesh_size)
    soft_size_control = create_soft_size_control(mesh)
    soft_size_params = create_soft_size_params(mesh, refined_size)
    soft_size_control.set_soft_sizing_params(soft_size_params)
    wire_label = get_wire_label(wire)
    scope = get_scope_for_wire(mesh, part, wire_label)
    soft_size_control.set_scope(scope)
    soft_size_control.set_suggested_name(f"refinement_{part.name}")


# Set edge refinement for leading and trailing edges

def create_edge_size_control(mesh):

    """Create and return a soft sizing control for edges."""

    return mesh.control_data.create_size_control(prime.SizingType.SOFT)

def create_edge_size_params(mesh, max_size):

    """Create and return soft sizing parameters for edges."""

    return prime.SoftSizingParams(model=mesh, max=max_size)

def get_edge_scope(mesh, part):

    """Return scope for all edges of a part."""

    return prime.ScopeDefinition(mesh, part_expression=part.name, entity_type=prime.ScopeEntity.EDGE)

def set_edge_refinement(mesh, part, mesh_size):

    """Set edge refinement for leading and trailing edges."""

    refined_size = get_refined_size(mesh_size)
    for idx, name in zip([0, -2], ["leading_edge", "trailing_edge"]):
        edge_size_control = create_edge_size_control(mesh)
        edge_size_params = create_edge_size_params(mesh, refined_size*0.5)
        edge_size_control.set_soft_sizing_params(edge_size_params)
        edge_scope = get_edge_scope(mesh, part)
        edge_size_control.set_scope(edge_scope)
        edge_size_control.set_suggested_name(f"{name}_{part.name}")


# Set curvature-based mesh refinement

def create_curvature_control(mesh):

    """Create and return a curvature sizing control object."""

    return mesh.control_data.create_size_control(prime.SizingType.CURVATURE)

def create_curvature_params(mesh, min_size, max_size):

    """Create and return curvature sizing parameters object."""

    return prime.CurvatureSizingParams(model=mesh, min=min_size, max=max_size, curvature_normalized=1.0)

def get_curvature_scope(mesh, part):

    """Return scope for curvature sizing (all edges of part)."""

    return prime.ScopeDefinition(mesh, part_expression=part.name, entity_type=prime.ScopeEntity.EDGE)

def set_curvature_refinement(mesh, part, mesh_size):
    
    """Set curvature-based mesh refinement."""

    refined_size = get_refined_size(mesh_size)
    curvature_control = create_curvature_control(mesh)
    curvature_params = create_curvature_params(mesh, refined_size*0.5, mesh_size*2.0)
    curvature_control.set_curvature_sizing_params(curvature_params)
    curvature_scope = get_curvature_scope(mesh, part)
    curvature_control.set_scope(curvature_scope)
    curvature_control.set_suggested_name(f"curvature_{part.name}")



def setup_mesh_controls_for_part(mesh, lucid, part, wire, mesh_size):
   
    """Main function to set all mesh controls for a part."""

    set_soft_sizing(mesh, part, wire, mesh_size)
    set_edge_refinement(mesh, part, mesh_size)
    set_curvature_refinement(mesh, part, mesh_size)
