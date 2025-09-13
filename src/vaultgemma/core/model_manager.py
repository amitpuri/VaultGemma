"""Model manager for VaultGemma."""

from typing import Optional, Dict, Any
from .base import BaseProvider
from .exceptions import ModelLoadError, ConfigurationError
from ..config.settings import ModelConfig, AuthConfig
from ..auth.huggingface_auth import HuggingFaceAuthenticator
from ..auth.kaggle_auth import KaggleAuthenticator
from ..providers.huggingface_provider import HuggingFaceProvider
from ..providers.kaggle_provider import KaggleProvider


class ModelManager:
    """Manages model loading and provider selection."""
    
    def __init__(self, auth_config: Optional[AuthConfig] = None):
        """Initialize model manager.
        
        Args:
            auth_config: Authentication configuration.
        """
        self.auth_config = auth_config or AuthConfig()
        self._provider: Optional[BaseProvider] = None
        self._authenticator = None
    
    def get_provider(self, provider_name: Optional[str] = None) -> BaseProvider:
        """Get a model provider.
        
        Args:
            provider_name: Name of the provider ("huggingface" or "kaggle").
                          If None, uses the configured provider.
            
        Returns:
            BaseProvider: Configured provider instance.
            
        Raises:
            ConfigurationError: If provider is not supported.
        """
        provider_name = provider_name or self.auth_config.provider
        
        if provider_name == "huggingface":
            return self._get_huggingface_provider()
        elif provider_name == "kaggle":
            return self._get_kaggle_provider()
        else:
            raise ConfigurationError(f"Unsupported provider: {provider_name}")
    
    def _get_huggingface_provider(self) -> HuggingFaceProvider:
        """Get Hugging Face provider with authentication."""
        if self._provider is None or not isinstance(self._provider, HuggingFaceProvider):
            authenticator = None
            
            if self.auth_config.token:
                authenticator = HuggingFaceAuthenticator(self.auth_config.token)
            elif self.auth_config.provider == "huggingface":
                authenticator = HuggingFaceAuthenticator()
            
            self._provider = HuggingFaceProvider(authenticator)
        
        return self._provider
    
    def _get_kaggle_provider(self) -> KaggleProvider:
        """Get Kaggle provider with authentication."""
        if self._provider is None or not isinstance(self._provider, KaggleProvider):
            authenticator = None
            
            if self.auth_config.username and self.auth_config.api_key:
                authenticator = KaggleAuthenticator(
                    self.auth_config.username, 
                    self.auth_config.api_key
                )
            elif self.auth_config.provider == "kaggle":
                authenticator = KaggleAuthenticator()
            
            self._provider = KaggleProvider(authenticator)
        
        return self._provider
    
    def load_model(
        self, 
        model_name: str, 
        provider_name: Optional[str] = None,
        model_config: Optional[ModelConfig] = None
    ) -> BaseProvider:
        """Load a model using the specified provider.
        
        Args:
            model_name: Name or path of the model to load.
            provider_name: Name of the provider to use.
            model_config: Model configuration.
            
        Returns:
            BaseProvider: Loaded provider instance.
            
        Raises:
            ModelLoadError: If model loading fails.
        """
        try:
            provider = self.get_provider(provider_name)
            provider.load_model(model_name, model_config)
            return provider
        except Exception as e:
            raise ModelLoadError(f"Failed to load model '{model_name}': {e}")
    
    def unload_model(self) -> None:
        """Unload the current model."""
        if self._provider:
            self._provider.unload_model()
            self._provider = None
    
    @property
    def current_provider(self) -> Optional[BaseProvider]:
        """Get the current provider."""
        return self._provider
    
    @property
    def is_model_loaded(self) -> bool:
        """Check if a model is currently loaded."""
        return self._provider is not None and self._provider.is_loaded
