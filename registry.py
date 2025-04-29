from agno_ai_multi_chat_app.models.standard_models import AnthropicModel
from agno.tools.tavily import TavilyTools

model_class_registry = {
    "claude": AnthropicModel
}

tools_registry = {
    "tavily": TavilyTools
}