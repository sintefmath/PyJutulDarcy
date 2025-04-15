from .julia_import import jl

def CartesianMesh(*arg, **kwargs):
    """
    Create a Cartesian mesh.
    To create a 10 x 10 x 5 mesh with a size of 1000.0 x 1000.0 x 500.0:
    g = CartesianMesh((10, 10, 5), (1000.0, 1000.0, 500.0))
    """
    return jl.Jutul.CartesianMesh(*arg, **kwargs)

def UnstructuredMesh(*arg, **kwargs):
    return jl.Jutul.UnstructuredMesh(*arg, **kwargs)
