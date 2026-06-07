# Mira: a multi-user AI companion

A persistent, character-driven LLM agent built with LangGraph, structured output, and a real-time Chainlit web UI.

![Mira chatting in the Chainlit UI](docs/screenshots/mira_demo.png)

## What is Mira?

Mira is a Moroccan freelance ML engineer character, built as an end-to-end AI companion that can hold real, contextual conversations with multiple users at the same time.

This isn't a wrapper around an API. It's a full agent architecture:

- A typed state graph orchestrates every turn
- An LLM-powered router decides between conversation, image, and audio workflows
- A SQLite checkpointer gives Mira persistent short-term memory across sessions
- An async-first design lets her handle multiple users concurrently
- A Chainlit web UI makes her chattable in any browser

Mira speaks English by default but sprinkles in Darija (Moroccan Arabic) and French, because she is from Casablanca.

## Features

- **Persistent memory.** Every conversation is saved to SQLite via LangGraph's AsyncSqliteSaver. Close the browser, come back, your chat is still there.
- **Multi-user concurrent sessions.** Each browser session gets its own thread_id. Open the app in two browsers and they have completely isolated conversations on the same server.
- **LLM-powered routing.** A small classifier model decides whether each message should trigger the conversation, image, or audio workflow, using structured Pydantic output (no string parsing).
- **Character-grounded persona.** Mira's identity, style, and Darija sprinkles live in one prompt file. Tweak it, instantly change who she is.
- **Async-first architecture.** The graph is fully async, so the same Python process can serve many users at once without blocking.
- **Stub-driven extensibility.** Image and audio nodes are stubs ready to be wired to FLUX or ElevenLabs or any other API.
- **Clean Python project layout.** src/ layout, editable install, typed config with Pydantic Settings, PEP 8 imports.

## Quickstart

Requires Python 3.11+ and a Groq API key (free tier works fine, get one at https://console.groq.com/keys).

### 1. Clone the repo

    git clone https://github.com/omarboukherys/mira-companion.git
    cd mira-companion

### 2. Create a virtual environment

    python -m venv .venv
    .venv\Scripts\activate

On macOS or Linux use `source .venv/bin/activate` instead.

### 3. Install dependencies

    pip install -e .

### 4. Configure your API key

    copy .env.example .env

On macOS or Linux use `cp .env.example .env` instead.

Then open `.env` and paste your Groq API key:

    GROQ_API_KEY=gsk_your_key_here

### 5. Launch the chat UI

    chainlit run src/mira/interfaces/chainlit/app.py

Your browser will open at http://localhost:8000 and you can start chatting with Mira.

## Architecture

Mira's brain is a directed graph. Each turn the graph:

1. Loads previous state from SQLite for this thread_id, if any
2. Runs router_node, which classifies the intent into conversation, image, or audio using structured Pydantic output
3. Branches to the matching workflow node
4. Persists the new state back to SQLite
5. Returns the assistant's reply

The same graph definition handles many users in flight at once, since async lets the SQLite and LLM I/O overlap across sessions.

## Tech Stack

| Layer          | Tool                                                 |
| -------------- | ---------------------------------------------------- |
| Language       | Python 3.11                                          |
| LLM provider   | Groq (Llama 3.3 70B and 3.1 8B)                      |
| Orchestration  | LangGraph                                            |
| LLM framework  | LangChain                                            |
| Persistence    | SQLite via langgraph-checkpoint-sqlite and aiosqlite |
| Validation     | Pydantic v2 and Pydantic Settings                    |
| Web UI         | Chainlit                                             |
| Project layout | src/ layout, pyproject.toml, editable install        |

## Project Structure

| Path                                  | Purpose                                      |
| ------------------------------------- | -------------------------------------------- |
| `src/mira/settings.py`                | Typed config (Pydantic Settings)             |
| `src/mira/core/prompts.py`            | Mira's character and router prompts          |
| `src/mira/graph/state.py`             | MiraState, the shared bus between nodes      |
| `src/mira/graph/nodes.py`             | Router, conversation, image stub, audio stub |
| `src/mira/graph/edges.py`             | select_workflow, the branching logic         |
| `src/mira/graph/graph.py`             | Async graph and SQLite checkpointer          |
| `src/mira/graph/utils/chains.py`      | Character and router chain factories         |
| `src/mira/interfaces/chainlit/app.py` | Web UI handlers                              |
| `notebooks/`                          | Chapter-by-chapter exploration notebooks     |
| `data/memory.db`                      | Persistent SQLite brain (gitignored)         |
| `docs/screenshots/`                   | Demo images                                  |
| `pyproject.toml`                      | Project metadata and dependencies            |

## The Build Journey

Mira was built as a chapter-by-chapter learning exercise, not a copy-paste tutorial. Each commit on `main` represents one architectural milestone.

| Chapter | Concept                                                     |
| ------- | ----------------------------------------------------------- |
| 1       | Project setup: venv, pyproject.toml, editable install       |
| 2       | Typed configuration: Pydantic Settings and singleton        |
| 3       | First LLM contact: message types, ChatGroq                  |
| 4       | First chain: ChatPromptTemplate, LCEL pipe operator         |
| 5       | Hello graph: state, nodes, edges, compilation               |
| 6       | Branching router: structured output and conditional edges   |
| 7       | Persistent memory: async, asynccontextmanager, checkpointer |
| 8       | Chainlit UI: multi-user sessions, real-time chat            |

The exploration notebooks in `notebooks/` mirror this progression. Open them to see each concept in isolation before it was wired into `src/mira/`.

## License

MIT. Feel free to fork, adapt, learn from, and share.

Built by [Omar Boukherys](https://github.com/omarboukherys).
