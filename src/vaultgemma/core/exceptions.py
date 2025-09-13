"""Custom exceptions for VaultGemma."""


class VaultGemmaError(Exception):
    """Base exception for all VaultGemma errors."""
    pass


class AuthenticationError(VaultGemmaError):
    """Raised when authentication fails."""
    pass


class ModelLoadError(VaultGemmaError):
    """Raised when model loading fails."""
    pass


class GenerationError(VaultGemmaError):
    """Raised when text generation fails."""
    pass


class ConfigurationError(VaultGemmaError):
    """Raised when configuration is invalid."""
    pass
