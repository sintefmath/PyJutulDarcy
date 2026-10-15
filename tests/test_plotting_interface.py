import asyncio
from types import SimpleNamespace

import pytest

import jutuldarcy.plotting as plotting


@pytest.fixture
def fake_plot(monkeypatch):
    figure = SimpleNamespace(scene=object())
    displayed = []
    monkeypatch.setattr(plotting, "_backend", "GLMakie")
    monkeypatch.setattr(
        plotting,
        "jl",
        SimpleNamespace(
            hasproperty=lambda value, name: hasattr(value, name),
            Symbol=str,
            display=displayed.append,
            isopen=lambda scene: False,
        ),
    )
    monkeypatch.setattr(plotting, "make_interactive", lambda: None)
    return figure, displayed


def test_explorer_figure_is_returned_and_displayed(fake_plot):
    figure, displayed = fake_plot
    result = plotting.plot_async(lambda: SimpleNamespace(fig=figure))
    assert result is figure
    assert displayed == [figure]


def test_figure_returns_inside_running_event_loop(fake_plot):
    figure, _ = fake_plot

    async def render():
        assert plotting.plot_async(lambda: figure) is figure
        await asyncio.sleep(0)

    asyncio.run(render())


def test_plot_errors_propagate(fake_plot):
    def broken():
        raise RuntimeError("plot failed")

    with pytest.raises(RuntimeError, match="plot failed"):
        plotting.plot_async(broken)
