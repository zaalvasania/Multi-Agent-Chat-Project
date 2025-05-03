# Multi Agent Chat App

The multi-agent chat app is a python library accessible via a streamlit web ui for enabling LLM's from different providers to interact and converse with each other on a user provided conversation topic. Powered by [agno.ai](https://github.com/agno-agi/agno), each model is able to optionally perform web search via the [Tavily](https://tavily.com/) search API or the [DuckDuckGo](https://duckduckgo.com/) search API and will respond to each other based on their search results and previous conversation context. As of now, various models from [together.ai](https://www.together.ai/), [OpenAI](https://openai.com/), [Anthropic](https://claude.ai/) and [DeepSeek](https://www.deepseek.com/) are supported.

<video src="assets/multi_chat_app_demo.webm" autoplay loop muted width="100%"></video>

## Installation

1. Run make build from within the pulled project repository
2. Copy the dist/*.whl file generated into a new directory of your choosing
3. Within that directory run the following commands

```bash
python3 -m venv <env_name> # Replace <env_name> with your environment name
source <env_name>/bin/activate
pip install *.whl
```
4. Once installed, simply run ```run-multiagent-chat``` in your cli

## Startup

1. Make sure your have activate the virtual env you created above
2. Run ```run-multiagent-chat``` in your cli from the directory of your choice

## Usage

1. Navigate to the 'Help' tab in the sidebar for more information on how to add model configurations and setup the conversation. Note that you will have to create and have your own API keys for the various model providers (and the tavily web search API if you are using it) ready to input into the model configuration fields