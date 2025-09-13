#!/usr/bin/env python3
"""
Quick start example for VaultGemma with Hugging Face.

This is the simplest way to get started with VaultGemma.
"""

import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from vaultgemma import ModelManager, TextGenerator, ModelConfig, GenerationConfig


def main():
    """Quick start example."""
    print("🚀 VaultGemma Quick Start (Hugging Face)")
    print("=" * 45)
    
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
    manager = ModelManager()
    provider = manager.load_model("google/vaultgemma-1b", model_config=model_config)
    generator = TextGenerator(provider)
    
    # Generate text
    prompt = "The future of AI is"
    response = generator.generate(prompt, generation_config)
    
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")
    
    manager.unload_model()
    return 0


if __name__ == "__main__":
    exit(main())
