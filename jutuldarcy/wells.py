from .julia_import import jl
from .conversion import to_julia, _kwargs

__all__ = [
    "setup_vertical_well",
    "setup_well",
    "setup_well_from_trajectory",
    "setup_injector_control",
    "setup_producer_control",
    "setup_disabled_control",
    "well_symbols",
    "well_output",
]


def _symbol(value):
    return jl.Symbol(value) if isinstance(value, str) else value


def setup_vertical_well(*args, name="Well", **kwargs):
    return jl.JutulDarcy.setup_vertical_well(
        *(to_julia(a) for a in args), name=_symbol(name), **_kwargs(kwargs)
    )


def setup_well(*args, name="Well", **kwargs):
    args = list(args)
    cells = args[-1]
    if isinstance(cells, list) and cells and isinstance(cells[0], tuple):
        args[-1] = jl.vect(*(to_julia(cell) for cell in cells))
    return jl.JutulDarcy.setup_well(
        *(to_julia(a) for a in args),
        name=_symbol(name),
        **_kwargs(kwargs, symbol_keys=("dir",)),
    )


def setup_well_from_trajectory(*args, name="Well", **kwargs):
    return jl.JutulDarcy.setup_well_from_trajectory(
        *(to_julia(a) for a in args), name=_symbol(name), **_kwargs(kwargs)
    )


def _target(value, kind):
    targets = {
        "rate": "TotalRateTarget",
        "bhp": "BottomHolePressureTarget",
        "mass_rate": "TotalMassRateTarget",
        "oil_rate": "SurfaceOilRateTarget",
        "water_rate": "SurfaceWaterRateTarget",
        "gas_rate": "SurfaceGasRateTarget",
        "liquid_rate": "SurfaceLiquidRateTarget",
    }
    if kind not in targets:
        raise ValueError(
            f"Unknown well control {kind!r}; choose from {', '.join(targets)}"
        )
    return getattr(jl.JutulDarcy, targets[kind])(value)


def setup_injector_control(val, itype, mix, density=1.0, **kwargs):
    return jl.JutulDarcy.InjectorControl(
        _target(val, itype), to_julia(list(mix)), density=density, **_kwargs(kwargs)
    )


def setup_producer_control(val, itype, **kwargs):
    return jl.JutulDarcy.ProducerControl(_target(val, itype), **_kwargs(kwargs))


def setup_disabled_control():
    return jl.JutulDarcy.DisabledControl()


def well_symbols(model):
    return [str(w) for w in jl.JutulDarcy.well_symbols(model)]


def well_output(*args, **kwargs):
    args = list(args)
    if len(args) > 2:
        args[2] = _symbol(args[2])
    if len(args) > 4:
        args[4] = _symbol(args[4])
    return jl.JutulDarcy.well_output(*(to_julia(a) for a in args), **_kwargs(kwargs))
