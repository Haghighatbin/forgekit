from functools import wraps
import cProfile
import pstats
import inspect
import time
import logging
from typing import Callable, Any, Optional
from io import StringIO


logger = logging.getLogger(__name__)


def argtype(func: Callable) -> Callable:
    """Shows the type of passed arguments for the given function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        arg_names = inspect.getfullargspec(func).args
        arg_types = [f"{name}: {type(arg).__name__}" for name, arg in zip(arg_names, args)]
        kwarg_types = [f"{key}: {type(value).__name__}" for key, value in kwargs.items()]
        
        output = f"Calling {func.__name__} with arguments:\n  {arg_types}"
        if kwarg_types:
            output += f'\n  keyword-arguments: {kwarg_types}'
        
        logger.info(output)
        print(output)
        return func(*args, **kwargs)
    return wrapper


def cputime(func: Callable, sort_by: str = 'cumulative', limit: int = 20) -> Callable:
    """
    Display CPU time statistics of given function.
    
    Args:
        func: Function to profile
        sort_by: Sort key for statistics ('cumulative', 'time', 'calls', etc.)
        limit: Number of lines to display in profile output
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        scope = _get_scope(func, args)
        print(f'CPU runtime for {scope}:')
        
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        
        # Redirect profile output to string buffer for better control
        string_buffer = StringIO()
        stats = pstats.Stats(profiler, stream=string_buffer)
        stats.sort_stats(sort_by)
        stats.print_stats(limit)
        
        print(string_buffer.getvalue())
        return result
    return wrapper


def docs(func: Callable) -> Callable:
    """Display docstrings of given function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        scope = _get_scope(func, args)
        print(f'Documentation for {scope}:')
        doc = inspect.getdoc(func)
        if doc:
            print(doc)
        else:
            print("No documentation available.")
        return func(*args, **kwargs)
    return wrapper


def timeit(func: Callable, precision: int = 3) -> Callable:
    """
    Display runtime statistics of given function.
    
    Args:
        func: Function to time
        precision: Decimal places for time display
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        scope = _get_scope(func, args)
        print(f'Execution speed of {scope}:')
        
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        elapsed = end_time - start_time
        print(f'took {elapsed:.{precision}f} seconds.')
        
        logger.info(f'{scope} took {elapsed:.{precision}f} seconds')
        return result
    return wrapper


def trace(func: Callable, verbose: bool = True) -> Callable:
    """
    Display argument and context call information of given function.
    
    Args:
        func: Function to trace
        verbose: If True, show full argument details; if False, show summary
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        scope = _get_scope(func, args)
        
        if verbose:
            print(f'Calling {scope} with:')
            print(f'   args: {args}')
            print(f'   kwargs: {kwargs}')
        else:
            print(f'Calling {scope} with {len(args)} args and {len(kwargs)} kwargs')
        
        logger.debug(f'Trace: {scope}(args={args}, kwargs={kwargs})')
        return func(*args, **kwargs)
    return wrapper


def profile_all(func: Callable, 
                show_args: bool = True,
                show_time: bool = True,
                show_cpu: bool = False) -> Callable:
    """
    Comprehensive profiling decorator combining multiple utilities.
    
    Args:
        func: Function to profile
        show_args: Display argument types
        show_time: Display execution time
        show_cpu: Display CPU profiling statistics
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        scope = _get_scope(func, args)
        
        if show_args:
            arg_names = inspect.getfullargspec(func).args
            arg_types = [f"{name}: {type(arg).__name__}" for name, arg in zip(arg_names, args)]
            print(f'\n{"="*60}')
            print(f'Profiling {scope}')
            print(f'Arguments: {arg_types}')
            if kwargs:
                print(f'Keyword arguments: {list(kwargs.keys())}')
        
        if show_cpu:
            profiler = cProfile.Profile()
            profiler.enable()
        
        if show_time:
            start_time = time.perf_counter()
        
        result = func(*args, **kwargs)
        
        if show_time:
            elapsed = time.perf_counter() - start_time
            print(f'Execution time: {elapsed:.3f} seconds')
        
        if show_cpu:
            profiler.disable()
            string_buffer = StringIO()
            stats = pstats.Stats(profiler, stream=string_buffer)
            stats.sort_stats('cumulative')
            stats.print_stats(10)
            print('\nCPU Profile (top 10):')
            print(string_buffer.getvalue())
        
        if show_args or show_time or show_cpu:
            print(f'{"="*60}\n')
        
        return result
    return wrapper


def _get_scope(func: Callable, args: tuple) -> str:
    """
    Get scope name of the given function.
    
    Args:
        func: Function to inspect
        args: Arguments passed to the function
        
    Returns:
        Fully qualified function name (module.Class.method or module.function)
    """
    module = inspect.getmodule(func)
    scope = module.__name__ if module else '<unknown>'
    
    try:
        # Check if this is a method by examining the first argument
        if args and hasattr(args[0], '__class__'):
            class_obj = args[0].__class__
            # Verify the function actually belongs to this class
            if hasattr(class_obj, func.__name__):
                class_method = getattr(class_obj, func.__name__)
                # Check if it's the same function (accounting for bound methods)
                if (hasattr(class_method, '__func__') and 
                    class_method.__func__ is func) or class_method is func:
                    scope += f'.{class_obj.__name__}.{func.__name__}'
                    return scope
        
        scope += f'.{func.__name__}'
    except (IndexError, AttributeError):
        scope += f'.{func.__name__}'
    
    return scope


# Context manager for ad-hoc profiling
class Timer:
    """
    Context manager for timing code blocks.
    
    Usage:
        with Timer("My operation"):
            # code to time
            pass
    """
    def __init__(self, description: str = "Operation", precision: int = 3):
        self.description = description
        self.precision = precision
        self.start_time: Optional[float] = None
        self.elapsed: Optional[float] = None
    
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start_time
        print(f'{self.description} took {self.elapsed:.{self.precision}f} seconds')
        return False


class Profiler:
    """
    Context manager for CPU profiling code blocks.
    
    Usage:
        with Profiler("My operation"):
            # code to profile
            pass
    """
    def __init__(self, description: str = "Operation", limit: int = 20):
        self.description = description
        self.limit = limit
        self.profiler: Optional[cProfile.Profile] = None
    
    def __enter__(self):
        self.profiler = cProfile.Profile()
        self.profiler.enable()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.profiler.disable()
        string_buffer = StringIO()
        stats = pstats.Stats(self.profiler, stream=string_buffer)
        stats.sort_stats('cumulative')
        stats.print_stats(self.limit)
        
        print(f'\nCPU Profile for {self.description}:')
        print(string_buffer.getvalue())
        return False


if __name__ == "__main__":
    # Example usage
    
    @timeit
    @argtype
    def example_function(x: int, y: int, multiplier: float = 1.0) -> float:
        """Example function demonstrating the decorators."""
        time.sleep(0.1)
        return (x + y) * multiplier
    
    
    class ExampleClass:
        @trace
        def method(self, value: int) -> int:
            """Example method in a class."""
            return value * 2
    
    
    # Test the decorators
    print("Testing function decorator:")
    result = example_function(5, 3, multiplier=2.0)
    print(f"Result: {result}\n")
    
    print("Testing method decorator:")
    obj = ExampleClass()
    obj.method(10)
    
    print("\nTesting context manager:")
    with Timer("Sleep operation"):
        time.sleep(0.05)