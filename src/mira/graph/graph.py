"""Build and export Mira's async, persistent graph."""

from contextlib import asynccontextmanager
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph import StateGraph, START, END

from mira.graph.edges import select_workflow
from mira.graph.nodes import (
    audio_node,
    conversation_node,
    image_node,
    router_node
)

from mira.graph.state import MiraState
from mira.settings import settings

def build_graph():
    """Construct Mira's graph (uncompiled).
    
    Shape:
        START -> router_node ---> conversation_node -> END
                              |-> image_node        -> END
                              |-> audio_node        -> END   
    """
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
            "audio_node":"audio_node",
        },
    )
    builder.add_edge("conversation_node",END)
    builder.add_edge("image_node", END)
    builder.add_edge("audio_node", END)

    return builder

@asynccontextmanager
async def get_compiled_graph():
    """Yield a compiled graph with a SQLite checkpointer attached."""

    async with AsyncSqliteSaver.from_conn_string(settings.SHORT_TERM_MEMORY_DB_PATH) as saver:
        compiled=build_graph().compile(checkpointer=saver)
        yield compiled