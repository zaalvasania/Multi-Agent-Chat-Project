from setuptools import setup, find_packages

requirements = [
    "anthropic",
    "together",
    "openai",
    "sqlalchemy",
    "agno",
    "tavily-python",
    "duckduckgo-search",
    "streamlit",
    "mcp"
]

setup(
    name="agno_ai_multi_chat_app",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "run-multiagent-chat=agno_ai_multi_chat_app.run:main",
        ],
    },
    scripts=["scripts/run.sh"],
)