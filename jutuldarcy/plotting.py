import juliapkg
from .julia_import import jl
import juliacall

def activate_plotting():
    try:
        jl.seval("using GLMakie")
    except:
        print("Unable to load GLMakie. Have you called install_plotting()?")
        return False
    return True

def install_plotting():
    juliapkg.add("GLMakie", "e9467ef8-e4e7-5192-8a1a-b1aee30e663a")
    activate_plotting()
    return True

def plot_reservoir(*arg, **kwarg):
    if activate_plotting():
        return jl.plot_reservoir(*arg, **kwarg)

def plot_well_results(*arg, **kwarg):
    if activate_plotting():
        return jl.plot_well_results(*arg, **kwarg)

def plot_field_measurables(*arg, **kwarg):
    if activate_plotting():
        return jl.plot_field_measurables(*arg, **kwarg)

def make_interactive():
    juliacall.interactive()
