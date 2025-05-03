from agno.agent import Agent

class BaseModelClass:
    def __init__(self, model_index, model, model_storage, session_id, tool_list):
        system_prompt_description = f"You are a part of a conversation with other models where you are only to be referred to \
            as model {model_index + 1}. Respond given the conversation context provided and feel free to refer to \
            other models too when responding. Also only use tools when you feel the need to do so we also want \
            to keep the conversation going so find a good balance. If you do use a tool though reference how \
            you used its output in your response and do so specifically so that we know you used the tool's output. Respond only as yourself \
            and give one response at a time to keep the conversation going."
        self.agent = Agent(
            model=model,
            session_id=session_id,
            storage=model_storage,
            add_history_to_messages=True,
            system_message = system_prompt_description,
            tools = tool_list,
        )
        self.model_index = model_index
    
    def generate(self, user_message, conversation_history):
        if not user_message:
            user_message = "Please continue the conversation"
        return self.agent.run(
            user_message,
            messages=conversation_history,
            session_id=self.session_id,
            user_id=f"agent_{self.model_index + 1}",
            stream=True
        )