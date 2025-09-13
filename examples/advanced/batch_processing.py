#!/usr/bin/env python3
"""
Advanced batch processing example for VaultGemma.

This example demonstrates batch text generation and processing.
"""

import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from vaultgemma import ModelManager, TextGenerator, ModelConfig, GenerationConfig


def main():
    """Batch processing example."""
    print("🚀 VaultGemma Batch Processing Example")
    print("=" * 40)
    
    # Configure model
    model_config = ModelConfig(
        model_name="google/vaultgemma-1b",
        use_fast_tokenizer=False,
        device_map="auto"
    )
    
    generation_config = GenerationConfig(
        max_new_tokens=100,
        temperature=0.7,
        do_sample=True
    )
    
    # Initialize
    manager = ModelManager()
    provider = manager.load_model("google/vaultgemma-1b", model_config=model_config)
    generator = TextGenerator(provider)
    
    # Batch prompts
    prompts = [
        "What is artificial intelligence?",
        "How do neural networks work?",
        "Explain quantum computing.",
        "What is machine learning?",
        "Describe deep learning."
    ]
    
    print(f"🔄 Processing {len(prompts)} prompts in batch...")
    
    # Batch generation
    responses = generator.batch_generate(prompts, generation_config)
    
    # Display results
    print("✅ Batch processing complete!")
    print("=" * 50)
    
    for i, (prompt, response) in enumerate(zip(prompts, responses), 1):
        print(f"\n{i}. Prompt: {prompt}")
        print(f"   Response: {response[:150]}...")
        print("-" * 30)
    
    manager.unload_model()
    return 0


if __name__ == "__main__":
    exit(main())
