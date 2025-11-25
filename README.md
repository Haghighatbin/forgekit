# forgekit

A personal collection of Python utilities for development, debugging, and documentation.

## Installation

```bash
pip install forgekit
```

Or for development:

```bash
git clone https://github.com/yourusername/forgekit.git
cd forgekit
pip install -e .
```

## Modules

### `garnish` - Function Decorators

Adds flavour to the functions with debugging and profiling decorators.

```python
from forgekit.garnish import timeit, trace, argtype

@timeit
@trace
def process_data(data, threshold=0.5):
    # Code here
    return result

# Output:
# Calling __main__.process_data with:
#    args: ([1, 2, 3],)
#    kwargs: {'threshold': 0.5}
# Execution speed of __main__.process_data:
# took 0.123 seconds.
```

**Available decorators:**
- `@timeit` - Measures execution time
- `@trace` - Displays function calls with arguments
- `@argtype` - Shows argument types
- `@cputime` - CPU profiling statistics
- `@docs` - Displays function docstrings
- `@profile_all` - Comprehensive profiling

**Context managers:**
```python
from forgekit.garnish import Timer, Profiler

with Timer("Data processing"):
    # Code here
    pass

with Profiler("Algorithm execution"):
    # Code here
    pass
```

### `docweaver` - Automatic Documentation

Generate Google-style docstring skeletons for your Python code.

```python
from forgekit.docweaver import process_file

# Add docstrings to functions and classes that don't have them
process_file('input.py', 'output_with_docs.py')
```

**Command line usage:**
```bash
python -m forgekit.docweaver input.py output.py
```

### `logman` - Logging Utilities

Rich console logging with automatic file rotation.

```python
from forgekit.logman import get_logger, collect_run_metadata

logger = get_logger(__name__)
logger.info("Processing started")

# Collect metadata about the current run
metadata = collect_run_metadata(seed=42)
logger.info(f"Run metadata: {metadata}")
```

**Features:**
- Automatic log rotation (5MB per file, 5 backups)
- Rich console output with tracebacks
- Run metadata collection (git SHA, Python version, host, etc.)
- Timestamp formatting

### `banner` - ASCII Art Banners

Display stylish ASCII art headers for your CLI applications.

```python
from forgekit.banner import Logo

Logo(version="1.0.0", author="Name")
# Displays a 3D ASCII art title with version and author info
```

### `exceptions` - Custom Exception Hierarchy

Pre-built exception classes for common error scenarios.

```python
from forgekit.exceptions import (
    DataNotFoundError,
    NetworkError,
    ModelNotTrainedError,
    InvalidConfigurationError
)

def load_data(filepath):
    if not os.path.exists(filepath):
        raise DataNotFoundError(f"Data file not found: {filepath}")
    # ...
```

**Exception categories:**
- Network errors (`NetworkError`)
- Data errors (`DataError`, `DataNotFoundError`, `DataProcessingError`)
- File errors (`FileError`, `InvalidPathError`)
- Configuration errors (`ConfigError`, `InvalidConfigurationError`)
- Model errors (`ModelError`, `ModelNotTrainedError`, `ModelLoadingError`)
- Signal errors (`SignalError`, `SlackNotificationError`)
- Database errors (`DatabaseError`, `DatabaseConnectionError`, `DatabaseQueryError`)

## Requirements

- Python 3.9+
- Dependencies: `rich`, `pyfiglet`

## Contributing

This is a personal toolkit, but suggestions and improvements are welcome. Feel free to open an issue or submit a pull request.

## Licence

MIT Licence - See LICENSE file for details.

## Author

Amin Haghighatbin  
