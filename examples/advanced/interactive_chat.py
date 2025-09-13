#!/usr/bin/env python3
"""
Interactive Chat Example for VaultGemma.

This example demonstrates a real-time interactive chat session with the VaultGemma model.
Users can have continuous conversations with the model, with conversation history
and special commands for session management.
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Any

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from vaultgemma import ModelManager, TextGenerator, ModelConfig, GenerationConfig, AuthConfig


class InteractiveChat:
    """Interactive chat session manager."""
    
    def __init__(self):
        """Initialize the interactive chat session."""
        self.manager = None
        self.generator = None
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = "You are a helpful, knowledgeable, and friendly AI assistant. Provide clear, accurate, and engaging responses to user questions."
        
    def setup_model(self) -> bool:
        """Initialize and load the model."""
        try:
            print("🔄 Initializing VaultGemma Interactive Chat...")
            print("=" * 50)
            
            # Configure authentication
            auth_config = AuthConfig(provider="huggingface")
            
            # Configure model loading
            model_config = ModelConfig(
                model_name="google/vaultgemma-1b",
                use_fast_tokenizer=False,
                device_map="auto",
                dtype="auto"
            )
            
            # Configure text generation for interactive chat
            self.generation_config = GenerationConfig(
                max_new_tokens=200,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=2  # Ensure proper padding
            )
            
            # Initialize model manager
            print("🔄 Loading model...")
            self.manager = ModelManager(auth_config)
            
            # Load model
            provider = self.manager.load_model(
                model_name=model_config.model_name,
                model_config=model_config
            )
            print("✅ Model loaded successfully!")
            
            # Create text generator
            self.generator = TextGenerator(provider)
            
            # Initialize conversation with system prompt
            self.conversation_history = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            return True
            
        except Exception as e:
            print(f"❌ Error setting up model: {e}")
            return False
    
    def show_help(self):
        """Display help information."""
        help_text = """
🤖 VaultGemma Interactive Chat Commands:
========================================

/help     - Show this help message
/clear    - Clear conversation history
/exit     - Exit the chat session
/quit     - Exit the chat session (alias)
/reset    - Reset conversation with new system prompt
/status   - Show conversation status

Just type your message to chat with the AI!
        """
        print(help_text)
    
    def clear_conversation(self):
        """Clear the conversation history."""
        self.conversation_history = [
            {"role": "system", "content": self.system_prompt}
        ]
        print("🧹 Conversation history cleared!")
    
    def show_status(self):
        """Show conversation status."""
        user_messages = len([msg for msg in self.conversation_history if msg["role"] == "user"])
        assistant_messages = len([msg for msg in self.conversation_history if msg["role"] == "assistant"])
        
        print(f"📊 Conversation Status:")
        print(f"   User messages: {user_messages}")
        print(f"   Assistant messages: {assistant_messages}")
        print(f"   Total messages: {len(self.conversation_history) - 1}")  # -1 for system prompt
    
    def reset_conversation(self):
        """Reset conversation with new system prompt."""
        new_prompt = input("Enter new system prompt (or press Enter for default): ").strip()
        if new_prompt:
            self.system_prompt = new_prompt
        self.clear_conversation()
        print("🔄 Conversation reset with new system prompt!")
    
    def process_command(self, user_input: str) -> bool:
        """Process special commands. Returns True if command was processed."""
        command = user_input.lower().strip()
        
        if command in ["/help", "/h"]:
            self.show_help()
            return True
        elif command in ["/clear", "/c"]:
            self.clear_conversation()
            return True
        elif command in ["/exit", "/quit", "/q"]:
            return False  # Signal to exit
        elif command in ["/reset", "/r"]:
            self.reset_conversation()
            return True
        elif command in ["/status", "/s"]:
            self.show_status()
            return True
        
        return False  # Not a command
    
    def generate_response(self, user_message: str) -> str:
        """Generate AI response to user message."""
        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            
            # Generate response
            print("🤔 Thinking...")
            response = self.generator.chat(self.conversation_history, self.generation_config)
            
            # Add assistant response to conversation history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            error_msg = f"❌ Error generating response: {e}"
            print(error_msg)
            return error_msg
    
    def run(self):
        """Run the interactive chat session."""
        if not self.setup_model():
            return 1
        
        print("\n🎉 Welcome to VaultGemma Interactive Chat!")
        print("Type '/help' for commands or start chatting!")
        print("=" * 50)
        
        try:
            while True:
                # Get user input
                try:
                    user_input = input("\n👤 You: ").strip()
                except KeyboardInterrupt:
                    print("\n\n👋 Goodbye!")
                    break
                except EOFError:
                    print("\n\n👋 Goodbye!")
                    break
                
                # Handle empty input
                if not user_input:
                    continue
                
                # Process commands
                if user_input.startswith("/"):
                    if not self.process_command(user_input):
                        break  # Exit command
                    continue
                
                # Generate and display response
                response = self.generate_response(user_input)
                print(f"\n🤖 Assistant: {response}")
                
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            return 1
        
        finally:
            # Clean up
            if self.manager:
                print("\n🧹 Cleaning up...")
                self.manager.unload_model()
                print("✅ Model unloaded. Goodbye!")
        
        return 0


def main():
    """Main function to run the interactive chat."""
    chat = InteractiveChat()
    return chat.run()


if __name__ == "__main__":
    exit(main())
