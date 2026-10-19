import os

import pytest

import jutuldarcy as jd

pytestmark = [
    pytest.mark.integration,
    pytest.mark.plotting,
    pytest.mark.skipif(
        os.environ.get("PYJUTULDARCY_TEST_PLOTTING") != "1",
        reason="Set PYJUTULDARCY_TEST_PLOTTING=1 with CairoMakie installed",
    ),
]


def test_plot_reservoir_returns_renderable_figure(tiny_case, tmp_path):
    jd.activate_plotting("CairoMakie")
    result = jd.simulate_reservoir(tiny_case, info_level=-1)
    # Test both native simulation results and Python-converted state containers.
    for states in (result, jd.to_python(result.states)):
        figure = jd.plot_reservoir(
            tiny_case.model, states, display=False, key="Pressure"
        )
        path = tmp_path / ("python.png" if isinstance(states, list) else "native.png")
        jd.jl.CairoMakie.save(str(path), figure)
        assert path.stat().st_size > 1000
