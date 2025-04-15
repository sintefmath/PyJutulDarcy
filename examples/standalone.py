import importlib
import jutuldarcy as jd
import numpy as np
importlib.reload(jd)
# Grab some unit conversion factors
day = jd.si_unit("day")
Darcy = jd.si_unit("darcy")
kg = jd.si_unit("kilogram")
meter = jd.si_unit("meter")
bar = jd.si_unit("bar")
# Set up mesh
nx = ny = 25
nz = 10
cart_dims = (nx, ny, nz)
physical_dims = (1000.0*meter, 1000.0*meter, 100.0*meter)
g = jd.CartesianMesh(cart_dims, physical_dims)
domain = jd.reservoir_domain(g, permeability = 0.3*Darcy, porosity = 0.2)
Injector = jd.setup_vertical_well(domain, 1, 1, name = "Injector")
Producer = jd.setup_well(domain, (nx, ny, 1), name = "Producer")
# Show the properties in the domain
phases = (jd.LiquidPhase(), jd.VaporPhase())
rhoLS = 1000.0*kg/meter**3
rhoGS = 100.0*kg/meter**3
reference_densities = [rhoLS, rhoGS]
sys = jd.ImmiscibleSystem(phases, reference_densities = reference_densities)
model, parameters = jd.setup_reservoir_model(domain, sys, wells = [Injector, Producer])
# Replace dynamic functions with custom ones
c = np.array([1e-6/bar, 1e-4/bar])
density = jd.jl.ConstantCompressibilityDensities(
    p_ref = 100*bar,
    density_ref = reference_densities,
    compressibility = c
)
kr = jd.jl.BrooksCoreyRelativePermeabilities(sys, np.array([2.0, 3.0]))
jd.replace_variables(model, PhaseMassDensities = density, RelativePermeabilities = kr)
# Set the initial conditions
state0 = jd.setup_reservoir_state(model,
    Pressure = 120*bar,
    Saturations = np.array([1.0, 0.0])
)
# Set up reporting steps
nstep = 25
dt = np.repeat(365.0*day, nstep)
# Set up timestepping and well controls
pv = jd.pore_volume(model, parameters)
inj_rate = 1.5*np.sum(pv)/sum(dt)
I_ctrl = jd.setup_injector_control(inj_rate, "rate", np.array([0.0, 1.0]), density = rhoGS)
P_ctrl = jd.setup_producer_control(100*bar, "bhp")
controls = dict(Injector = I_ctrl, Producer = P_ctrl)
forces = jd.setup_reservoir_forces(model, control = controls)
result = jd.simulate_reservoir(state0, model, dt, parameters = parameters, forces = forces)

# To run the following:
# 1. Run in an environment that supports plotting (OpenGL capable)
# 2. Run jd.install_plotting()
# 
plt = jd.plot_reservoir(model, result.states)
jd.make_interactive()
