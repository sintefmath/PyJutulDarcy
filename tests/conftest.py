import numpy as np
import pytest

import jutuldarcy as jd


@pytest.fixture(scope="session")
def tiny_case():
    mesh = jd.reservoir_mesh((3, 1, 1), (30.0, 10.0, 10.0))
    domain = jd.reservoir_domain(
        mesh, permeability=np.full(3, 1e-12), porosity=[0.2, 0.25, 0.3]
    )
    system = jd.ImmiscibleSystem(
        [jd.AqueousPhase(), jd.LiquidPhase()], reference_densities=[1000.0, 800.0]
    )
    injector = jd.setup_well(domain, [1], name="Injector")
    producer = jd.setup_well(domain, (3, 1, 1), name="Producer")
    model = jd.setup_reservoir_model(domain, system, wells=[injector, producer])
    density = jd.ConstantCompressibilityDensities(
        p_ref=1e7, density_ref=[1000.0, 800.0], compressibility=[1e-9, 1e-9]
    )
    jd.replace_variables(model, PhaseMassDensities=density)
    jd.replace_variables(
        model,
        RelativePermeabilities=jd.BrooksCoreyRelativePermeabilities(system, [2.0, 2.0]),
    )
    state = jd.setup_reservoir_state(model, Pressure=1e7, Saturations=[0.2, 0.8])
    forces = jd.setup_reservoir_forces(
        model,
        control={
            "Injector": jd.setup_injector_control(
                1e-4, "rate", [1.0, 0.0], density=1000.0
            ),
            "Producer": jd.setup_producer_control(9e6, "bhp"),
        },
        limits={"Producer": {"bhp": 1e5}},
    )
    return jd.setup_jutul_case(state, model, [86400.0, 86400.0], forces)
