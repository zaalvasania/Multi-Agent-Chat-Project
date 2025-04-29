import argparse
from rich.pretty import pprint

from agno_ai_multi_chat_app.configs import ModelConfig
from agno_ai_multi_chat_app.conversation import ConversationManager
from agno.utils.pprint import pprint_run_response

class ChatCLI:
    """Command-line interface for chatting with a model"""
    
    def __init__(self, model_list, db_file, table_name = "memory", session_id = None):
        """Initialize the CLI chat interface
        
        Args:
            model_path: Path to the model or model name on HuggingFace
            conversation_file: Optional path to save/load conversation history
        """
        # Load the model with vLLM
        self.conversation_manager = ConversationManager(model_list, db_file, table_name, session_id)
    
    def chat_loop(self):
        """Main chat loop"""
        print("\n=== Chat started (type 'skip' or 'exit'/Ctrl+C to end) ===")

        start_text = f"This is the beginning of a conversation between {self.conversation_manager.num_models()} different chatbot(s) and a single human. \
            Each chatbot will speak in the same order each time around and will be referred to by the order in  which they speak (i.e. the first model to \
            speak will be referred to as model 1, the second as model 2, etc). Each chatbot should engage in conversation and not hesitate to express their own \
            point of view in response to other models. The topic of conversation will be prompted at the beginning by the user and the user may periodically input their \
            own thoughts from time to time.\n\n"
        
        try:
            while True:
                # Get user input
                user_input = input("\nYou: ").strip()
                print("="*60)
                
                # Handle special commands
                if user_input.lower() in ['exit']:
                    break
                
                overall_user_input = start_text
                # Add user message to conversation
                if user_input.lower() != "skip":
                    overall_user_input += user_input                    

                for i in range(self.conversation_manager.num_models()):
                    self.conversation_manager.generate_text_for_indexed_model(i, overall_user_input)
                
                start_text = ""
        
        except KeyboardInterrupt:
            print("\nChat ended by user.")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Storage db path')
    parser.add_argument('--storage_db_path', type=str, required=True, 
                        help='Path storage db is located')
    args = parser.parse_args()
    storage_db_path = args.storage_db_path
    
    # Initialize CLI chat interface
    model_config_list = [
        ModelConfig(
            model_provider="claude",
            model_initialization_args={"id": "claude-3-5-sonnet-20241022"},
            tools={"tavily": {"instructions": "Use this tool only once total", "add_instructions": True}}
        ),
        ModelConfig(
            model_provider="claude",
            model_initialization_args={"id": "claude-3-5-sonnet-20241022"},
            tools={"tavily": {"instructions": "Use this tool only once total", "add_instructions": True}}
        )
    ]
    chat_cli = ChatCLI(model_list=model_config_list, db_file=storage_db_path)
    
    # Start chat loop
    chat_cli.chat_loop()

if __name__ == '__main__':
    main()