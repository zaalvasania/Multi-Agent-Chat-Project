from agno.agent import Agent

class BaseModelClass:
    def __init__(self, model_index, model, model_storage, session_id, tool_list):
        system_prompt_description = f"You are a part of a conversation with other models where you are referred to as model {model_index + 1}. Respond given the conversation context provided and feel free to refer to other models too when responding. Also only use tools when you feel the need to do so we also want to keep the conversation going so find a good balance."
        self.agent = Agent(
            model=model,
            session_id=session_id,
            storage=model_storage,
            add_history_to_messages=True,
            description = system_prompt_description,
            tools = tool_list,
            show_tool_calls=True
        )
        self.model_index = model_index