from agno_ai_multi_chat_app.src.models.standard_models import AnthropicModel, DeepSeekModel, OpenAIModel, TogetherModel
from agno.tools.tavily import TavilyTools
from agno.tools.duckduckgo import DuckDuckGoTools

model_class_registry = {
    "Claude": AnthropicModel,
    "OpenAI": OpenAIModel,
    "Together": TogetherModel,
    "DeepSeek": DeepSeekModel
}

tools_registry = {
    "tavily": TavilyTools,
    "DuckDuckGo": DuckDuckGoTools
}