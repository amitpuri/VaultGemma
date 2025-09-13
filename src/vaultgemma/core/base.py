"""Base classes and interfaces for VaultGemma components."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple
from .exceptions import AuthenticationError, ModelLoadError


class BaseAuthenticator(ABC):
    """Abstract base class for authentication handlers."""
    
    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate with the service.
        
        Returns:
            bool: True if authentication successful, False otherwise.
            
        Raises:
            AuthenticationError: If authentication fails.
        """
        pass
    
    @abstractmethod
    def is_authenticated(self) -> bool:
        """Check if already authenticated.
        
        Returns:
            bool: True if authenticated, False otherwise.
        """
        pass
    
    @abstractmethod
    def setup_credentials(self, **kwargs) -> bool:
        """Set up authentication credentials.
        
        Args:
            **kwargs: Credential parameters.
            
        Returns:
            bool: True if setup successful, False otherwise.
        """
        pass


class BaseProvider(ABC):
    """Abstract base class for model providers."""
    
    def __init__(self, authenticator: Optional[BaseAuthenticator] = None):
        """Initialize the provider.
        
        Args:
            authenticator: Authentication handler for this provider.
        """
        self.authenticator = authenticator
        self._model = None
        self._tokenizer = None
    
    @abstractmethod
    def load_model(self, model_name: str, **kwargs) -> Tuple[Any, Any]:
        """Load model and tokenizer.
        
        Args:
            model_name: Name or path of the model to load.
            **kwargs: Additional model loading parameters.
            
        Returns:
            Tuple of (model, tokenizer).
            
        Raises:
            ModelLoadError: If model loading fails.
        """
        pass
    
    @abstractmethod
    def generate_text(
        self, 
        prompt: str, 
        max_tokens: int = 100,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Generate text from a prompt.
        
        Args:
            prompt: Input text prompt.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            **kwargs: Additional generation parameters.
            
        Returns:
            Generated text.
        """
        pass
    
    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded.
        
        Returns:
            bool: True if model is loaded, False otherwise.
        """
        return self._model is not None and self._tokenizer is not None
    
    def unload_model(self) -> None:
        """Unload the current model to free memory."""
        self._model = None
        self._tokenizer = None
