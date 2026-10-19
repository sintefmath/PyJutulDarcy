from types import SimpleNamespace

import pytest

import jutuldarcy.backends as backends


@pytest.fixture
def fake_environment(monkeypatch):
    calls = []
    fake = SimpleNamespace(
        _package_present=lambda name: False,
        _load_optional_package=lambda *args: calls.append(("using", args)),
        _remove_optional_package=lambda name: calls.append(("remove", name)),
        CUDA=SimpleNamespace(functional=lambda: True),
        AMDGPU=SimpleNamespace(functional=lambda: True),
        Symbol=str,
    )
    monkeypatch.setattr(backends, "jl", fake)
    monkeypatch.setattr(backends, "_enabled", set())
    monkeypatch.setattr(
        backends.juliapkg, "add", lambda *args: calls.append(("add", args))
    )
    monkeypatch.setattr(
        backends.juliapkg, "rm", lambda *args: calls.append(("rm", args))
    )
    monkeypatch.setattr(
        backends.juliapkg, "resolve", lambda: calls.append(("resolve",))
    )
    return fake, calls


@pytest.mark.parametrize(
    "key,activate,remove",
    [
        ("cuda", backends.activate_cuda, backends.remove_cuda),
        ("amd", backends.activate_amd, backends.remove_amd),
    ],
)
def test_optional_backend_lifecycle(fake_environment, key, activate, remove):
    fake, calls = fake_environment
    assert activate()
    assert len([call for call in calls if call[0] == "add"]) == 1
    fake._package_present = lambda name: True
    assert activate()
    assert len([call for call in calls if call[0] == "add"]) == 1
    assert backends._simulation_kwargs(gpu=True)["mode"] == f"ka_{key}"
    assert backends._simulation_kwargs(gpu=key)["mode"] == f"ka_{key}"
    assert remove()
    assert backends.available_backends() == []
    assert any(call[0] == "rm" for call in calls)


def test_gpu_selection_fails_without_functional_backend(fake_environment):
    fake, _ = fake_environment
    assert backends._simulation_kwargs()["mode"] == "ka"
    with pytest.raises(RuntimeError, match="functional"):
        backends._simulation_kwargs(gpu=True)
    fake.CUDA.functional = lambda: False
    assert not backends.activate_cuda()
    with pytest.raises(RuntimeError):
        backends._simulation_kwargs(mode="ka_cuda")
    with pytest.raises(ValueError):
        backends._simulation_kwargs(mode="default", gpu=True)


def test_gpu_priority_and_explicit_selection(fake_environment):
    backends.activate_cuda()
    backends.activate_amd()
    assert backends._simulation_kwargs(gpu=True)["mode"] == "ka_cuda"
    assert backends._simulation_kwargs(mode="gpu")["mode"] == "ka_cuda"
    assert backends._simulation_kwargs(gpu="amdgpu")["mode"] == "ka_amd"
