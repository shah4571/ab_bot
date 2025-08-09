from pyrogram import filters
from pyrogram.types import Message
from bot import config as cfg
from pyrogram import Client

def init(app: Client):
    @app.on_message(filters.command('cap') & filters.private)
    async def cap_cmd(client: Client, message: Message):
        lines = [f"{name} — ${price}" for name, price in cfg.COUNTRIES.items()]
        txt = "Available countries and prices:\n\n" + "\n".join(lines)
        await message.reply(txt)
