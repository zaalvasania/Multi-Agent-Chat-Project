import streamlit as st
from pathlib import Path
import json
import os

# Simple path for storing API keys locally during development
CONFIG_DIR = Path.home() / ".chat_orchestrator"
CONFIG_DIR.mkdir(exist_ok=True)
API_KEYS_FILE = CONFIG_DIR / "api_keys.json"

def save_api_keys(keys):
    with open(API_KEYS_FILE, "w") as f:
        json.dump(keys, f)

def load_api_keys():
    if API_KEYS_FILE.exists():
        with open(API_KEYS_FILE, "r") as f:
            return json.load(f)
    return {
        "ANTHROPIC_API_KEY": "",
        "TAVILY_API_KEY": ""
    }

def main():
    st.title("AI Chat Orchestrator")
    
    # Create tabs for different pages
    tab1, tab2, tab3 = st.tabs(["Chat", "API Keys", "Help"])
    
    with tab1:
        # Model configuration 
        st.header("Configure Models")
        
        # Get number of models
        num_models = st.number_input("Number of models", min_value=1, max_value=5, value=2)
        
        # Create configuration for each model
        models_config = []
        for i in range(num_models):
            st.subheader(f"Model {i+1}")
            
            model_type = st.selectbox(
                f"Type", 
                ["gpt-4", "claude-3-opus", "gemini-pro", "llama-3"],
                key=f"model_type_{i}"
            )
            
            # Add more parameters as needed
            
            models_config.append({
                "model_type": model_type
            })
        # Chat interface
        st.header("Chat")
        
        # Initialize state
        if "conversation_container" not in st.session_state:
            st.session_state.conversation_container = st.container()
            st.session_state.first_prompt = True
        
        # Create placeholder for conversation output
        conversation_output = st.session_state.conversation_container
        
        # Input area
        prompt_label = "Enter initial prompt:" if st.session_state.first_prompt else "Enter prompt (optional):"
        user_input = st.text_input(prompt_label, key="user_input")
        
        # Action buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            send_button = st.button("Send" if st.session_state.first_prompt else "Send Input")
        
        with col2:
            # Only show skip button after first prompt
            skip_button = False if st.session_state.first_prompt else st.button("Skip")
        
        # Process user actions
        if send_button and user_input:
            # Display user message
            with conversation_output:
                st.write(f"**You:** {user_input}")
            
            # Setup API keys
            api_keys = load_api_keys()
            for key, value in api_keys.items():
                if value:
                    os.environ[key] = value
            
            # Call orchestrator and get responses
            run_response = orchestrator.run_conversation(user_input)
            
            # Display response
            with conversation_output:
                display_response_in_streamlit(run_response)
            
            # No longer first prompt
            st.session_state.first_prompt = False
            
        elif skip_button:
            # Setup API keys
            api_keys = load_api_keys()
            for key, value in api_keys.items():
                if value:
                    os.environ[key] = value
            
            # Create orchestrator
            orchestrator = ChatOrchestrator(models_config)
            
            # Call orchestrator with None
            run_response = orchestrator.run_conversation(None)
            
            # Display response
            with conversation_output:
                display_response_in_streamlit(run_response, markdown=markdown)
    
    with tab2:
        # API key configuration
        st.header("API Keys")
        
        # Load existing keys
        keys = load_api_keys()
        
        # Create input fields
        new_keys = {}
        new_keys["OPENAI_API_KEY"] = st.text_input(
            "OpenAI API Key", 
            value=keys.get("OPENAI_API_KEY", ""),
            type="password"
        )
        
        new_keys["ANTHROPIC_API_KEY"] = st.text_input(
            "Anthropic API Key", 
            value=keys.get("ANTHROPIC_API_KEY", ""),
            type="password"
        )
        
        new_keys["GOOGLE_API_KEY"] = st.text_input(
            "Google API Key", 
            value=keys.get("GOOGLE_API_KEY", ""),
            type="password"
        )
        
        new_keys["HUGGINGFACE_API_KEY"] = st.text_input(
            "HuggingFace API Key", 
            value=keys.get("HUGGINGFACE_API_KEY", ""),
            type="password"
        )
        
        # Save button
        if st.button("Save API Keys"):
            save_api_keys(new_keys)
            st.success("API keys saved!")
    
    with tab3:
        # Help/documentation
        st.header("Help")
        st.markdown("""
        ## How to use the Chat Orchestrator
        
        1. Configure your API keys in the "API Keys" tab
        2. Set up the models you want to use in the "Chat" tab
        3. Enter your initial prompt to start the conversation
        4. Either:
           - Click "Skip" to let models continue conversing without your input
           - Type a message and click "Send" to add your input to the conversation
        
        ## About
        This tool allows multiple AI models to converse with each other.
        """)

def display_response_in_streamlit(run_response, markdown=True):
    """
    Simplified display function that only handles string content.
    """
    # Handle single response case
    if not hasattr(run_response, '__iter__') or isinstance(run_response, str):
        # Handle a single response (non-iterable)
        st.markdown("---")  # Separator
        
        # Create styled container for the response
        response_container = st.container()
        with response_container:
            if markdown:
                st.markdown(run_response)
            else:
                st.text(run_response)
    
    # Handle streaming response case
    else:
        # Create placeholder for streaming content
        response_container = st.empty()
        streaming_response_content = ""
        
        # Process each response chunk
        for resp in run_response:
            # Append the new content
            streaming_response_content += resp
            
            # Update the display with the accumulated content
            if markdown:
                response_container.markdown(streaming_response_content)
            else:
                response_container.text(streaming_response_content)

if __name__ == "__main__":
    main()