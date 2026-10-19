"""The integration suite must exercise the registered 0.4 release series."""

import pytest

import jutuldarcy as jd

pytestmark = pytest.mark.integration


def test_released_jutuldarcy():
    version = str(jd.jl.Base.pkgversion(jd.jl.JutulDarcy))
    assert tuple(map(int, version.split(".")[:2])) == (0, 4)
    assert jd.jl.seval(
        "Pkg.dependencies()[Base.PkgId(JutulDarcy).uuid].is_tracking_registry"
    )
