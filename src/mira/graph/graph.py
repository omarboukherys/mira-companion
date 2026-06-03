"""Build and export Mira's compiled graph."""

from langgraph.graph import StateGraph, START, END
from mira.graph.edges import select_workflow
from mira.graph.nodes import (
    audio_node,
    image_node,
    conversation_node,
    router_node
)

from mira.graph.state import MiraState

def build_graph():
    """Construct Mira's graph with routing."""
    builder=StateGraph(MiraState)
    builder.add_node("router_node", router_node)
    builder.add_node("conversation_node", conversation_node)
    builder.add_node("image_node", image_node)
    builder.add_node("audio_node", audio_node)
    builder.add_edge(START, "router_node")
    builder.add_conditional_edges(
        "router_node",
        select_workflow,
        {
            "conversation_node":"conversation_node",
            "image_node":"image_node",
            "audio_node":"audio_node"
        }
    )
    builder.add_edge("conversation_node", END)
    builder.add_edge("image_node", END)
    builder.add_edge("audio_node", END)

    return builder

graph=build_graph().compile()