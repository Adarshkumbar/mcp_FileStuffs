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

Using the MCP Python SDK in this project gives you:

- Faster development: define tools/resources/prompts with Python decorators instead of writing raw JSON schemas.
- Built-in validation: type hints and `pydantic` fields validate tool input and produce clearer errors.
- Better model guidance: tool names, descriptions, and parameter metadata are exposed in a model-friendly way.
- Cleaner maintenance: adding or updating server capabilities in `mcp_server.py` is straightforward and readable.
- Safer integration: exceptions and return types map naturally to MCP responses, reducing protocol-level boilerplate.

### Windows troubleshooting (if setup fails)

```powershell
# 1) Activate your project venv
.\.venv\Scripts\activate

# 2) Upgrade pip
python -m pip install --upgrade pip

# 3) Remove broken pydantic installs
pip uninstall -y pydantic-core pydantic

# 4) Reinstall a known-good pydantic v2
pip install "pydantic==2.9.2"
```

## Docker for this project (MCP + Ollama)

In this repo, Docker is used to package and run your MCP server (`mcp_server.py`) consistently, while Ollama remains your local LLM provider.

### Why this helps here

- Your MCP server runs with pinned dependencies from `requirements.txt`.
- Tool behavior stays consistent across machines.
- You can run MCP servers in containers while your app still talks to local Ollama.
- It is easier to test stdio MCP behavior (`stdin`/`stdout`) in a reproducible environment.

### Build your MCP server image

```bash
docker build -t mcp-server:local .
```

### Verify container can load your server module

```bash
docker run --rm mcp-server:local python -c "import mcp_server; print('mcp_server import ok')"
```

### Run your MCP server over stdio

```bash
docker run --rm -i mcp-server:local
```

### Use a Docker MCP server from your app

Your app can connect to extra MCP servers started with Docker commands.

```bash
python main.py "docker run -i --rm mcp-server:local"
```

Notes:
- Keep `-i` so `stdin` stays open for stdio MCP.
- `PYTHONUNBUFFERED=1` in the Docker image helps avoid delayed stdout responses.