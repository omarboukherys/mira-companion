"""Node functions for Mira's graph.

Each node is a pure function:
  - Takes the current state as input
  - Performs work (e.g. calls an LLM)
  - Returns a dict of fields to UPDATE in state
"""

from mira.graph.state import MiraState
from mira.graph.utils.chains import get_character_response_chain, get_router_chain
from langchain_core.messages import AIMessage
from mira.graph.utils.chains import get_memory_extraction_chain
from mira.graph.utils.memory import memory_manager

def conversation_node(state: MiraState):
    """Generate Mira's in-character reply, enriched with long-term memories."""
    last_message = state["messages"][-1]

    memories = memory_manager.retrieve_memories(
        query=last_message.content,
        user_id=state["user_id"],
        top_k=3,
    )
    memories_text = "\n".join(f"- {m}" for m in memories) if memories else "Nothing yet."

    chain = get_character_response_chain()
    response = chain.invoke(
        {
            "messages": state["messages"],
            "memories": memories_text,
        }
    )

    return {"messages": [response]}

def memory_extraction_node(state: MiraState):
    """Analyze the latest user message and store any durable fact in Qdrant."""
    last_message = state["messages"][-1]

    chain = get_memory_extraction_chain()
    analysis = chain.invoke({"message": last_message.content})

    if analysis.is_important and analysis.formatted_memory:
        memory_manager.store_memory(
            text=analysis.formatted_memory,
            user_id=state["user_id"],
        )

    return {}

def router_node(state: MiraState) -> dict:
    """Classify the user's intent and write the chosen workflow to state."""
    chain=get_router_chain()
    result=chain.invoke({"messages": state['messages']})

    return {"workflow": result.response_type}

def image_node(state: MiraState) -> dict:
    """Stub: pretends to generate an image. Returns a placeholder text reply."""
    placeholder=AIMessage(
        content="Image generation is not wired up yet"
    )
    return {"messages": [placeholder]}

def audio_node(state: MiraState) -> dict:
    """Stub: pretends to generate an audio."""
    placeholder= AIMessage(
        content="Audio generation is not wired up yet."
    )

    return {"messages": [placeholder]}