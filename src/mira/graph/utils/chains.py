"""Chain factories for Mira's LLM workflows."""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq.chat_models import ChatGroq

from mira.core.prompts import CHARACTER_CARD_PROMPT, ROUTER_PROMPT, MEMORY_ANALYSIS_PROMPT
from mira.settings import settings

from typing import Literal, Optional
from pydantic import BaseModel, Field

class RouterResponse(BaseModel):
    """The llm's classification of the user's intent."""

    response_type : Literal["conversation", "image", "audio"] = Field(
        description=(
            "Which workflow Mira should use to respond. "
            "'conversation' for normal chat (the default). "
            "'image' only if the user explicitly asks for a picture or image. "
            "'audio' only if the user explicitly asks to hear a voice. "
        )
    )

def get_character_response_chain():
    """Build a chain that makes the llm response as Mira."""
    llm=ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.TEXT_MODEL_NAME,
        temperature=0.7
    )

    prompt=ChatPromptTemplate.from_messages(
        [
            ("system", CHARACTER_CARD_PROMPT),
            MessagesPlaceholder("messages")
        ]
    )

    return prompt | llm

def get_router_chain():
    """Build a chain that classifies the user's intent into a workflow."""

    llm=ChatGroq(
        model=settings.SMALL_TEXT_MODEL_NAME,
        api_key=settings.GROQ_API_KEY,
        temperature=0,
    )

    prompt=ChatPromptTemplate.from_messages([
        ("system", ROUTER_PROMPT),
        MessagesPlaceholder("messages")
    ])

    return prompt | llm.with_structured_output(RouterResponse)

class MemoryAnalysis(BaseModel):
    """Result of analyzing a user message for long-term memory facts."""

    is_important: bool = Field(
        description="Whether the message contains a durable personal fact worth remembering",
    )
    formatted_memory: Optional[str] = Field(
        default=None,
        description="The fact rewritten as a clean third-person statement, or null if not important",
    )


def get_memory_extraction_chain():
    """Chain that judges a user message and extracts a durable fact if present."""
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.SMALL_TEXT_MODEL_NAME,
        temperature=0,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", MEMORY_ANALYSIS_PROMPT),
        ]
    )

    return prompt | llm.with_structured_output(MemoryAnalysis)