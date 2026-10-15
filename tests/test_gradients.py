import numpy as np
import pytest

import jutuldarcy as jd

pytestmark = pytest.mark.integration


def pressure_objective(model, state, dt, step, forces):
    return (
        jd.jl.sum(state[jd.jl.Symbol("Reservoir")][jd.jl.Symbol("Pressure")]) * dt / 1e7
    )


def test_adjoint_matches_finite_difference(tiny_case):
    # Adjoint support operates on the host model and needs output substates.
    result = jd.simulate_reservoir(
        tiny_case, mode="default", output_substates=True, info_level=-1
    )
    gradients = jd.reservoir_sensitivities(
        tiny_case, result, pressure_objective, convert=True
    )
    assert "porosity" in gradients
    assert np.isfinite(gradients["porosity"]).all()
    eps = 1e-5
    values = []
    for sign in (-1, 1):
        case = jd.jl.deepcopy(tiny_case)
        domain = jd.reservoir_domain(case)
        porosity = np.array(domain[jd.jl.Symbol("porosity")])
        porosity[0] += sign * eps
        domain[jd.jl.Symbol("porosity")] = jd.to_julia(porosity)
        parameters = jd.setup_parameters(case.model)
        case = jd.setup_jutul_case(
            case.state0, case.model, case.dt, case.forces, parameters
        )
        perturbed = jd.simulate_reservoir(case, mode="default", info_level=-1)
        values.append(float(jd.evaluate_objective(pressure_objective, case, perturbed)))
    finite_difference = (values[1] - values[0]) / (2 * eps)
    np.testing.assert_allclose(
        gradients["porosity"][0], finite_difference, rtol=5e-3, atol=1e-3
    )


def test_julia_objective_and_optimization_config(tiny_case):
    objective = jd.jl.seval(
        "(model, state, dt, step, forces) -> sum(state[:Reservoir][:Pressure])*dt/1e7"
    )
    result, gradients = jd.reservoir_sensitivities(
        tiny_case,
        objective,
        convert=True,
        sim_arg={"mode": "default", "output_substates": True, "info_level": -1},
    )
    assert len(result.states) == 2
    assert np.isfinite(gradients["porosity"]).all()
    assert jd.optimization_config(tiny_case.model, tiny_case.parameters) is not None
    assert jd.optimization_config(tiny_case) is not None
    problem = jd.setup_reservoir_parameter_optimization(
        tiny_case, objective, print=False
    )
    assert np.isfinite(getattr(problem, "F!")(problem.x0))
