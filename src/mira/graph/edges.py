"""Edge functions for Mira's graph.

Each edge function reads state and returns the NAME (str) of the next node.
Used with `add_conditional_edges` for branching.
"""

from mira.graph.state import MiraState

def select_workflow(state: MiraState) -> str:
    """Pick the next node based on the router's decision in state['workflow']."""
    workflow=state.get("workflow", "conversation")

    if workflow == "image":
        return "image_node"
    
    if workflow == "audio":
        return "audio_node"
    
    return "conversation_node"

