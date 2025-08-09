from pyrogram import filters
from pyrogram.types import Message
from bot import config as cfg
from pyrogram import Client

def init(app: Client):
    @app.on_message(filters.command('support') & filters.private)
    async def support_cmd(client: Client, message: Message):
        await message.reply(f"Support: {cfg.SUPPORT_HANDLE}")
