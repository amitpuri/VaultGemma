#!/usr/bin/env python3
"""
Starter script for VaultGemma - Quick Start.

This is the simplest way to get started with VaultGemma.
Run with: python run_example.py starter quick_start
"""

import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from vaultgemma import ModelManager, TextGenerator, ModelConfig, GenerationConfig


def main():
    """Quick start example."""
    print("🚀 VaultGemma Quick Start")
    print("=" * 30)
    
    try:
        # Simple configuration
        model_config = ModelConfig(
            model_name="google/vaultgemma-1b",
            use_fast_tokenizer=False,
            device_map="auto"
        )
        
        generation_config = GenerationConfig(
            max_new_tokens=50,
            temperature=0.7
        )
        
        # Initialize and use
        print("🔄 Loading model...")
        manager = ModelManager()
        provider = manager.load_model("google/vaultgemma-1b", model_config=model_config)
        generator = TextGenerator(provider)
        
        # Generate text
        prompt = "The future of AI is"
        print(f"🔄 Generating response for: '{prompt}'")
        response = generator.generate(prompt, generation_config)
        
        print("✅ Generated response:")
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        
        manager.unload_model()
        print("🧹 Model unloaded.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure you have installed the dependencies:")
        print("pip install -r requirements/core.txt")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
