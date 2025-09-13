#!/usr/bin/env python3
"""
Basic usage example for VaultGemma.

This example demonstrates how to use the VaultGemma library
with the Hugging Face provider.
"""

import sys
import os
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from vaultgemma import ModelManager, TextGenerator, ModelConfig, GenerationConfig, AuthConfig


def main():
    """Main example function."""
    print("🚀 VaultGemma Basic Usage Example")
    print("=" * 40)
    
    try:
        # Configure authentication (optional for public models)
        auth_config = AuthConfig(provider="huggingface")
        
        # Configure model loading
        model_config = ModelConfig(
            model_name="google/vaultgemma-1b",
            use_fast_tokenizer=False,  # Use slow tokenizer to avoid issues
            device_map="auto",
            dtype="auto"
        )
        
        # Configure text generation
        generation_config = GenerationConfig(
            max_new_tokens=100,
            temperature=0.7,
            do_sample=True,
            top_p=0.9
        )
        
        # Initialize model manager
        print("🔄 Initializing model manager...")
        manager = ModelManager(auth_config)
        
        # Load model
        print("🔄 Loading model...")
        provider = manager.load_model(
            model_name=model_config.model_name,
            model_config=model_config
        )
        print("✅ Model loaded successfully!")
        
        # Create text generator
        generator = TextGenerator(provider)
        
        # Generate text
        prompt = "Tell me an interesting fact about biology."
        print(f"🔄 Generating response for: '{prompt}'")
        
        response = generator.generate(prompt, generation_config)
        print("✅ Generated response:")
        print("-" * 50)
        print(response)
        print("-" * 50)
        
        # Show model info
        model_info = generator.get_model_info()
        print(f"\n📊 Model Info: {model_info}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    finally:
        # Clean up
        if 'manager' in locals():
            manager.unload_model()
            print("🧹 Model unloaded.")
    
    return 0


if __name__ == "__main__":
    exit(main())
