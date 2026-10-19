from pathlib import Path

import numpy as np
import pytest

import jutuldarcy as jd

pytestmark = pytest.mark.integration


@pytest.mark.parametrize(
    "value",
    [
        np.arange(6.0).reshape(2, 3),
        np.arange(6).reshape(2, 3),
        np.array([True, False]),
        np.array(1.0),
    ],
)
def test_native_array_roundtrip(value):
    native = jd.to_julia(value)
    assert jd.jl.isa(native, jd.jl.Array)
    np.testing.assert_array_equal(jd.to_python(native), value)


def test_nested_dictionary_and_sequence_conversion():
    data = jd.to_julia(
        {"Reservoir": {"Pressure": [1.0, 2.0]}, "limits": {"I": {"bhp": 1e5}}}
    )
    assert jd.jl.haskey(data, jd.jl.Symbol("Reservoir"))
    np.testing.assert_array_equal(
        jd.to_python(data)["Reservoir"]["Pressure"], [1.0, 2.0]
    )
    deck = jd.to_julia({"GRID": {"PORO": [0.2, 0.3]}}, symbols=False)
    assert jd.jl.haskey(deck, "GRID")
    assert jd.to_julia(Path("sample.DATA")) == str(Path("sample.DATA"))
    assert str(jd.jl.typeof(jd.to_julia((1, 2, 3)))).startswith("Tuple")
    assert jd.jl.length(jd.to_julia([])) == 0


def test_arrays_are_copies():
    source = np.array([1.0, 2.0])
    native = jd.to_julia(source)
    source[0] = 10.0
    assert jd.to_python(native)[0] == 1.0


def test_existing_julia_objects_pass_through():
    native = jd.jl.Dict()
    assert jd.to_julia(native) is native
