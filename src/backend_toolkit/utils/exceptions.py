class ToolkitError(Exception):
    """Base exception for all toolkit errors."""

class ConfigurationError(ToolkitError):
    pass

class ExternalServiceError(ToolkitError):
    pass

class ValidationError(ToolkitError):
    pass
