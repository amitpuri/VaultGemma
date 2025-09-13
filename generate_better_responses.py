#!/usr/bin/env python3
"""
Script to generate better, more complete responses for VaultGemma examples in README.md
"""

import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent / "src"))

from vaultgemma import ModelManager, TextGenerator, ModelConfig, GenerationConfig


def generate_response(prompt, max_tokens=400):
    """Generate a response using VaultGemma with better configuration."""
    try:
        print(f"🔄 Generating response for: {prompt[:60]}...")
        
        # Configuration for better, more complete responses
        model_config = ModelConfig(
            model_name="google/vaultgemma-1b",
            use_fast_tokenizer=False,
            device_map="auto"
        )
        
        generation_config = GenerationConfig(
            max_new_tokens=max_tokens,
            temperature=0.8,
            do_sample=True,
            top_p=0.95,
            repetition_penalty=1.1,
            pad_token_id=50256
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
    """Generate better responses for all incomplete examples."""
    
    # Define the prompts that need complete responses with better prompts
    prompts = {
        "quantum_computing": "Explain quantum computing in simple terms that a 10-year-old could understand. Use analogies and examples to make it clear and engaging.",
        "machine_learning": "Describe how machine learning algorithms learn from data, using analogies from everyday life. Give specific examples and explain the process step by step.",
        "carbon_footprint": "A company wants to reduce its carbon footprint by 50% in 5 years. What are 5 innovative strategies they could implement? Provide detailed explanations for each strategy.",
        "smart_city": "Design a smart city transportation system that reduces traffic congestion and pollution. Describe the key components, technologies, and benefits in detail.",
        "ai_ethics": "What are the ethical implications of creating AI that can think and feel like humans? Discuss the key concerns, benefits, and considerations in detail.",
        "consciousness": "How do you define consciousness, and can artificial intelligence ever truly be conscious? Provide a thoughtful analysis of this complex question.",
        "space_exploration": "What is the future of space exploration? Discuss upcoming missions, technologies, and goals for the next decade.",
        "climate_agriculture": "How will climate change affect global agriculture? Explain the impacts on crops, farming practices, and food security worldwide.",
        "sustainable_living": "I'm interested in learning about sustainable living. Can you help me understand what it means and how I can start? Provide practical tips and actionable steps."
    }
    
    print("🚀 VaultGemma Better Response Generator")
    print("=" * 50)
    print("Generating complete, well-formatted responses...")
    print()
    
    responses = {}
    
    for key, prompt in prompts.items():
        print(f"\n📝 Processing: {key}")
        response = generate_response(prompt, max_tokens=500)
        if response:
            # Clean up the response
            cleaned_response = clean_response(response)
            responses[key] = cleaned_response
        print()
    
    # Save responses to a file
    output_file = "better_responses.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Better Generated VaultGemma Responses\n")
        f.write("=" * 50 + "\n\n")
        
        for key, response in responses.items():
            f.write(f"Key: {key}\n")
            f.write(f"Response:\n{response}\n")
            f.write("-" * 50 + "\n\n")
    
    print(f"✅ All responses saved to {output_file}")
    print(f"📊 Generated {len(responses)} complete responses")


def clean_response(response):
    """Clean up the response to remove unwanted formatting and make it more readable."""
    # Remove step numbers and formatting artifacts
    lines = response.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip lines that are just step numbers or formatting
        if any(skip in line.lower() for skip in ['step 1', 'step 2', 'result', '1 of 2', '2 of 2', 'answer:']):
            continue
        # Skip lines that are just mathematical expressions without context
        if line.strip().startswith('$') and len(line.strip()) < 20:
            continue
        # Skip very short lines that are just formatting
        if len(line.strip()) < 3:
            continue
        cleaned_lines.append(line)
    
    # Join lines and clean up
    cleaned = '\n'.join(cleaned_lines).strip()
    
    # Remove the original prompt if it appears at the beginning
    if cleaned.startswith('Explain quantum computing') or cleaned.startswith('Describe how machine learning'):
        # Find where the actual response starts
        lines = cleaned.split('\n')
        for i, line in enumerate(lines):
            if len(line.strip()) > 50 and not line.startswith('Explain') and not line.startswith('Describe'):
                cleaned = '\n'.join(lines[i:])
                break
    
    return cleaned


if __name__ == "__main__":
    main()
