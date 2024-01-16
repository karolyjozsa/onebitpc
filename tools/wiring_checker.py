"""Wire checker

This tool checks whether inputs of HW elements are defined and connected to
outputs correctly.

Usage
-----
@hw_elem
class Nand:
    @input
    def in1(self, val): ...
    @input
    def in2(self, val): ...

@input
def input_slot(val): ...

When a wire is connected to an input, this input_connected() below marks the
input connected.

After all HW element definitions and connections are done, the check() verifies
that all inputs are connected.
"""
from collections.abc import Callable

# Collect methods decorated with @input of classes decorated with @hw_elem
_inputs_by_classes: dict[str, list[str]] = {}

# List function names found in @hw_elem classes
_inputs_found_in_hwelem: list[str] = []

# Collect "connected" flag of functions decorated with @input 
_inputs_connected: dict[str, bool] = {}


def hw_elem(klass: type):
    """Decorator for a HW element class
    
    When this is called input decorators have already run and inputs_by_classes
    already contains the list of names of the input functions in this class.

    Augment the __init__() of the class, so that the @input instance methods
    are enumerated. They are stored in inputs_connected with the key being the
    repr() of the method, so that it is unique in all instances and the value
    flag, by default, not connected.
    """
    fully_qual_class_name = f"{klass.__module__}.{klass.__qualname__}"
    if fully_qual_class_name not in _inputs_by_classes:
        raise SystemError(f"{fully_qual_class_name} missing @input methods, or should not be @hw_elem")
    klass_init = klass.__init__
    def init(klass_self, *args, **kwargs):
        for fn_name in _inputs_by_classes[fully_qual_class_name]:
            _inputs_found_in_hwelem.append(f"{fully_qual_class_name}.{fn_name}")
            _register_input_fn(getattr(klass_self, fn_name))
        klass_init(klass_self, *args, **kwargs)
    klass.__init__ = init
    return klass

def input(fn: Callable):
    """Decorator for input

    This decorator runs while the class is still being parsed, i.e. the class
    itself does not exist yet.

    Get the fully qualified name (module, parent classes) of the class,
    containing the input function. This is key of the inputs_by_classes dict
    and it will store the names of the @input method names in this class.

    If this is not a method of a class, store it in inputs_connected with the
    key being the repr() of the method, so that it is unique in all instances
    and the value flag, by default, not connected.
    """
    class_qual_sections = fn.__qualname__.split('.<locals>', 1)[0].rsplit('.')
    class_qual_sections.pop()
    if not class_qual_sections:
        _register_input_fn(fn)
        return fn
    class_qual_sections.insert(0, fn.__module__)
    fully_qual_class_name = ".".join(class_qual_sections)
    if fully_qual_class_name not in _inputs_by_classes:
        _inputs_by_classes[fully_qual_class_name] = [fn.__name__]
    else:
        _inputs_by_classes[fully_qual_class_name].append(fn.__name__)
    return fn

def _register_input_fn(fn: Callable) -> None:
    """Register the input and mark it not-connected-yet"""
    fn_repr = fn.__repr__()
    if fn_repr in _inputs_connected:
        raise SystemError(f"{fn_repr} input already exists")
    _inputs_connected[fn_repr] = False

def input_connected(fn: Callable):
    """Mark the (registered) input as connected"""
    fn_repr = repr(fn)
    if fn_repr not in _inputs_connected:
        raise SystemError(f"{fn_repr} not an @input or its class is not a @hw_elem")
    if _inputs_connected[fn_repr]:
        raise SystemError(f"{fn_repr} @input already connected to an output")
    _inputs_connected[fn_repr] = True

def check():
    """Check that inputs are functions or correct class members, and all connected"""
    all_input_fn = [qc+"."+fn for qc, fnlist in _inputs_by_classes.items() for fn in fnlist]
    input_fn_outside_hwelem = set(all_input_fn) - set(_inputs_found_in_hwelem)
    if input_fn_outside_hwelem:
        raise SystemError(f"class(es) of @input method(s) {input_fn_outside_hwelem} missing @hw_elem")

    not_connected = [k for k,v in filter(lambda i: not i[1], _inputs_connected.items())]
    if not_connected:
        raise SystemError(f"{not_connected} input(s) not connected")
