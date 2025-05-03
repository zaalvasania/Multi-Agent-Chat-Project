from dataclasses import dataclass

class ModelConfig:
    def __init__(self, model_provider, model_initialization_args=None, tools=dict()):
        self.model_provider = model_provider
        self.model_initialization_args = model_initialization_args if model_initialization_args is not None else dict()
        self.tools = tools