"""Tests for configuration classes."""

import unittest
from src.vaultgemma.config.settings import ModelConfig, GenerationConfig, AuthConfig


class TestModelConfig(unittest.TestCase):
    """Test ModelConfig class."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = ModelConfig()
        
        self.assertEqual(config.model_name, "google/vaultgemma-1b")
        self.assertEqual(config.device_map, "auto")
        self.assertEqual(config.dtype, "auto")
        self.assertFalse(config.use_fast_tokenizer)
        self.assertFalse(config.trust_remote_code)
        self.assertIsNone(config.cache_dir)
        self.assertFalse(config.local_files_only)
    
    def test_custom_values(self):
        """Test custom configuration values."""
        config = ModelConfig(
            model_name="custom/model",
            device_map="cpu",
            dtype="float32",
            use_fast_tokenizer=True,
            trust_remote_code=True,
            cache_dir="/tmp/cache",
            local_files_only=True
        )
        
        self.assertEqual(config.model_name, "custom/model")
        self.assertEqual(config.device_map, "cpu")
        self.assertEqual(config.dtype, "float32")
        self.assertTrue(config.use_fast_tokenizer)
        self.assertTrue(config.trust_remote_code)
        self.assertEqual(config.cache_dir, "/tmp/cache")
        self.assertTrue(config.local_files_only)
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = ModelConfig()
        config_dict = config.to_dict()
        
        expected_keys = {
            "device_map", "dtype", "trust_remote_code", 
            "cache_dir", "local_files_only"
        }
        self.assertEqual(set(config_dict.keys()), expected_keys)
        self.assertEqual(config_dict["device_map"], "auto")
        self.assertEqual(config_dict["dtype"], "auto")


class TestGenerationConfig(unittest.TestCase):
    """Test GenerationConfig class."""
    
    def test_default_values(self):
        """Test default generation values."""
        config = GenerationConfig()
        
        self.assertEqual(config.max_new_tokens, 100)
        self.assertEqual(config.temperature, 0.7)
        self.assertTrue(config.do_sample)
        self.assertEqual(config.top_p, 0.9)
        self.assertEqual(config.top_k, 50)
        self.assertEqual(config.repetition_penalty, 1.1)
        self.assertIsNone(config.pad_token_id)
        self.assertIsNone(config.eos_token_id)
        self.assertEqual(config.num_beams, 1)
        self.assertFalse(config.early_stopping)
    
    def test_custom_values(self):
        """Test custom generation values."""
        config = GenerationConfig(
            max_new_tokens=200,
            temperature=0.5,
            do_sample=False,
            top_p=0.8,
            top_k=40,
            repetition_penalty=1.2,
            pad_token_id=0,
            eos_token_id=1,
            num_beams=4,
            early_stopping=True
        )
        
        self.assertEqual(config.max_new_tokens, 200)
        self.assertEqual(config.temperature, 0.5)
        self.assertFalse(config.do_sample)
        self.assertEqual(config.top_p, 0.8)
        self.assertEqual(config.top_k, 40)
        self.assertEqual(config.repetition_penalty, 1.2)
        self.assertEqual(config.pad_token_id, 0)
        self.assertEqual(config.eos_token_id, 1)
        self.assertEqual(config.num_beams, 4)
        self.assertTrue(config.early_stopping)
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = GenerationConfig()
        config_dict = config.to_dict()
        
        expected_keys = {
            "max_new_tokens", "temperature", "do_sample", "top_p", "top_k",
            "repetition_penalty", "num_beams", "early_stopping"
        }
        self.assertEqual(set(config_dict.keys()), expected_keys)
        self.assertEqual(config_dict["max_new_tokens"], 100)
        self.assertEqual(config_dict["temperature"], 0.7)


class TestAuthConfig(unittest.TestCase):
    """Test AuthConfig class."""
    
    def test_default_values(self):
        """Test default authentication values."""
        config = AuthConfig()
        
        self.assertEqual(config.provider, "huggingface")
        self.assertIsNone(config.token)
        self.assertIsNone(config.username)
        self.assertIsNone(config.api_key)
        self.assertIsNone(config.config_file)
    
    def test_custom_values(self):
        """Test custom authentication values."""
        config = AuthConfig(
            provider="kaggle",
            token="hf_token_123",
            username="kaggle_user",
            api_key="kaggle_key_456",
            config_file="/path/to/config.json"
        )
        
        self.assertEqual(config.provider, "kaggle")
        self.assertEqual(config.token, "hf_token_123")
        self.assertEqual(config.username, "kaggle_user")
        self.assertEqual(config.api_key, "kaggle_key_456")
        self.assertEqual(config.config_file, "/path/to/config.json")
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = AuthConfig(
            provider="huggingface",
            token="test_token"
        )
        config_dict = config.to_dict()
        
        self.assertEqual(config_dict["provider"], "huggingface")
        self.assertEqual(config_dict["token"], "test_token")


if __name__ == "__main__":
    unittest.main()
