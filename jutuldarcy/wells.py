from .julia_import import jl

def setup_vertical_well(*arg, name = "Well", **kwargs):
    if isinstance(name, str):
        name = jl.Symbol(name)
    return jl.setup_vertical_well(*arg, name = name, **kwargs)

def setup_well(*arg, name = "Well", **kwargs):
    if isinstance(name, str):
        name = jl.Symbol(name)
    return jl.setup_well(*arg, name = name, **kwargs)

def setup_injector_control(val, itype, mix, density = 1.0, **kwargs):
    if itype == "rate":
        t = jl.TotalRateTarget(val)
    elif itype == "bhp":
        t = jl.BottomHolePressureTarget(val)
    else:
        raise Exception("Invalid control type")

    return jl.InjectorControl(t, mix, density = density, **kwargs)

def setup_producer_control(val, itype, **kwargs):
    if itype == "rate":
        t = jl.TotalRateTarget(val)
    elif itype == "bhp":
        t = jl.BottomHolePressureTarget(val)
    else:
        raise Exception("Invalid control type")

    return jl.ProducerControl(t, **kwargs)

def setup_disabled_control():
    return jl.DisabledControl()
