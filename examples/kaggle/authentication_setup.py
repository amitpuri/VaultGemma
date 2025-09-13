#!/usr/bin/env python3
"""
Kaggle authentication setup example.

This example shows how to set up Kaggle authentication for VaultGemma.
"""

import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from vaultgemma import ModelManager, AuthConfig, ModelConfig, GenerationConfig, TextGenerator


def main():
    """Kaggle authentication setup example."""
    print("🚀 VaultGemma Kaggle Authentication Setup")
    print("=" * 45)
    
    try:
        # Set up Kaggle authentication
        # You can get these from https://www.kaggle.com/settings
        auth_config = AuthConfig(
            provider="kaggle",
            username="your_kaggle_username",  # Replace with your username
            api_key="your_kaggle_api_key"     # Replace with your API key
        )
        
        # Configure model
        model_config = ModelConfig(
            model_name="google/vaultgemma/transformers/1b",
            use_fast_tokenizer=False,
            device_map="auto"
        )
        
        generation_config = GenerationConfig(
            max_new_tokens=100,
            temperature=0.7
        )
        
        # Initialize with authentication
        manager = ModelManager(auth_config)
        provider = manager.load_model(
            model_name=model_config.model_name,
            model_config=model_config
        )
        generator = TextGenerator(provider)
        
        # Test generation
        prompt = "Explain machine learning in simple terms."
        response = generator.generate(prompt, generation_config)
        
        print(f"✅ Authentication successful!")
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        
        manager.unload_model()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Setup Instructions:")
        print("1. Go to https://www.kaggle.com/settings")
        print("2. Create a new API token")
        print("3. Update the username and api_key in this script")
        print("4. Run this script again")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
