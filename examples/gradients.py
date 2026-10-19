"""Compute adjoint sensitivities with a Python objective.

The companion standalone example supplies the case. Preserve Julia automatic
differentiation values inside the objective: do not convert them to NumPy or
Python floats. Only the final objective value is converted for display.
"""

import numpy as np

import jutuldarcy as jd
from standalone import build_case


def pressure_objective(model, state, dt, step, forces):
    pressure = state[jd.jl.Symbol("Reservoir")][jd.jl.Symbol("Pressure")]
    return jd.jl.sum(pressure) * dt / 1e7


def main(output_dir=None):
    case = build_case(nx=3, ny=1, nz=1, nstep=2)
    result = jd.simulate_reservoir(
        case, mode="default", output_substates=True, info_level=-1
    )
    # output_substates=True exposes internal solver steps in result.states too.
    assert len(result.result.states) == len(case.dt)
    np.testing.assert_allclose(result.time[-1], np.sum(case.dt))
    gradients = jd.reservoir_sensitivities(
        case, result, pressure_objective, convert=True
    )
    porosity_gradient = gradients["porosity"]
    assert porosity_gradient.shape == (3,) and np.isfinite(porosity_gradient).all()
    value = float(jd.evaluate_objective(pressure_objective, case, result))
    print(f"Objective: {value:.6g}")
    print("Porosity gradient:", np.array2string(porosity_gradient, precision=4))
    return gradients


if __name__ == "__main__":
    main()
