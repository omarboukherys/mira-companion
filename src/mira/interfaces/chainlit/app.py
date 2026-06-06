"""Chainlit UI for Mira.

Run with:
    chainlit run src/mira/interfaces/chainlit/app.py
"""

import uuid
import chainlit as cl
from langchain_core.messages import HumanMessage
from mira.graph.graph import get_compiled_graph

@cl.on_chat_start
async def on_chat_start():
    """Runs once when a user opens the chat page."""

    thread_id=str(uuid.uuid4())
    cl.user_session.set("thread_id", thread_id)

    await cl.Message(
        content="Salam! I'm Mira. What's up ?",
        author="Mira",
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """Runs every time the user sends a message."""
    thread_id=cl.user_session.get("thread_id")

    async with get_compiled_graph() as graph:
        result=await graph.ainvoke(
            {
                "messages": [HumanMessage(content=message.content)]
            },
            config={"configurable": {"thread_id": thread_id}}
        )
    
    reply_text=result['messages'][-1].content

    await cl.Message(
        content=reply_text,
        author="Mira"
    ).send()