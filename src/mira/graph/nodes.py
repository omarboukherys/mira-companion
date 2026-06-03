"""Node functions for Mira's graph.

Each node is a pure function:
  - Takes the current state as input
  - Performs work (e.g. calls an LLM)
  - Returns a dict of fields to UPDATE in state
"""

from mira.graph.state import MiraState
from mira.graph.utils.chains import get_character_response_chain, get_router_chain
from langchain_core.messages import AIMessage

def conversation_node(state: MiraState) -> dict:
    """Generate Mira's reply using the charecter chain."""
    chain=get_character_response_chain()
    response=chain.invoke({"messages": state['messages']})
    return {"messages": [response]}

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