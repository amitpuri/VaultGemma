"""
VaultGemma - A Python library for running Google's VaultGemma models.

This package provides a clean, object-oriented interface for working with
VaultGemma models from different providers (Hugging Face, Kaggle).
"""

from .core.model_manager import ModelManager
from .core.text_generator import TextGenerator
from .providers.huggingface_provider import HuggingFaceProvider
from .providers.kaggle_provider import KaggleProvider
from .config.settings import ModelConfig, GenerationConfig, AuthConfig

__version__ = "1.0.0"
__author__ = "VaultGemma Team"

__all__ = [
    "ModelManager",
    "TextGenerator", 
    "HuggingFaceProvider",
    "KaggleProvider",
    "ModelConfig",
    "GenerationConfig",
    "AuthConfig",
]
