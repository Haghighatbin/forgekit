"""
exceptions.py
Custom exceptions for the stock signal generation project.
"""

class StockSignalError(Exception):
    """
    Base exception for all custom exceptions in the Stock Signal Generation project.
    """
    pass

# -- Network-Related Errors -------------------------------------------------- #
class NetworkError(StockSignalError):
    """
    Raised when a network request fails or times out.
    """
    pass

# -- Data-related Errors ------------------------------------------------------ #
class DataNotFoundError(StockSignalError):
    """
    Raised when required data (e.g., a file, dataset, or record) is invalid.
    """
    pass

class DataError(StockSignalError):
    """
    Raised when required data (e.g., a file, dataset, or record) is missing.
    """
    pass

class DataProcessingError(StockSignalError):
    """
    Raised when there's an error processing or transforming data.
    """
    pass

# -- File-related Errors ------------------------------------------------------ #
class FileError(StockSignalError):
    """
    General file-related error within the project.
    """
    pass


class InvalidPathError(FileError):
    """
    Raised when a provided file path is invalid or does not exist.
    """
    pass


# -- Configuration and Setup Errors ------------------------------------------ #
class ConfigError(StockSignalError):
    """
    Raised for general configuration or setup related errors.
    """
    pass


class InvalidConfigurationError(ConfigError):
    """
    Raised when the configuration values are invalid or missing.
    """
    pass


# -- Model/Training Related Errors ------------------------------------------- #
class ModelError(StockSignalError):
    """
    General error related to ML model operations.
    """
    pass


class ModelNotTrainedError(ModelError):
    """
    Raised when attempting to use a model that has not been trained.
    """
    pass


class ModelLoadingError(ModelError):
    """
    Raised when the model file cannot be loaded (e.g., corrupted file).
    """
    pass


# -- Signal/Notification Errors ---------------------------------------------- #
class SignalError(StockSignalError):
    """
    General error related to signal generation or processing.
    """
    pass


class SlackNotificationError(SignalError):
    """
    Raised when Slack notification fails (e.g., invalid webhook or connection issue).
    """
    pass


# -- Database Errors --------------------------------------------------------- #
class DatabaseError(StockSignalError):
    """
    General error related to database operations.
    """
    pass


class DatabaseConnectionError(DatabaseError):
    """
    Raised when the database connection fails or is unavailable.
    """
    pass


class DatabaseQueryError(DatabaseError):
    """
    Raised for failures during database queries or transactions.
    """
    pass
