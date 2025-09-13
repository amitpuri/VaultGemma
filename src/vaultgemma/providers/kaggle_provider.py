"""Kaggle model provider."""

from typing import Any, Tuple, Optional
from ..core.base import BaseProvider
from ..core.exceptions import ModelLoadError, GenerationError
from ..config.settings import ModelConfig, GenerationConfig


class KaggleProvider(BaseProvider):
    """Kaggle model provider for VaultGemma."""
    
    def __init__(self, authenticator=None):
        """Initialize Kaggle provider.
        
        Args:
            authenticator: Kaggle authenticator instance.
        """
        super().__init__(authenticator)
        self._model = None
        self._tokenizer = None
        self._model_path = None
    
    def load_model(self, model_name: str, config: Optional[ModelConfig] = None) -> Tuple[Any, Any]:
        """Load model and tokenizer from Kaggle.
        
        Args:
            model_name: Name or path of the model to load (e.g., "google/vaultgemma/transformers/1b").
            config: Model configuration. If None, uses default config.
            
        Returns:
            Tuple of (model, tokenizer).
            
        Raises:
            ModelLoadError: If model loading fails.
        """
        try:
            import kagglehub
            from transformers import AutoTokenizer, AutoModelForCausalLM
            
            if config is None:
                config = ModelConfig(model_name=model_name)
            
            # Authenticate if needed
            if self.authenticator and not self.authenticator.is_authenticated():
                self.authenticator.authenticate()
            
            # Download model from Kaggle
            self._model_path = kagglehub.model_download(model_name)
            
            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(
                self._model_path,
                use_fast=config.use_fast_tokenizer,
                trust_remote_code=config.trust_remote_code,
                cache_dir=config.cache_dir,
                local_files_only=config.local_files_only
            )
            
            # Load model
            model = AutoModelForCausalLM.from_pretrained(
                self._model_path,
                **config.to_dict()
            )
            
            self._model = model
            self._tokenizer = tokenizer
            
            return model, tokenizer
            
        except Exception as e:
            raise ModelLoadError(f"Failed to load Kaggle model '{model_name}': {e}")
    
    def generate_text(
        self, 
        prompt: str, 
        config: Optional[GenerationConfig] = None,
        **kwargs
    ) -> str:
        """Generate text from a prompt.
        
        Args:
            prompt: Input text prompt.
            config: Generation configuration. If None, uses default config.
            **kwargs: Additional generation parameters.
            
        Returns:
            Generated text.
            
        Raises:
            GenerationError: If text generation fails.
        """
        if not self.is_loaded:
            raise GenerationError("Model not loaded. Call load_model() first.")
        
        try:
            if config is None:
                config = GenerationConfig()
            
            # Tokenize input
            input_ids = self._tokenizer(prompt, return_tensors="pt").to(self._model.device)
            
            # Generate text
            generation_kwargs = config.to_dict()
            generation_kwargs.update(kwargs)
            
            outputs = self._model.generate(**input_ids, **generation_kwargs)
            
            # Decode output
            generated_text = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return generated_text
            
        except Exception as e:
            raise GenerationError(f"Text generation failed: {e}")
    
    def generate_streaming(
        self, 
        prompt: str, 
        config: Optional[GenerationConfig] = None,
        **kwargs
    ):
        """Generate text with streaming output.
        
        Args:
            prompt: Input text prompt.
            config: Generation configuration. If None, uses default config.
            **kwargs: Additional generation parameters.
            
        Yields:
            str: Generated text chunks.
            
        Raises:
            GenerationError: If text generation fails.
        """
        if not self.is_loaded:
            raise GenerationError("Model not loaded. Call load_model() first.")
        
        try:
            if config is None:
                config = GenerationConfig()
            
            # Tokenize input
            input_ids = self._tokenizer(prompt, return_tensors="pt").to(self._model.device)
            
            # Generate with streaming
            generation_kwargs = config.to_dict()
            generation_kwargs.update(kwargs)
            
            # Note: This is a simplified streaming implementation
            # For full streaming support, you'd need to implement proper streaming
            outputs = self._model.generate(**input_ids, **generation_kwargs)
            generated_text = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Yield the full text (in a real implementation, this would be chunked)
            yield generated_text
            
        except Exception as e:
            raise GenerationError(f"Streaming text generation failed: {e}")
    
    @property
    def model(self) -> Any:
        """Get the loaded model."""
        return self._model
    
    @property
    def tokenizer(self) -> Any:
        """Get the loaded tokenizer."""
        return self._tokenizer
    
    @property
    def model_path(self) -> Optional[str]:
        """Get the downloaded model path."""
        return self._model_path
