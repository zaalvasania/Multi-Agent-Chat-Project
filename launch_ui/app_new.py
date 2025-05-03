import random
import uuid
import streamlit as st

from agno_ai_multi_chat_app.src.configs import ModelConfig
from agno_ai_multi_chat_app.src.main_multi_agent_chat import ChatCLI
from agno_ai_multi_chat_app.launch_ui.available_models_config import available_models

def generate_n_animal_emojis(sample_count):
    emoji_collections = {
        "animal": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔", "🐧", "🐦", "🦆", "🦉", "🦇", "🐺", "🐗", "🐴", "🦄", "🐝", "🐛", "🦋", "🐌", "🐞", "🐜", "🦟", "🦗", "🕷️", "🦂", "🐢", "🐍", "🦎", "🦖", "🦕"],
    }

    return random.sample(emoji_collections['animal'], sample_count)

def sanity_checks_on_config():
    for idx, config in enumerate(st.session_state.config_items):
        if not len(config['model_api_key']) > 5:
            return idx
        if config["web_search"] and config['web_search_api_key'] == '':
            return idx
    
    return -1

def create_conversation_manager():
    model_config_list = []

    for config in st.session_state.config_items:
        tools = dict()
        if config['web_search']:
            tools["tavily"] = {"api_key": config['web_search_api_key']}
        model_config_list.append(
            ModelConfig(
                model_provider=config['model_provider'],
                model_initialization_args={"id": config['model_id'], "api_key": config["model_api_key"]},
                tools=tools
            )
        )
    st.session_state.chat_cli = ChatCLI(model_list=model_config_list, db_file="/Users/zvasania/Documents/agno_ai_chat_project/tmp/storage.db")
    st.session_state.emojis = generate_n_animal_emojis(st.session_state.chat_cli.num_models)
    st.session_state.messages = []
    st.session_state.empty_message_sent = False
    st.session_state.config_changed_and_valid = False
    st.toast("Successfully updated model configuration and restarted chat")

st.title("Multi-Model Chat App")

if "config_changed_and_valid" not in st.session_state:
    st.session_state.config_changed_and_valid = False

# Initialize session state if not already initialized
if 'config_items' not in st.session_state:
    st.session_state.config_items = []  # List to store all config items

if "messages" not in st.session_state:
    st.session_state.messages = []

if "empty_message_sent" not in st.session_state:
    st.session_state.empty_message_sent = False


def add_config_item():
    st.session_state.config_items.append({
        'model_provider': '',
        'model_id': '',
        'model_api_key': '',
        'web_search': True,
        'web_search_api_key': ''
    })

# Function to delete a config item
def delete_config_item(item_idx):
    st.session_state.config_items.pop(item_idx)

tab1, tab2 = st.sidebar.tabs(["Help", "Model Config"])

with tab1:
    st.markdown("""
    # Model Configuration Dashboard Instructions
    
    Welcome to the **Model Configuration Dashboard**. Here are some instructions on how to set up and start your multi-agent conversation!
    
    ## Getting Started
    1. Navigate to the Model Config tab in the sidebar to configure your AI models
    2. Click the **➕ Add Model Configuration** button to add a new model
    3. Fill in the required fields for each model configuration:
       - Select a **Model Provider**
       - Choose a specific **Model ID** based on the provider
       - Toggle **Enable web search** if you want this model to access the web
       - Enter your **API Key** for the selected provider
       - If web search is enabled, provide your **Tavily API Key**
    
    ## Managing Configurations
    - Each model configuration can be expanded or collapsed
    - Use the **Delete** button to remove unwanted configurations
    - Click **Confirm all model configs** when you're done
    
    ## Conversing
    - Once you have entered and pressed confirm for a valid configuration the prompt input field will pop up on the main window
    - Enter your prompt and press enter to begin a conversation
    - After the inital prompt, you can press skip to let the models just continue talking with each other without your input
    
    ## Important Notes
    - **API keys are stored securely** within the context of a session and never shared
    - Configurations are saved to your session and will persist while the app is running
    - For any issues or questions, please contact zaalvasania@gmail.com
    """)


