"""Text generator for VaultGemma."""

from typing import Optional, Dict, Any, Iterator
from .base import BaseProvider
from .exceptions import GenerationError
from ..config.settings import GenerationConfig


class TextGenerator:
    """High-level text generation interface."""
    
    def __init__(self, provider: BaseProvider):
        """Initialize text generator.
        
        Args:
            provider: Model provider instance.
        """
        self.provider = provider
    
    def generate(
        self, 
        prompt: str, 
        config: Optional[GenerationConfig] = None,
        **kwargs
    ) -> str:
        """Generate text from a prompt.
        
        Args:
            prompt: Input text prompt.
            config: Generation configuration.
            **kwargs: Additional generation parameters.
            
        Returns:
            str: Generated text.
            
        Raises:
            GenerationError: If text generation fails.
        """
        try:
            return self.provider.generate_text(prompt, config, **kwargs)
        except Exception as e:
            raise GenerationError(f"Text generation failed: {e}")
    
    def generate_streaming(
        self, 
        prompt: str, 
        config: Optional[GenerationConfig] = None,
        **kwargs
    ) -> Iterator[str]:
        """Generate text with streaming output.
        
        Args:
            prompt: Input text prompt.
            config: Generation configuration.
            **kwargs: Additional generation parameters.
            
        Yields:
            str: Generated text chunks.
            
        Raises:
            GenerationError: If text generation fails.
        """
        try:
            yield from self.provider.generate_streaming(prompt, config, **kwargs)
        except Exception as e:
            raise GenerationError(f"Streaming text generation failed: {e}")
    
    def chat(
        self, 
        messages: list, 
        config: Optional[GenerationConfig] = None,
        **kwargs
    ) -> str:
        """Generate text in a chat format.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.
            config: Generation configuration.
            **kwargs: Additional generation parameters.
            
        Returns:
            str: Generated response.
            
        Raises:
            GenerationError: If text generation fails.
        """
        try:
            # Convert messages to prompt format
            prompt = self._format_chat_messages(messages)
            return self.generate(prompt, config, **kwargs)
        except Exception as e:
            raise GenerationError(f"Chat generation failed: {e}")
    
    def _format_chat_messages(self, messages: list) -> str:
        """Format chat messages into a prompt.
        
        Args:
            messages: List of message dictionaries.
            
        Returns:
            str: Formatted prompt.
        """
        formatted_messages = []
        
        for message in messages:
            role = message.get('role', 'user')
            content = message.get('content', '')
            
            if role == 'system':
                formatted_messages.append(f"System: {content}")
            elif role == 'user':
                formatted_messages.append(f"User: {content}")
            elif role == 'assistant':
                formatted_messages.append(f"Assistant: {content}")
        
        return "\n".join(formatted_messages) + "\nAssistant:"
    
    def batch_generate(
        self, 
        prompts: list, 
        config: Optional[GenerationConfig] = None,
        **kwargs
    ) -> list:
        """Generate text for multiple prompts.
        
        Args:
            prompts: List of input text prompts.
            config: Generation configuration.
            **kwargs: Additional generation parameters.
            
        Returns:
            list: List of generated texts.
            
        Raises:
            GenerationError: If text generation fails.
        """
        try:
            results = []
            for prompt in prompts:
                result = self.generate(prompt, config, **kwargs)
                results.append(result)
            return results
        except Exception as e:
            raise GenerationError(f"Batch generation failed: {e}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model.
        
        Returns:
            Dict[str, Any]: Model information.
        """
        if not self.provider.is_loaded:
            return {"status": "not_loaded"}
        
        info = {
            "status": "loaded",
            "provider": type(self.provider).__name__,
        }
        
        # Add provider-specific information
        if hasattr(self.provider, 'model_path'):
            info["model_path"] = self.provider.model_path
        
        return info
