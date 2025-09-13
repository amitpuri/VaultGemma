#!/usr/bin/env python3
"""
Hello World example for VaultGemma.

The absolute simplest example to verify VaultGemma is working.
Run with: python run_example.py starter hello_world
"""

import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from vaultgemma import ModelManager, TextGenerator, ModelConfig, GenerationConfig


def main():
    """Hello world example."""
    print("🚀 VaultGemma Hello World")
    print("=" * 25)
    print("This is the simplest example to verify VaultGemma is working correctly.")
    print()
    
    try:
        print("🔄 Setting up configuration...")
        # Minimal configuration
        model_config = ModelConfig(
            model_name="google/vaultgemma-1b",
            use_fast_tokenizer=False,
            device_map="auto"
        )
        
        generation_config = GenerationConfig(
            max_new_tokens=20,
            temperature=0.7
        )
        print("✅ Configuration ready")
        
        print("🔄 Initializing model manager...")
        manager = ModelManager()
        print("✅ Model manager initialized")
        
        print("🔄 Loading VaultGemma model (this may take a moment)...")
        provider = manager.load_model("google/vaultgemma-1b", model_config=model_config)
        print("✅ Model loaded successfully!")
        
        print("🔄 Creating text generator...")
        generator = TextGenerator(provider)
        print("✅ Text generator ready")
        
        print("🔄 Generating response...")
        print("   Prompt: 'Hello'")
        response = generator.generate("Hello", generation_config)
        
        print("✅ Generation complete!")
        print()
        print("🎉 VaultGemma says:")
        print(f"   {response}")
        print()
        print("🧹 Cleaning up...")
        manager.unload_model()
        print("✅ Model unloaded successfully")
        print()
        print("🎊 Hello World example completed successfully!")
        print("   VaultGemma is working correctly! 🚀")
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print()
        print("💡 Troubleshooting tips:")
        print("   1. Make sure you have installed the dependencies:")
        print("      pip install -r requirements/core.txt")
        print("   2. Install the VaultGemma-specific transformers:")
        print("      pip install git+https://github.com/huggingface/transformers@v4.56.1-Vault-Gemma-preview")
        print("   3. Check your internet connection for model download")
        print("   4. Try running: python run_example.py starter quick_start")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
