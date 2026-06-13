"""Shared state schema for Mira's graph."""

from langgraph.graph import MessagesState


class MiraState(MessagesState):
    """The state passed between nodes in Mira's graph.
    
    Inherits `messages` (with append reducer) from MessagesState.
    More fields will be added in later chapters (summary, memory, etc.).
    """
    workflow: str
    user_id: str
    image_data: bytes