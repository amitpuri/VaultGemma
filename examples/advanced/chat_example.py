#!/usr/bin/env python3
"""
Chat example for VaultGemma.

This example demonstrates how to use the VaultGemma library
for chat-style interactions.
"""

import sys
import os
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from vaultgemma import ModelManager, TextGenerator, ModelConfig, GenerationConfig, AuthConfig


def main():
    """Main example function."""
    print("🚀 VaultGemma Chat Example")
    print("=" * 30)
    
    try:
        # Configure authentication
        auth_config = AuthConfig(provider="huggingface")
        
        # Configure model loading
        model_config = ModelConfig(
            model_name="google/vaultgemma-1b",
            use_fast_tokenizer=False,
            device_map="auto",
            dtype="auto"
        )
        
        # Configure text generation for chat
        generation_config = GenerationConfig(
            max_new_tokens=150,
            temperature=0.8,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.1
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
        
        # Example chat conversation
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant that provides interesting and accurate information."},
            {"role": "user", "content": "What are some fascinating facts about the human brain?"},
        ]
        
        print("🔄 Generating chat response...")
        response = generator.chat(messages, generation_config)
        
        print("✅ Chat response:")
        print("-" * 50)
        print(response)
        print("-" * 50)
        
        # Example batch generation
        print("\n🔄 Batch generation example...")
        prompts = [
            "Explain quantum computing in simple terms.",
            "What is the history of artificial intelligence?",
            "How do neural networks work?"
        ]
        
        responses = generator.batch_generate(prompts, generation_config)
        
        print("✅ Batch responses:")
        for i, (prompt, response) in enumerate(zip(prompts, responses), 1):
            print(f"\n{i}. Prompt: {prompt}")
            print(f"   Response: {response[:100]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    finally:
        # Clean up
        if 'manager' in locals():
            manager.unload_model()
            print("\n🧹 Model unloaded.")
    
    return 0


if __name__ == "__main__":
    exit(main())
