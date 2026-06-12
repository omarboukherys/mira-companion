"""Telegram bot interface for Mira.

Run with:
    python -m mira.interfaces.telegram.app
"""

import logging

from langchain_core.messages import HumanMessage
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from mira.graph.graph import get_compiled_graph
from mira.settings import settings


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def on_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Runs when a user sends /start to the bot."""
    await update.message.reply_text(
        "Salam! I'm Mira. Just say hi and we'll chat."
    )


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Runs for every text message the bot receives."""
    user_text = update.message.text
    chat_id = update.message.chat_id

    logger.info(f"Message from chat {chat_id}: {user_text[:50]}")

    async with get_compiled_graph() as graph:
        result = await graph.ainvoke(
            {"messages": [HumanMessage(content=user_text)],
             "user_id":str(chat_id)
             },
            config={"configurable": {"thread_id": str(chat_id)}},
        )

    reply_text = result["messages"][-1].content
    await update.message.reply_text(reply_text)


def main() -> None:
    """Build the bot and start long polling."""
    app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", on_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))

    logger.info("Mira is online on Telegram...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()