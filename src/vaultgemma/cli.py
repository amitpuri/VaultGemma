"""Command-line interface for VaultGemma."""

import argparse
import sys
from typing import Optional
from . import ModelManager, TextGenerator, ModelConfig, GenerationConfig, AuthConfig


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="VaultGemma - A Python library for running Google's VaultGemma models"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate text from a prompt")
    generate_parser.add_argument("prompt", help="Input text prompt")
    generate_parser.add_argument("--provider", choices=["huggingface", "kaggle"], 
                               default="huggingface", help="Model provider")
    generate_parser.add_argument("--model", default="google/vaultgemma-1b", 
                               help="Model name or path")
    generate_parser.add_argument("--max-tokens", type=int, default=100, 
                               help="Maximum tokens to generate")
    generate_parser.add_argument("--temperature", type=float, default=0.7, 
                               help="Sampling temperature")
    generate_parser.add_argument("--output", help="Output file (optional)")
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Interactive chat mode")
    chat_parser.add_argument("--provider", choices=["huggingface", "kaggle"], 
                           default="huggingface", help="Model provider")
    chat_parser.add_argument("--model", default="google/vaultgemma-1b", 
                           help="Model name or path")
    
    # Auth command
    auth_parser = subparsers.add_parser("auth", help="Set up authentication")
    auth_parser.add_argument("provider", choices=["huggingface", "kaggle"], 
                           help="Provider to authenticate with")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == "generate":
            return generate_text(args)
        elif args.command == "chat":
            return interactive_chat(args)
        elif args.command == "auth":
            return setup_auth(args)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def generate_text(args) -> int:
    """Generate text from command line arguments."""
    print("🚀 VaultGemma Text Generation")
    print("=" * 30)
    
    # Configure authentication
    auth_config = AuthConfig(provider=args.provider)
    
    # Configure model
    model_config = ModelConfig(
        model_name=args.model,
        use_fast_tokenizer=False,
        device_map="auto",
        dtype="auto"
    )
    
    # Configure generation
    generation_config = GenerationConfig(
        max_new_tokens=args.max_tokens,
        temperature=args.temperature,
        do_sample=True,
        top_p=0.9
    )
    
    # Initialize and load model
    print("🔄 Loading model...")
    manager = ModelManager(auth_config)
    provider = manager.load_model(args.model, model_config=model_config)
    generator = TextGenerator(provider)
    
    # Generate text
    print(f"🔄 Generating response for: '{args.prompt}'")
    response = generator.generate(args.prompt, generation_config)
    
    # Output result
    print("✅ Generated response:")
    print("-" * 50)
    print(response)
    print("-" * 50)
    
    # Save to file if requested
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(response)
        print(f"💾 Response saved to: {args.output}")
    
    # Clean up
    manager.unload_model()
    return 0


def interactive_chat(args) -> int:
    """Interactive chat mode."""
    print("🚀 VaultGemma Interactive Chat")
    print("=" * 30)
    print("Type 'quit' or 'exit' to end the chat.")
    print()
    
    # Configure authentication
    auth_config = AuthConfig(provider=args.provider)
    
    # Configure model
    model_config = ModelConfig(
        model_name=args.model,
        use_fast_tokenizer=False,
        device_map="auto",
        dtype="auto"
    )
    
    # Configure generation
    generation_config = GenerationConfig(
        max_new_tokens=150,
        temperature=0.8,
        do_sample=True,
        top_p=0.9,
        repetition_penalty=1.1
    )
    
    # Initialize and load model
    print("🔄 Loading model...")
    manager = ModelManager(auth_config)
    provider = manager.load_model(args.model, model_config=model_config)
    generator = TextGenerator(provider)
    print("✅ Model loaded! Starting chat...")
    print()
    
    # Chat loop
    messages = []
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not user_input:
                continue
            
            # Add user message
            messages.append({"role": "user", "content": user_input})
            
            # Generate response
            print("🤖 VaultGemma: ", end="", flush=True)
            response = generator.chat(messages, generation_config)
            print(response)
            print()
            
            # Add assistant response
            messages.append({"role": "assistant", "content": response})
            
        except KeyboardInterrupt:
            break
    
    # Clean up
    manager.unload_model()
    return 0


def setup_auth(args) -> int:
    """Set up authentication for a provider."""
    print(f"🔧 Setting up {args.provider} authentication")
    print("=" * 40)
    
    if args.provider == "huggingface":
        from .auth.huggingface_auth import HuggingFaceAuthenticator
        
        token = input("Enter your Hugging Face API token: ").strip()
        if not token:
            print("❌ Token is required!")
            return 1
        
        authenticator = HuggingFaceAuthenticator()
        if authenticator.setup_credentials(token):
            print("✅ Hugging Face authentication set up successfully!")
            return 0
        else:
            print("❌ Failed to set up authentication!")
            return 1
    
    elif args.provider == "kaggle":
        from .auth.kaggle_auth import KaggleAuthenticator
        
        username = input("Enter your Kaggle username: ").strip()
        api_key = input("Enter your Kaggle API key: ").strip()
        
        if not username or not api_key:
            print("❌ Username and API key are required!")
            return 1
        
        authenticator = KaggleAuthenticator()
        if authenticator.setup_credentials(username, api_key):
            print("✅ Kaggle authentication set up successfully!")
            return 0
        else:
            print("❌ Failed to set up authentication!")
            return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
