# MCP Chat

MCP Chat is a command-line interface application that enables interactive chat capabilities with a **local Ollama model**. The application supports document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Context Protocol) architecture.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) running locally

## Setup

### Step 1: Configure the environment variables

1. Create or edit the `.env` file in the project root and verify that the following variables are set correctly:

```
OLLAMA_MODEL=qwen2.5-coder:7b
OLLAMA_BASE_URL=http://localhost:11434
```

Pull the model if needed:

```bash
ollama pull qwen2.5-coder:7b
```

### Step 2: Install dependencies

#### Option 1: Setup with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install uv, if not already installed:

```bash
pip install uv
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv pip install -e .
```

4. Run the project

```bash
uv run main.py
```

#### Option 2: Setup without uv

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the project

```bash
python main.py 
```
if there are issues use the python present in the .venv

## Usage

### Basic Interaction

Simply type your message and press Enter to chat with the model.

### Document Retrieval

Use the @ symbol followed by a document ID to include document content in your query:

```
> Tell me about @deposition.md
```

### Commands

Use the / prefix to execute commands defined in the MCP server:

```
> /summarize deposition.md
```

Commands will auto-complete when you press Tab.

## Development

### Adding New Documents

Edit the `mcp_server.py` file to add new documents to the `docs` dictionary.

### Implementing MCP Features

To fully implement the MCP features:

1. Complete the TODOs in `mcp_server.py`
2. Implement the missing functionality in `mcp_client.py`

### Linting and Typing Check

There are no lint or type checks implemented.


### Key Benefits of the SDK Approach
No manual JSON schema writing required
Type hints provide automatic validation
Clear parameter descriptions help the model understand tool usage
Error handling integrates naturally with Python exceptions
Tool registration happens automatically through decorators
The MCP Python SDK transforms tool creation from a complex schema-writing exercise into simple Python function definitions. This approach makes it much easier to build and maintain MCP servers while ensuring LLM receives properly formatted tool specifications.


### For windows and facing issues with above steps (created venv for local dependencies)

# 1. Activate your project venv
.\.venv\Scripts\activate

# 2. Make sure pip itself is up to date
python -m pip install --upgrade pip

# 3. Remove any broken installs
pip uninstall -y pydantic-core pydantic

# 4. Reinstall a known-good pydantic v2 (which pulls pydantic-core)
pip install "pydantic==2.9.2"