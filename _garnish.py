from functools import wraps
import cProfile
import inspect
import time


def argtype(func):
    """Shows the type of passed arguments for the given function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        arg_names = inspect.getfullargspec(func).args
        arg_types = [f"{name}: {type(arg)}" if arg is not None else 'None' for name, arg in zip(arg_names, args)]
        kwarg_types = [f"{key}: {type(value).__name__}" if value is not None else f"{key}: None" for key, value in kwargs.items()]
        print(f"Calling {func.__name__} with arguments:\n {arg_types}")
        if kwarg_types:
            print(f'keyword-arguments:\n {kwarg_types}\n')
        return func(*args, **kwargs)

    return wrapper

def cputime(f):
    """Display CPU Time statistics of given function."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        print(f'CPU runtime for {_get_scope(f, args)}:')

        t = cProfile.Profile()
        r = t.runcall(f, *args, **kwargs)
        t.print_stats()

        return r

    return wrapper

def docs(f):
    """Display Docstrings of given function."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        print(f'Documentation for {_get_scope(f, args)}:')
        print(inspect.getdoc(f))

        return f(*args, **kwargs)

    return wrapper

def timeit(f):
    """Display Runtime statistics of given function."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        print(f'Execution speed of {_get_scope(f, args)}:')
        _t0 = time.time()
        _runtime = f(*args, **kwargs)
        _t1 = time.time()

        print(f'took {_t1 - _t0:.3f} seconds.')

        return _runtime

    return wrapper

def trace(f):
    """Display epic argument and context call information of given function."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        _scope = _get_scope(f, args)

        print(f'Calling {_scope} with:')
        print(f'   args: {args}')
        print(f'   kwargs: {kwargs}')

        return f(*args, **kwargs)

    return wrapper

def _get_scope(f, args):
    """Get scope name of the given function."""

    _scope = inspect.getmodule(f).__name__
    try:
        if f.__name__ in dir(args[0].__class__):
            _scope += '.' + args[0].__class__.__name__
            _scope += '.' + f.__name__
        else:
            _scope += '.' + f.__name__
    except IndexError:
        _scope += '.' + f.__name__

    return _scope
