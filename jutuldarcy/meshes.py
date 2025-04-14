from .julia_import import jl

def CartesianMesh(*arg, **kwargs):
    return jl.Jutul.CartesianMesh(*arg, **kwargs)

def UnstructuredMesh(*arg, **kwargs):
    return jl.Jutul.UnstructuredMesh(*arg, **kwargs)
