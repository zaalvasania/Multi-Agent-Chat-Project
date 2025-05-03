from setuptools import setup, find_packages

setup(
    name="agno_ai_multi_chat_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "anthropic",
        "together",
        "openai",
        "sqlalchemy",
        "agno",
        "tavily-python",
        "duckduckgo-search",
        "streamlit"
    ],
    entry_points={
        "console_scripts": [
            "run-multiagent-chat=agno_ai_multi_chat_app.run:main",
        ],
    },
    scripts=["scripts/run.sh"],
)