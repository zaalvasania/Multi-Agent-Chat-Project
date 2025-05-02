from agno.storage.sqlite import SqliteStorage

from agno_ai_multi_chat_app.src import registry
import time

class ConversationManager:
    def __init__(self, model_list, db_file, table_name, session_id):
        self.models = []
        if not session_id:
            session_id = str(time.time())

        storage=SqliteStorage(table_name=table_name, db_file=db_file)

        for i, model_config in enumerate(model_list):
            model_class = registry.model_class_registry.get(model_config.model_provider)
            if(model_class):
                model_init_kwargs = model_config.model_initialization_args

                tool_list = []
                for tool_name in model_config.tools:
                    curr_tool_kwargs = model_config.tools[tool_name]
                    tool_class = registry.tools_registry.get(tool_name)
                    if(tool_class):
                        tool_list.append(tool_class(**curr_tool_kwargs))

                self.models.append(model_class(model_index = i, storage=storage, session_id=session_id, tool_list=tool_list, **model_init_kwargs))
            else:
                raise Exception("Unsupported model provider found")
        
    def num_models(self):
        return len(self.models)

    def generate_text_for_indexed_model(self, index, user_input):
        if(index < 0 or index >= len(self.models)):
            raise Exception("Out of range of number of models")
        
        if user_input == "":
            user_input = None

        return self.models[index].generate(user_input)