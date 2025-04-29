from agno.agent import Agent
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.memory import Memory
from agno.models.anthropic.claude import Claude
from rich.pretty import pprint
from agno.utils.pprint import pprint_run_response
from agno.tools.tavily import TavilyTools


# memory = Memory()

storage=SqliteStorage(table_name="memory", db_file="tmp/storage_example.db")

agent1 = Agent(
    model=Claude(id="claude-3-5-sonnet-20241022"),
    session_id="test_run",
    storage=storage,
    add_history_to_messages=True,
)

agent2 = Agent(
    model=Claude(id="claude-3-5-sonnet-20241022"),
    session_id="test_run",
    storage=storage,
    add_history_to_messages=True,
    tools=[TavilyTools()], 
    show_tool_calls=True
)

chat_session_id = "test_run"

agent2.print_response(
    "What is the weather in paris today?",
    stream=True,
    session_id=chat_session_id,
    user_id="agent2",
)

# agent1.print_response(
#     "What is the capital of france?",
#     stream=True,
#     session_id=chat_session_id,
#     user_id="agent1",
# )

# agent2.print_response(
#     stream=True,
#     # session_id=chat_session_id,
#     user_id="agent2",
# )