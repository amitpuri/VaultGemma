"""Configuration classes for VaultGemma."""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class ModelConfig:
    """Configuration for model loading."""
    
    model_name: str = "google/vaultgemma-1b"
    device_map: str = "auto"
    dtype: str = "auto"
    use_fast_tokenizer: bool = False
    trust_remote_code: bool = False
    cache_dir: Optional[str] = None
    local_files_only: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for model loading."""
        return {
            "device_map": self.device_map,
            "dtype": self.dtype,
            "trust_remote_code": self.trust_remote_code,
            "cache_dir": self.cache_dir,
            "local_files_only": self.local_files_only,
        }


@dataclass
class GenerationConfig:
    """Configuration for text generation."""
    
    max_new_tokens: int = 100
    temperature: float = 0.7
    do_sample: bool = True
    top_p: float = 0.9
    top_k: int = 50
    repetition_penalty: float = 1.1
    pad_token_id: Optional[int] = None
    eos_token_id: Optional[int] = None
    num_beams: int = 1
    early_stopping: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for generation."""
        config = {
            "max_new_tokens": self.max_new_tokens,
            "temperature": self.temperature,
            "do_sample": self.do_sample,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "repetition_penalty": self.repetition_penalty,
            "num_beams": self.num_beams,
            "early_stopping": self.early_stopping,
        }
        
        # Only include optional parameters if they're set
        if self.pad_token_id is not None:
            config["pad_token_id"] = self.pad_token_id
        if self.eos_token_id is not None:
            config["eos_token_id"] = self.eos_token_id
            
        return config


@dataclass
class AuthConfig:
    """Configuration for authentication."""
    
    provider: str = "huggingface"  # "huggingface" or "kaggle"
    token: Optional[str] = None
    username: Optional[str] = None
    api_key: Optional[str] = None
    config_file: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for authentication."""
        config = {"provider": self.provider}
        
        if self.token:
            config["token"] = self.token
        if self.username:
            config["username"] = self.username
        if self.api_key:
            config["api_key"] = self.api_key
        if self.config_file:
            config["config_file"] = self.config_file
            
        return config
