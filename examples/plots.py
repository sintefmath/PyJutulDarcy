# Example of plotting a reservoir simulation result using JutulDarcy's plotting
# functions. These plots use GLMakie, which requires an OpenGL-capable
# environment. If you are running in an environment that does not support
# plotting, you can still run the simulation and convert the results to a Python
# dictionary (see examples/standalone.py for an example of this) and then use a
# Python plotting library to visualize the results.
import jutuldarcy as jd

pth = jd.test_file_path("SPE9", "SPE9.DATA")
case = jd.setup_case_from_data_file(pth)
result = jd.simulate_reservoir(case)
if not jd.activate_plotting():
    print(
        "Plotting is not available in this environment. Please run jd.install_plotting() and try again."
    )
# Plot the reservoir results (3D)
jd.plot_reservoir(case.model, result.states)
# Plot the well results (2D)
jd.plot_well_results(result)
