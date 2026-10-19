"""Relative permeability and capillary pressure helpers from JutulDarcy."""

import numpy as np

from .julia_import import jl
from .conversion import to_julia, _kwargs

__all__ = [
    "BrooksCoreyRelativePermeabilities",
    "TabulatedSimpleRelativePermeabilities",
    "PhaseRelativePermeability",
    "RelativePermeabilities",
    "ReservoirRelativePermeabilities",
    "SimpleCapillaryPressure",
    "set_relative_permeability",
    "set_capillary_pressure",
    "SaturationWeightedOilRelperm",
    "StoneIMethod",
    "StoneIIMethod",
]


def BrooksCoreyRelativePermeabilities(*args, **kwargs):
    return jl.JutulDarcy.BrooksCoreyRelativePermeabilities(
        *(to_julia(a) for a in args), **_kwargs(kwargs)
    )


def TabulatedSimpleRelativePermeabilities(s, kr, **kwargs):
    # Julia expects one vector per phase, not a matrix.
    kr = jl.vect(*(to_julia(list(row)) for row in kr))
    if isinstance(s, (list, tuple, np.ndarray)):
        if len(s) and isinstance(s[0], (list, tuple, np.ndarray)):
            s = jl.vect(*(to_julia(list(row)) for row in s))
        else:
            s = to_julia(list(s))
    return jl.JutulDarcy.TabulatedSimpleRelativePermeabilities(s, kr, **_kwargs(kwargs))


def PhaseRelativePermeability(s, kr, **kwargs):
    return jl.JutulDarcy.PhaseRelativePermeability(
        to_julia(s), to_julia(kr), **_kwargs(kwargs, symbol_keys=("label",))
    )


def RelativePermeabilities(*args, **kwargs):
    return jl.JutulDarcy.RelativePermeabilities(
        *(to_julia(a) for a in args), **_kwargs(kwargs)
    )


def ReservoirRelativePermeabilities(**kwargs):
    return jl.JutulDarcy.ReservoirRelativePermeabilities(**_kwargs(kwargs))


def SimpleCapillaryPressure(*args, **kwargs):
    return jl.JutulDarcy.SimpleCapillaryPressure(
        *(to_julia(a) for a in args), **_kwargs(kwargs)
    )


def set_relative_permeability(model, **kwargs):
    """Set relperm from SWOF/SGOF NumPy matrices or phase interpolators."""
    getattr(jl.JutulDarcy, "set_relative_permeability!")(model, **_kwargs(kwargs))
    return model


def set_capillary_pressure(model, **kwargs):
    """Set Pc from [saturation, pressure] tables; pressures are in Pa."""
    getattr(jl.JutulDarcy, "set_capillary_pressure!")(model, **_kwargs(kwargs))
    return model


def SaturationWeightedOilRelperm():
    return jl.JutulDarcy.SaturationWeightedOilRelperm()


def StoneIMethod(*args, **kwargs):
    return jl.JutulDarcy.StoneIMethod(*args, **kwargs)


def StoneIIMethod():
    return jl.JutulDarcy.StoneIIMethod()
