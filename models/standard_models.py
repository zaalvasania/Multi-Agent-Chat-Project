from agno_ai_multi_chat_app.models import BaseModelClass
from agno.models.anthropic.claude import Claude
from agno.utils.pprint import pprint_run_response
from agno.run.response import RunResponse


class AnthropicModel(BaseModelClass):
    def __init__(self, model_index, storage, session_id, tool_list, **model_init_kwargs):
        model = Claude(**model_init_kwargs)
        super().__init__(model_index=model_index, model=model, model_storage=storage, session_id=session_id, tool_list=tool_list)
        self.response_prefix = f"Model {self.model_index + 1} - {model_init_kwargs["id"]}:"
        self.session_id = session_id
    
    def generate(self, user_message):
        print(self.response_prefix)
        if not user_message:
            user_message = "Please continue the conversation"
        self.agent.print_response(
            user_message,
            show_message=False,
            stream=True,
            session_id=self.session_id,
            user_id=f"agent_{self.model_index + 1}",
        )
        print()