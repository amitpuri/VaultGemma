#!/usr/bin/env python3
"""
Script to generate complete responses for incomplete VaultGemma examples in README.md
"""

import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent / "src"))

from vaultgemma import ModelManager, TextGenerator, ModelConfig, GenerationConfig


def generate_response(prompt, max_tokens=200):
    """Generate a response using VaultGemma."""
    try:
        print(f"🔄 Generating response for: {prompt[:50]}...")
        
        # Configuration for better responses
        model_config = ModelConfig(
            model_name="google/vaultgemma-1b",
            use_fast_tokenizer=False,
            device_map="auto"
        )
        
        generation_config = GenerationConfig(
            max_new_tokens=max_tokens,
            temperature=0.7,
            do_sample=True,
            top_p=0.9
        )
        
        # Initialize and load model
        manager = ModelManager()
        provider = manager.load_model("google/vaultgemma-1b", model_config=model_config)
        generator = TextGenerator(provider)
        
        # Generate response
        response = generator.generate(prompt, generation_config)
        
        # Clean up
        manager.unload_model()
        
        print("✅ Response generated successfully")
        return response
        
    except Exception as e:
        print(f"❌ Error generating response: {e}")
        return None


def main():
    """Generate responses for all incomplete examples."""
    
    # Define the prompts that need complete responses
    prompts = {
        "quantum_computing": "Explain quantum computing in simple terms that a 10-year-old could understand.",
        "machine_learning": "Describe how machine learning algorithms learn from data, using analogies from everyday life.",
        "carbon_footprint": "A company wants to reduce its carbon footprint by 50% in 5 years. What are 5 innovative strategies they could implement?",
        "smart_city": "Design a smart city transportation system that reduces traffic congestion and pollution.",
        "ai_ethics": "What are the ethical implications of creating AI that can think and feel like humans?",
        "consciousness": "How do you define consciousness, and can artificial intelligence ever truly be conscious?",
        "space_exploration": "What is the future of space exploration?",
        "climate_agriculture": "How will climate change affect global agriculture?",
        "sustainable_living": "I'm interested in learning about sustainable living. Can you help me understand what it means and how I can start?"
    }
    
    print("🚀 VaultGemma Response Generator")
    print("=" * 40)
    print("Generating complete responses for incomplete examples...")
    print()
    
    responses = {}
    
    for key, prompt in prompts.items():
        print(f"\n📝 Processing: {key}")
        response = generate_response(prompt, max_tokens=300)
        if response:
            responses[key] = response
        print()
    
    # Save responses to a file
    output_file = "generated_responses.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Generated VaultGemma Responses\n")
        f.write("=" * 40 + "\n\n")
        
        for key, response in responses.items():
            f.write(f"Key: {key}\n")
            f.write(f"Response:\n{response}\n")
            f.write("-" * 40 + "\n\n")
    
    print(f"✅ All responses saved to {output_file}")
    print(f"📊 Generated {len(responses)} complete responses")


if __name__ == "__main__":
    main()
