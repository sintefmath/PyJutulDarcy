import numpy as np
import pytest

import jutuldarcy as jd

pytestmark = pytest.mark.integration


def test_mesh_domain_and_helpers(tiny_case):
    assert jd.number_of_cells(jd.reservoir_mesh(tiny_case)) == 3
    assert jd.number_of_cells(jd.reservoir_mesh(nx=2, ny=2, nz=1)) == 4
    assert jd.number_of_cells(jd.reservoir_mesh(np.array([2, 2, 1]), [20, 20, 1])) == 4
    mesh = jd.CartesianMesh([2, 2, 1], (20.0, 20.0, 1.0))
    domain = jd.reservoir_domain(
        jd.UnstructuredMesh(mesh),
        permeability=np.full((3, 4), 1e-12),
        porosity=[0.2] * 4,
    )
    assert jd.number_of_cells(domain) == 4
    assert jd.number_of_faces(mesh) > 0
    np.testing.assert_allclose(np.array(jd.pore_volume(domain)), 20.0)
    assert jd.si_unit("day") == 86400.0
    assert set(jd.well_symbols(tiny_case.model)) == {"Injector", "Producer"}
    assert jd.jl.length(jd.setup_parameters(tiny_case.model)) > 0


def test_relperm_and_capillary_tables(tiny_case):
    model = jd.jl.deepcopy(tiny_case.model)
    s = np.linspace(0.0, 1.0, 5)
    kr = jd.PhaseRelativePermeability(s, s**2, label="w")
    assert jd.jl.isa(kr, jd.jl.JutulDarcy.PhaseRelativePermeability)
    assert jd.TabulatedSimpleRelativePermeabilities(s, [s**2, s**3]) is not None
    assert jd.TabulatedSimpleRelativePermeabilities([s, s], [s**2, s**3]) is not None
    assert (
        jd.set_relative_permeability(
            model, swof=np.column_stack([s, s**2, (1 - s) ** 2]), regions=[1, 1, 1]
        )
        is model
    )
    assert (
        jd.set_capillary_pressure(model, pcow=np.column_stack([s, 1e4 * (1 - s)]))
        is model
    )
    parameters = jd.setup_parameters(model)
    assert parameters is not None


def test_sources_and_boundary_conditions(tiny_case):
    src = jd.SourceTerm(1, 1e-4, fractional_flow=[1.0, 0.0], type="VolumeSource")
    bc = jd.FlowBoundaryCondition(3, 1e7, fractional_flow=[0.0, 1.0])
    forces = jd.setup_reservoir_forces(tiny_case.model, sources=[src], bc=[bc])
    assert jd.jl.length(forces[jd.jl.Symbol("Reservoir")].sources) == 1


def test_well_controls_validate_kind():
    with pytest.raises(ValueError, match="Unknown well control"):
        jd.setup_producer_control(1.0, "nonsense")


def test_simulation_and_python_result(tiny_case):
    result = jd.simulate_reservoir(tiny_case, info_level=-1)
    assert len(result.states) == 2
    assert "KernelAbstractions" in str(
        jd.jl.typeof(
            result.extra[jd.jl.Symbol("simulator")]
            .model[jd.jl.Symbol("Reservoir")]
            .context
        )
    )
    output = jd.convert_to_pydict(result, tiny_case, units="si")
    assert set(output) == {"WELLS", "FIELD", "DAYS", "STATES"}
    np.testing.assert_allclose(output["DAYS"], [1, 2])
    assert output["STATES"][0]["Pressure"].shape == (3,)
    assert np.isfinite(output["STATES"][-1]["Saturations"]).all()
    with pytest.raises(ValueError, match="case="):
        jd.convert_to_pydict(result)


def test_simulator_and_legacy_mode(tiny_case):
    simulator, config = jd.setup_reservoir_simulator(
        tiny_case, mode="default", info_level=-1
    )
    output = jd.simulate_reservoir(
        tiny_case, simulator=simulator, config=config, convert=True
    )
    assert len(output["STATES"]) == 2
    output2 = jd.simulate_reservoir(
        tiny_case.state0,
        tiny_case.model,
        [86400.0],
        forces=tiny_case.forces,
        convert=True,
        info_level=-1,
    )
    assert len(output2["STATES"]) == 1
