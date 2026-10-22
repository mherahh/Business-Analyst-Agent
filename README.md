# Modular Business Analyst Agent

## Setup
1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your OpenRouter API key.
4. Run from this project directory: `python main.py`

Generated SVG, JSON, and DOCX files are saved in `outputs/`.

## Structure
- `main.py`: terminal entry point
- `config/`: settings and static project choices
- `agent/state.py`: LangGraph shared state
- `agent/nodes.py`: workflow steps
- `agent/routing.py`: conditional routing functions
- `agent/graph.py`: graph wiring
- `services/llm_service.py`: model calls and JSON parsing
- `services/document_service.py`: Word document generation

The graph behavior is intended to remain the same; this change separates responsibilities into modules.
