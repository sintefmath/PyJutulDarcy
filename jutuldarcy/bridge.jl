# Kept in Julia so Python objectives preserve ForwardDiff dual numbers.
using PythonCall
import Pkg
import Base: vect

_package_present(name) = any(p -> p.name == name, values(Pkg.dependencies()))
_direct_dependency(name) = haskey(Pkg.project().dependencies, name)

function _load_optional_package(name, uuid)
    # A package may already exist as an indirect dependency. Loading by PkgId
    # avoids adding it again just to make `using Name` work in the active project.
    mod = Base.require(Base.PkgId(Base.UUID(uuid), name))
    Core.eval(@__MODULE__, Expr(:(=), Symbol(name), QuoteNode(mod)))
    return mod
end

function _remove_optional_package(name)
    if _direct_dependency(name)
        Pkg.rm(name)
    end
    return nothing
end

function _python_objective(f::Py)
    return function (args...)
        value = f(args...)
        return pyconvert(Any, value)
    end
end
_python_objective(f) = f

function _gradient_dict(domain)
    out = Dict{Symbol, Any}()
    for (key, (value, entity)) in pairs(domain.data)
        out[key] = value
    end
    return out
end
