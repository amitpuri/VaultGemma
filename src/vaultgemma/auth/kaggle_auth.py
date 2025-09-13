"""Kaggle authentication handler."""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from ..core.base import BaseAuthenticator
from ..core.exceptions import AuthenticationError


class KaggleAuthenticator(BaseAuthenticator):
    """Handles Kaggle authentication."""
    
    def __init__(self, username: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize Kaggle authenticator.
        
        Args:
            username: Kaggle username. If None, will try to load from config file.
            api_key: Kaggle API key. If None, will try to load from config file.
        """
        self.username = username
        self.api_key = api_key
        self._config_file = Path.home() / ".kaggle" / "kaggle.json"
    
    def authenticate(self) -> bool:
        """Authenticate with Kaggle.
        
        Returns:
            bool: True if authentication successful.
            
        Raises:
            AuthenticationError: If authentication fails.
        """
        try:
            import kaggle
            from kaggle.api.kaggle_api_extended import KaggleApi
            
            if not self.username or not self.api_key:
                self._load_credentials_from_file()
            
            if not self.username or not self.api_key:
                raise AuthenticationError("No Kaggle credentials available")
            
            # Set environment variables
            os.environ['KAGGLE_USERNAME'] = self.username
            os.environ['KAGGLE_KEY'] = self.api_key
            
            # Test authentication
            api = KaggleApi()
            api.authenticate()
            
            return True
            
        except Exception as e:
            raise AuthenticationError(f"Kaggle authentication failed: {e}")
    
    def is_authenticated(self) -> bool:
        """Check if already authenticated.
        
        Returns:
            bool: True if authenticated, False otherwise.
        """
        try:
            import kaggle
            from kaggle.api.kaggle_api_extended import KaggleApi
            api = KaggleApi()
            api.authenticate()
            return True
        except:
            return False
    
    def setup_credentials(self, username: str, api_key: str) -> bool:
        """Set up Kaggle credentials.
        
        Args:
            username: Kaggle username.
            api_key: Kaggle API key.
            
        Returns:
            bool: True if setup successful, False otherwise.
        """
        try:
            # Create .kaggle directory
            kaggle_dir = self._config_file.parent
            kaggle_dir.mkdir(exist_ok=True)
            
            # Create kaggle.json
            kaggle_config = {
                "username": username,
                "key": api_key
            }
            
            with open(self._config_file, 'w') as f:
                json.dump(kaggle_config, f)
            
            # Set permissions (Windows doesn't support chmod, but we can try)
            try:
                os.chmod(self._config_file, 0o600)
            except:
                pass  # Windows doesn't support chmod
            
            self.username = username
            self.api_key = api_key
            
            return True
            
        except Exception as e:
            raise AuthenticationError(f"Failed to setup Kaggle credentials: {e}")
    
    def _load_credentials_from_file(self) -> None:
        """Load credentials from kaggle.json file."""
        try:
            if self._config_file.exists():
                with open(self._config_file, 'r') as f:
                    config = json.load(f)
                    self.username = config.get("username")
                    self.api_key = config.get("key")
        except Exception:
            pass
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get authenticated user information.
        
        Returns:
            Dict[str, Any]: User information.
            
        Raises:
            AuthenticationError: If not authenticated.
        """
        try:
            import kaggle
            from kaggle.api.kaggle_api_extended import KaggleApi
            api = KaggleApi()
            api.authenticate()
            # Note: Kaggle API doesn't have a direct whoami method
            # This is a placeholder for future implementation
            return {"username": self.username}
        except Exception as e:
            raise AuthenticationError(f"Failed to get user info: {e}")
