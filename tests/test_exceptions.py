"""Tests for custom exceptions."""

import unittest
from src.vaultgemma.core.exceptions import (
    VaultGemmaError, AuthenticationError, ModelLoadError, 
    GenerationError, ConfigurationError
)


class TestExceptions(unittest.TestCase):
    """Test custom exception classes."""
    
    def test_vaultgemma_error(self):
        """Test base VaultGemmaError."""
        error = VaultGemmaError("Test error")
        self.assertEqual(str(error), "Test error")
        self.assertIsInstance(error, Exception)
    
    def test_authentication_error(self):
        """Test AuthenticationError."""
        error = AuthenticationError("Auth failed")
        self.assertEqual(str(error), "Auth failed")
        self.assertIsInstance(error, VaultGemmaError)
    
    def test_model_load_error(self):
        """Test ModelLoadError."""
        error = ModelLoadError("Model load failed")
        self.assertEqual(str(error), "Model load failed")
        self.assertIsInstance(error, VaultGemmaError)
    
    def test_generation_error(self):
        """Test GenerationError."""
        error = GenerationError("Generation failed")
        self.assertEqual(str(error), "Generation failed")
        self.assertIsInstance(error, VaultGemmaError)
    
    def test_configuration_error(self):
        """Test ConfigurationError."""
        error = ConfigurationError("Config invalid")
        self.assertEqual(str(error), "Config invalid")
        self.assertIsInstance(error, VaultGemmaError)
    
    def test_exception_inheritance(self):
        """Test exception inheritance chain."""
        auth_error = AuthenticationError("test")
        model_error = ModelLoadError("test")
        gen_error = GenerationError("test")
        config_error = ConfigurationError("test")
        
        # All should inherit from VaultGemmaError
        self.assertIsInstance(auth_error, VaultGemmaError)
        self.assertIsInstance(model_error, VaultGemmaError)
        self.assertIsInstance(gen_error, VaultGemmaError)
        self.assertIsInstance(config_error, VaultGemmaError)
        
        # All should inherit from Exception
        self.assertIsInstance(auth_error, Exception)
        self.assertIsInstance(model_error, Exception)
        self.assertIsInstance(gen_error, Exception)
        self.assertIsInstance(config_error, Exception)


if __name__ == "__main__":
    unittest.main()
