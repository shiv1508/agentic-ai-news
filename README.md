# Agentic AI News

Agentic AI News is a small demo that composes a graph-based, agentic chatbot to fetch, summarize, and persist AI-related news. The project uses modular nodes wired by a graph builder, a Groq-backed LLM for generation, and an external search tool (Tavily) for sourcing articles. Summaries are saved as Markdown files under the AINews/ folder and a Streamlit UI provides interactive control.

Table of contents
- [Quick start](#quick-start)
- [Features](#features)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project layout](#project-layout)
- [Development](#development)

## Quick start

Requirements
- Python 3.10+
- Windows (PowerShell or CMD)
- Install dependencies listed in requirements.txt

Install
```powershell
pip install -r requirements.txt
```

Run (app entry)
```powershell
python app.py
```
Or run the Streamlit UI directly:
```powershell
streamlit run src/langgraphagenticai/ui/streamlitui/loadui.py
```

## Features
- Graph-based agent composition (GraphBuilder + nodes)
- Groq LLM wrapper for text generation
- Search tool integration for news discovery (Tavily)
- Streamlit UI with configurable options
- Automatic saving of generated summaries to AINews/ (daily, weekly, monthly)

## Configuration

Environment variables
- TAVILY_API_KEY — API key for the search tool (if required)
- GROQ_API_KEY — API key for Groq LLM (if required)
Set keys in your environment or a secrets manager. Check the LLM and tool wrappers for exact variable names and usage.

## UI configuration
- src/langgraphagenticai/ui/uiconfigfile.ini — UI defaults and options

Where to look in code
- app.py — application entry point
- src/langgraphagenticai/main.py — bootstrap and app loader
- src/langgraphagenticai/graph/graph_builder.py — wires nodes and tools together
- src/langgraphagenticai/nodes/ai_news_node.py — fetch, summarize, and save logic
- src/langgraphagenticai/LLMS/groqllm.py — Groq LLM wrapper
- src/langgraphagenticai/tools/search_tool.py — search tool integration
- src/langgraphagenticai/ui/streamlitui/ — Streamlit UI components
- AINews/ — generated markdown summaries

## Development
- Edit code under src/.
- Add unit tests in a tests/ folder and run with pytest or preferred test runner.
- Use the Streamlit UI to iterate quickly on agent behavior and prompts.

Notes
- This repository contains example integrations and demo code. Verify API keys and environment setup before running.
- Generated summaries are stored in AINews/; clean up or adjust file paths as
