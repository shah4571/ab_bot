# bot/main.py

import logging
import sys
from pyrogram import Client
from bot.handlers import register_handlers
from bot import config as cfg

# --- Logging Configuration ---
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def validate_config():
    """
    Ensure all required configs are set before starting.
    """
    required_fields = {
        "API_ID": cfg.API_ID,
        "API_HASH": cfg.API_HASH,
        "BOT_TOKEN": cfg.BOT_TOKEN
    }

    for field, value in required_fields.items():
        if not value or (isinstance(value, str) and not value.strip()):
            logger.error(f"❌ Missing required config: {field}")
            sys.exit(1)


def main():
    """
    Main bot runner.
    """
    validate_config()

    logger.info("🔄 Initializing bot client...")
    app = Client(
        "sh_newbot",
        api_id=cfg.API_ID,
        api_hash=cfg.API_HASH,
        bot_token=cfg.BOT_TOKEN
    )

    # Register all handlers
    register_handlers(app)
    logger.info("✅ All handlers registered successfully.")

    logger.info("🚀 Starting bot...")
    try:
        app.run()
    except Exception as e:
        logger.error(f"❌ Bot stopped due to error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
