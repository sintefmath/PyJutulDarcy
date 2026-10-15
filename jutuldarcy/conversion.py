"""Conversions at the Python/Julia boundary."""

from collections.abc import Mapping
from os import PathLike, fspath

import numpy as np

from .julia_import import jl, jlconvert, JuliaValue

__all__ = ["to_julia", "to_python", "convert_to_pydict", "symdict_to_pydict"]


def to_julia(value, *, symbols=True):
    """Copy containers to Julia; dict keys become Symbols unless symbols=False.

    Matrices retain their shape (phases/components by cells). Indices stay
    one-based. Existing Julia values, including AD values, pass through.
    """
    if isinstance(value, JuliaValue):
        return value
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, PathLike):
        return fspath(value)
    if isinstance(value, Mapping):
        result = jl.Dict()
        for key, item in value.items():
            key = jl.Symbol(key) if symbols and isinstance(key, str) else key
            result[key] = to_julia(item, symbols=symbols)
        return result
    if isinstance(value, tuple):
        return jl.tuple(*(to_julia(v, symbols=symbols) for v in value))
    if isinstance(value, np.ndarray):
        if value.dtype.kind not in "biufc":
            return jl.vect(*(to_julia(v, symbols=symbols) for v in value))
        array = value if value.ndim == 0 else np.asfortranarray(value)
        return jlconvert(jl.Array, array)
    if isinstance(value, list):
        try:
            array = np.asarray(value)
        except (ValueError, TypeError):
            array = None
        if array is not None and array.dtype.kind in "biufc" and value:
            return to_julia(array)
        return jl.vect(*(to_julia(v, symbols=symbols) for v in value))
    return value


def _kwargs(kwargs, *, symbol_keys=()):
    return {
        key: jl.Symbol(value)
        if key in symbol_keys and isinstance(value, str)
        else to_julia(value)
        for key, value in kwargs.items()
    }


def to_python(value):
    """Recursively copy Julia dictionaries, tuples and arrays into Python/NumPy."""
    if isinstance(value, Mapping):
        return {str(k): to_python(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_python(v) for v in value]
    if isinstance(value, (str, int, float, complex, bool, type(None), np.ndarray)):
        return value
    if jl.isa(value, jl.AbstractDict):
        return {str(k): to_python(value[k]) for k in jl.keys(value)}
    if jl.isa(value, jl.Tuple):
        return tuple(to_python(v) for v in value)
    if jl.isa(value, jl.AbstractArray):
        if jl.seval("x -> eltype(x) <: Number")(value):
            return np.array(value, copy=True)
        return [to_python(v) for v in value]
    return value


def _convert_units(units):
    if isinstance(units, str):
        if units not in ("field", "si", "metric", "lab"):
            raise ValueError("units must be one of field, si, metric, lab")
        return jl.Symbol(units)
    return units


def convert_to_pydict(result, case=None, units=jl.missing):
    """Return WELLS, FIELD, DAYS and STATES as Python dictionaries/NumPy arrays."""
    if case is None:
        key = jl.Symbol("case")
        if not jl.haskey(result.extra, key):
            raise ValueError(
                "Pass case= when the result was not created by simulate_data_file()."
            )
        case = result.extra[key]
    summary = jl.JutulDarcy.summary_result(case, result, _convert_units(units))
    return {
        "WELLS": to_python(summary["VALUES"]["WELLS"]),
        "FIELD": to_python(summary["VALUES"]["FIELD"]),
        "DAYS": np.array(summary["TIME"].seconds) / 86400.0,
        "STATES": [to_python(state) for state in result.states],
    }


def symdict_to_pydict(value):
    """Convert Symbol keys to strings, keeping the dictionary values as Julia values."""
    return {str(k): v for k, v in value.items()}


def _stringdict_to_symdict(value):
    return to_julia(value)
