from agno_ai_multi_chat_app.src.conversation import ConversationManager

class ChatCLI:
    """Command-line interface for chatting with a model"""
    
    def __init__(self, model_list, db_file, table_name = "memory", session_id=None):
        """Initialize the CLI chat interface
        
        Args:
            model_path: Path to the model or model name on HuggingFace
            conversation_file: Optional path to save/load conversation history
        """
        self.conversation_manager = ConversationManager(model_list, db_file, table_name, session_id)
        self.num_models = self.conversation_manager.num_models()
        conversation_starter = f"This is the beginning of a conversation between {self.num_models} different chatbot(s) and a single human. \
            Each chatbot will speak in the same order each time around and will be referred to by the order in  which they speak (i.e. the first model to \
            speak will be referred to as model 1, the second as model 2, etc). Each chatbot should engage in conversation and not hesitate to express their own \
            point of view in response to other models but should only respond one at a time. The topic of conversation will be prompted at the beginning by the user and the user may periodically input their \
            own thoughts from time to time. \n\n"
        self.conversation_manager.add_message("user", conversation_starter)
    
    def chat_step(self, user_input, model_idx):
        """Query and retrieve stream output for model with index model_idx given user input
        
        Args:
            user_input: User input (optionally empty string if Skip button is pressed)
            model_idx: Index of model to query
        """
        overall_user_input = user_input
        output = self.conversation_manager.generate_text_for_indexed_model(model_idx, overall_user_input)
        return output