import juliapkg
from .julia_import import jl
import juliacall
import asyncio

def activate_plotting():
    try:
        jl.seval("using GLMakie")
    except:
        print("Unable to load GLMakie. Have you called install_plotting()?")
        return False
    return True

def install_plotting():
    juliapkg.add("GLMakie", "e9467ef8-e4e7-5192-8a1a-b1aee30e663a")
    juliapkg.resolve()
    activate_plotting()
    return True

def uninstall_plotting():
    juliapkg.rm("GLMakie", "e9467ef8-e4e7-5192-8a1a-b1aee30e663a")
    juliapkg.resolve()
    return True

def plot_reservoir(*arg, **kwarg):
    return plot_async(jl.plot_reservoir, *arg, **kwarg)

def plot_well_results(*arg, **kwarg):
    return plot_async(jl.plot_well_results, *arg, **kwarg)

def plot_field_measurables(*arg, **kwarg):
    return plot_async(jl.plot_field_measurables, *arg, **kwarg)

# def plot_summary(*arg, **kwarg):
#     return plot_async(jl.JutulDarcy.plot_summary, *arg, **kwarg)

def make_interactive():
    juliacall.interactive()

def plot_async(F, *arg, **kwargs):
    if activate_plotting():
        try:
            loop = asyncio.get_event_loop()
            # Notebook or already running loop
            loop.create_task(plot_alive(F, *arg, **kwargs))

        except RuntimeError:
            # Script: no loop running, so start one
            asyncio.run(plot_alive(F, *arg, **kwargs))

async def plot_alive(F, *arg, **kwargs):
    print("Plotting... (close the plot window to end the plot and restore the terminal)")
    fig = F(*arg, **kwargs)
    jl.display(fig)
    while True:
        if not jl.isopen(fig.scene):
            break
        jl.seval("yield()")
        await asyncio.sleep(0.01)
