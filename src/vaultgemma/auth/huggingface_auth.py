"""Hugging Face authentication handler."""

import os
from pathlib import Path
from typing import Optional
from ..core.base import BaseAuthenticator
from ..core.exceptions import AuthenticationError


class HuggingFaceAuthenticator(BaseAuthenticator):
    """Handles Hugging Face authentication."""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize Hugging Face authenticator.
        
        Args:
            token: Hugging Face API token. If None, will try to load from file.
        """
        self.token = token
        self._token_file = Path.home() / ".cache" / "huggingface" / "token"
    
    def authenticate(self) -> bool:
        """Authenticate with Hugging Face.
        
        Returns:
            bool: True if authentication successful.
            
        Raises:
            AuthenticationError: If authentication fails.
        """
        try:
            from huggingface_hub import HfApi
            
            if not self.token:
                self.token = self._load_token_from_file()
            
            if not self.token:
                raise AuthenticationError("No Hugging Face token available")
            
            # Set environment variable
            os.environ['HF_TOKEN'] = self.token
            
            # Test authentication
            api = HfApi()
            user_info = api.whoami()
            
            return True
            
        except Exception as e:
            raise AuthenticationError(f"Hugging Face authentication failed: {e}")
    
    def is_authenticated(self) -> bool:
        """Check if already authenticated.
        
        Returns:
            bool: True if authenticated, False otherwise.
        """
        try:
            from huggingface_hub import HfApi
            api = HfApi()
            api.whoami()
            return True
        except:
            return False
    
    def setup_credentials(self, token: str) -> bool:
        """Set up Hugging Face credentials.
        
        Args:
            token: Hugging Face API token.
            
        Returns:
            bool: True if setup successful, False otherwise.
        """
        try:
            # Create cache directory
            cache_dir = self._token_file.parent
            cache_dir.mkdir(parents=True, exist_ok=True)
            
            # Save token to file
            with open(self._token_file, 'w') as f:
                f.write(token)
            
            # Set permissions (Windows doesn't support chmod, but we can try)
            try:
                os.chmod(self._token_file, 0o600)
            except:
                pass  # Windows doesn't support chmod
            
            self.token = token
            return True
            
        except Exception as e:
            raise AuthenticationError(f"Failed to setup Hugging Face credentials: {e}")
    
    def _load_token_from_file(self) -> Optional[str]:
        """Load token from file.
        
        Returns:
            Optional[str]: Token if found, None otherwise.
        """
        try:
            if self._token_file.exists():
                with open(self._token_file, 'r') as f:
                    return f.read().strip()
        except Exception:
            pass
        return None
    
    def get_user_info(self) -> dict:
        """Get authenticated user information.
        
        Returns:
            dict: User information.
            
        Raises:
            AuthenticationError: If not authenticated.
        """
        try:
            from huggingface_hub import HfApi
            api = HfApi()
            return api.whoami()
        except Exception as e:
            raise AuthenticationError(f"Failed to get user info: {e}")
