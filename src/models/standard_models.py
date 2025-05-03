from agno_ai_multi_chat_app.src.models import BaseModelClass
from agno.models.anthropic.claude import Claude
from agno.models.openai import OpenAIChat
from agno.models.openai.like import OpenAILike
from agno.models.deepseek import DeepSeek

class AnthropicModel(BaseModelClass):
    def __init__(self, model_index, storage, session_id, tool_list, **model_init_kwargs):
        model = Claude(**model_init_kwargs)
        super().__init__(model_index=model_index, model=model, model_storage=storage, session_id=session_id, tool_list=tool_list)
        self.response_prefix = f"Model {self.model_index + 1} - {model_init_kwargs["id"]}:"
        self.session_id = session_id

class OpenAIModel(BaseModelClass):
    def __init__(self, model_index, storage, session_id, tool_list, **model_init_kwargs):
        model = OpenAIChat(**model_init_kwargs)
        super().__init__(model_index=model_index, model=model, model_storage=storage, session_id=session_id, tool_list=tool_list)
        self.response_prefix = f"Model {self.model_index + 1} - {model_init_kwargs["id"]}:"
        self.session_id = session_id

class TogetherModel(BaseModelClass):
    def __init__(self, model_index, storage, session_id, tool_list, **model_init_kwargs):
        model = OpenAILike(**model_init_kwargs, base_url="https://api.together.xyz/v1")
        super().__init__(model_index=model_index, model=model, model_storage=storage, session_id=session_id, tool_list=tool_list)
        self.response_prefix = f"Model {self.model_index + 1} - {model_init_kwargs["id"]}:"
        self.session_id = session_id

class DeepSeekModel(BaseModelClass):
    def __init__(self, model_index, storage, session_id, tool_list, **model_init_kwargs):
        model = DeepSeek(**model_init_kwargs)
        super().__init__(model_index=model_index, model=model, model_storage=storage, session_id=session_id, tool_list=tool_list)
        self.response_prefix = f"Model {self.model_index + 1} - {model_init_kwargs["id"]}:"
        self.session_id = session_id