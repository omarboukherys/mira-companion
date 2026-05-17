"""Chain factories for Mira's LLM workflows."""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq.chat_models import ChatGroq

from mira.core.prompts import CHARACTER_CARD_PROMPT
from mira.settings import settings

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