"""Build and simulate a two-phase injection model.

This is a small Python version of the Julia manual's first model:
https://sintefmath.github.io/JutulDarcy.jl/stable/man/first_ex
All input quantities use SI units; well coordinates are one-based.
"""

import numpy as np

import jutuldarcy as jd


def build_case(nx=10, ny=10, nz=3, nstep=12):
    day = jd.si_unit("day")
    darcy = jd.si_unit("darcy")
    bar = jd.si_unit("bar")
    mesh = jd.reservoir_mesh((nx, ny, nz), (1000.0, 1000.0, 100.0))
    domain = jd.reservoir_domain(mesh, permeability=0.3 * darcy, porosity=0.2)
    injector = jd.setup_vertical_well(domain, 1, 1, name="Injector")
    producer = jd.setup_well(domain, (nx, ny, 1), name="Producer")
    densities = [1000.0, 100.0]  # kg/m³ at reference conditions
    system = jd.ImmiscibleSystem(
        (jd.LiquidPhase(), jd.VaporPhase()), reference_densities=densities
    )
    model = jd.setup_reservoir_model(domain, system, wells=[injector, producer])
    density = jd.ConstantCompressibilityDensities(
        p_ref=100 * bar,
        density_ref=densities,
        compressibility=[1e-6 / bar, 1e-4 / bar],
    )
    relperm = jd.BrooksCoreyRelativePermeabilities(system, [2.0, 3.0])
    jd.replace_variables(model, PhaseMassDensities=density, RelativePermeabilities=relperm)
    state0 = jd.setup_reservoir_state(model, Pressure=120 * bar, Saturations=[1.0, 0.0])
    dt = np.full(nstep, 90.0 * day)
    # Inject 1.5 pore volumes over the simulation period.
    injection_rate = 1.5 * np.sum(jd.pore_volume(model)) / np.sum(dt)
    forces = jd.setup_reservoir_forces(
        model,
        control={
            "Injector": jd.setup_injector_control(
                injection_rate, "rate", [0.0, 1.0], density=densities[1]
            ),
            "Producer": jd.setup_producer_control(100 * bar, "bhp"),
        },
    )
    return jd.setup_jutul_case(state0, model, dt, forces)


def main(output_dir=None):
    case = build_case()
    result = jd.simulate_reservoir(case, info_level=-1)
    output = jd.convert_to_pydict(result, case, units="field")
    np.testing.assert_allclose(output["DAYS"], np.arange(1, 13) * 90.0)
    pressure = output["STATES"][-1]["Pressure"]
    assert pressure.shape == (300,) and np.isfinite(pressure).all()
    print(f"Completed {len(result.states)} reporting steps on {pressure.size} cells.")
    print(f"Final mean pressure: {pressure.mean() / jd.si_unit('bar'):.2f} bar")
    return case, result, output


if __name__ == "__main__":
    main()
