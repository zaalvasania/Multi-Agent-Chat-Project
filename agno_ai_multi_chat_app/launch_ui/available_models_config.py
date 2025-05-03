
def generate_metadata(url):
    return {
        "url": url
    }

available_models = {
    "Claude": {
        "claude-3-7-sonnet-20250219": generate_metadata("https://docs.anthropic.com/en/docs/about-claude/models/all-models"),
        "claude-3-5-sonnet-20241022": generate_metadata("https://docs.anthropic.com/en/docs/about-claude/models/all-models"),
        "claude-3-5-haiku-20241022": generate_metadata("https://docs.anthropic.com/en/docs/about-claude/models/all-models"),
        "claude-3-opus-20240229": generate_metadata("https://docs.anthropic.com/en/docs/about-claude/models/all-models"),
        "claude-3-haiku-20240307": generate_metadata("https://docs.anthropic.com/en/docs/about-claude/models/all-models")
    },
    "OpenAI": {
        "chatgpt-4o-latest": generate_metadata("https://platform.openai.com/docs/models/chatgpt-4o-latest"),
        "gpt-4.1-2025-04-14": generate_metadata("https://platform.openai.com/docs/models/gpt-4.1"),
        "gpt-4.1-nano-2025-04-14": generate_metadata("https://platform.openai.com/docs/models/gpt-4.1-nano"),
        "gpt-4o-2024-08-06": generate_metadata("https://platform.openai.com/docs/models/gpt-4o"),
        "gpt-4o-mini-2024-07-18": generate_metadata("https://platform.openai.com/docs/models/gpt-4o-mini"),
        "o4-mini-2025-04-16": generate_metadata("https://platform.openai.com/docs/models/o4-mini"),
        "o3-mini-2025-01-31": generate_metadata("https://platform.openai.com/docs/models/o3-mini")

    },
    "Together": {
        "deepseek-ai/DeepSeek-V3": generate_metadata("https://www.together.ai/models/deepseek-v3"),
        "meta-llama/Llama-4-Scout-17B-16E-Instruct": generate_metadata("https://www.together.ai/models/llama-4-scout"),
        "meta-llama/Llama-3.3-70B-Instruct-Turbo": generate_metadata("https://www.together.ai/models/llama-3-3-70b"),
        "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo": generate_metadata("https://www.together.ai/models/llama-3-1"),
        "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free": generate_metadata("https://www.together.ai/models/llama-3-3-70b-free")
    },
    "DeepSeek": {
        "deepseek-chat": generate_metadata("https://api-docs.deepseek.com/quick_start/pricing"),
        "deepseek-reasoner": generate_metadata("https://api-docs.deepseek.com/quick_start/pricing")
    }
}