with tab2:
    st.header("Configure Models")
    
    # Create a container for scrollable content
    config_container = st.container()
    
    # Add new config button
    if st.button("➕ Add Model Configuration"):
        add_config_item()
    
    with st.container():
        for idx, config in enumerate(st.session_state.config_items):            
            # with col1:
            expander_label = f"Model {idx + 1}"
            
            # Create native expander
            with st.expander(expander_label, expanded=True):
                config["model_provider"] = st.selectbox(
                    "Model Provider", 
                    list(available_models.keys()), 
                    index=0,
                    key=f"model_provider_{idx}"
                )
                config["model_id"] = st.selectbox(
                    "Model ID",
                    list(available_models[config["model_provider"]].keys()),
                    index=0,
                    key=f"model_id_{idx}"
                )
                config["web_search"] = st.checkbox("Enable web search", value=True, key=f"web_search_{idx}")
                config["model_api_key"] = st.text_input(f"{config["model_provider"]} API Key", type="password", key=f"model_api_key_{idx}")
                if config["web_search"]:
                    config["web_search_api_key"] = st.text_input(f"Tavily API Key", type="password", key=f"web_search_api_key_{idx}")
                st.markdown(f"Selected Model details {available_models[config["model_provider"]][config["model_id"]]["url"]}")


                if st.button("Delete", help="Delete this configuration", key=f"delete_button_{idx}"):
                    delete_config_item(idx)
                    st.rerun()
        
        confirm = st.button("Confirm all model configs", disabled=(len(st.session_state.config_items) <= 0))
        if confirm:
            invalid_idx = sanity_checks_on_config()
            if invalid_idx == -1:
                st.session_state.config_changed_and_valid = True
                st.rerun()
            else:
                st.toast(f'Configuration invalid at idx {invalid_idx}, please try again...', icon='❌')

if st.session_state.config_changed_and_valid:
    create_conversation_manager()

def generate_response(input_text, i):
    model_response = st.session_state.chat_cli.chat_step(input_text, i)
    return (obj.content for obj in model_response)

def generate_and_render_all_responses(chat_response=None):
    for i in range(st.session_state.chat_cli.num_models):
        with st.chat_message("assistant", avatar=st.session_state.emojis[i]):
            generator = generate_response(chat_response, i)
            st.write(f"**Model {i+1}'s response:**")
            response = st.write_stream(generator)
        st.session_state.chat_cli.conversation_manager.add_message("assistant", response)
        st.session_state.messages.append({"role": "assistant", "content": response, "assistant_idx": i})

def create_main_window():
    # Create a container for messages
    messages_container = st.container()

    # Create a container for input at the bottom
    input_container = st.container()
    with input_container:
        # Create a two-column layout for the chat input and empty button
        col1, col2 = st.columns([0.9, 0.1])

        with col1:
            chat_response = st.chat_input("Enter user prompt or press skip button to continue generating...")

        with col2:
            # Align the button with the chat input
            send_empty = st.button("Skip", help="Send empty message")

    if send_empty:
        st.session_state.empty_message_sent = True
        st.rerun()
    
    with messages_container:
        for message in st.session_state.messages:
            avatar = None
            if 'assistant_idx' in message:
                avatar = st.session_state.emojis[message['assistant_idx']]
            with st.chat_message(message["role"], avatar=avatar):
                if 'assistant_idx' in message:
                    st.write(f"**Model {message['assistant_idx'] + 1}'s response:**")
                st.markdown(message["content"])


        # Handle empty message submission from previous run
        if st.session_state.empty_message_sent:
            generate_and_render_all_responses()
        
            # Reset the flag
            st.session_state.empty_message_sent = False

        if chat_response:
            st.session_state.messages.append({"role": "user", "content": chat_response})
            st.session_state.chat_cli.conversation_manager.add_message("user", chat_response)
            with st.chat_message("user"):
                st.markdown(chat_response)

            generate_and_render_all_responses(chat_response)


if "chat_cli" in st.session_state:
    create_main_window()
else:
    st.warning("Model configuration not yet set!", icon="⚠")