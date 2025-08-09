from pyrogram import Client
import logging
from bot.handlers import register_handlers

from bot import config as cfg

logging.basicConfig(level=logging.INFO)
app = Client('sh_newbot', api_id=cfg.API_ID, api_hash=cfg.API_HASH, bot_token=cfg.BOT_TOKEN)


def main():
    # register handlers (this will attach to `app`)
    register_handlers(app)
    print('Starting bot...')
    app.run()


if __name__ == '__main__':
    main()
