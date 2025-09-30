from .julia_import import jl

def LiquidPhase():
    return jl.LiquidPhase()

def VaporPhase():
    return jl.VaporPhase()

def AqueousPhase():
    return jl.AqueousPhase()

def ImmiscibleSystem(*arg, **kwargs):
    return jl.ImmiscibleSystem(*arg, **kwargs)

def SinglePhaseSystem(*arg, **kwargs):
    return jl.SinglePhaseSystem(*arg, **kwargs)
