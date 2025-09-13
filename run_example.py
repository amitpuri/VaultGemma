#!/usr/bin/env python3
"""
Entry point for running VaultGemma examples.

This script provides a simple way to run different examples
without having to navigate to the examples directory.
"""

import sys
import os
from pathlib import Path


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("🚀 VaultGemma Example Runner")
        print("=" * 30)
        print("\nAvailable examples:")
        print("\n📁 Starter Examples (recommended for beginners):")
        print("  starter hello_world  - Hello World example")
        print("  starter quick_start  - Quick start guide")
        print("\n📁 Hugging Face Examples:")
        print("  hf basic            - Basic usage with Hugging Face")
        print("  hf quick_start      - Quick start with HF")
        print("  huggingface basic   - Basic usage with Hugging Face")
        print("  huggingface quick_start - Quick start with HF")
        print("\n📁 Kaggle Examples:")
        print("  kaggle basic        - Kaggle provider example")
        print("  kaggle auth_setup   - Kaggle authentication setup")
        print("\n📁 Advanced Examples:")
        print("  advanced chat       - Chat-style interaction")
        print("  advanced batch      - Batch processing example")
        print("\nUsage: python run_example.py <category> <example_name>")
        print("\nExamples:")
        print("  python run_example.py starter hello_world")
        print("  python run_example.py hf basic")
        print("  python run_example.py huggingface basic")
        print("  python run_example.py kaggle auth_setup")
        return 1
    
    if len(sys.argv) < 3:
        print("❌ Please specify both category and example name")
        print("Usage: python run_example.py <category> <example_name>")
        return 1
    
    category = sys.argv[1].lower()
    example_name = sys.argv[2].lower()
    
    # Define example structure
    example_structure = {
        "starter": {
            "hello_world": "hello_world.py",
            "quick_start": "quick_start.py"
        },
        "hf": {
            "basic": "basic_usage.py",
            "quick_start": "quick_start.py"
        },
        "huggingface": {
            "basic": "basic_usage.py",
            "quick_start": "quick_start.py"
        },
        "kaggle": {
            "basic": "kaggle_usage.py",
            "auth_setup": "authentication_setup.py"
        },
        "advanced": {
            "chat": "chat_example.py",
            "batch": "batch_processing.py"
        }
    }
    
    if category not in example_structure:
        print(f"❌ Unknown category: {category}")
        print("Available categories:", ", ".join(example_structure.keys()))
        return 1
    
    if example_name not in example_structure[category]:
        print(f"❌ Unknown example: {example_name}")
        print(f"Available examples for {category}:", ", ".join(example_structure[category].keys()))
        return 1
    
    # Determine the correct directory and file
    if category == "starter":
        example_dir = Path(__file__).parent / "starter"
    else:
        # Map category aliases to actual directory names
        category_mapping = {
            "hf": "huggingface",
            "huggingface": "huggingface",
            "kaggle": "kaggle",
            "advanced": "advanced"
        }
        actual_category = category_mapping.get(category, category)
        example_dir = Path(__file__).parent / "examples" / actual_category
    
    example_file = example_dir / example_structure[category][example_name]
    
    if not example_file.exists():
        print(f"❌ Example file not found: {example_file}")
        return 1
    
    print(f"🔄 Running example: {category}/{example_name}")
    print("=" * 40)
    
    # Run the example
    import subprocess
    result = subprocess.run([sys.executable, str(example_file)], cwd=Path(__file__).parent)
    return result.returncode


if __name__ == "__main__":
    exit(main())
