from pyrogram import filters
from pyrogram.types import Message
from bot.utils.storage import get_user_info, create_or_get_user
from pyrogram import Client

def init(app: Client):
    @app.on_message(filters.command('account') & filters.private)
    async def account_cmd(client: Client, message: Message):
        uid = message.from_user.id
        create_or_get_user(uid)
        info = get_user_info(uid)
        if not info:
            await message.reply('No account information yet. Type /start to begin.')
            return
        text = (
            "🎫 Your user account in the robot:\n\n"
            f"👤ID: {info['id']}\n"
            f"🥅 Totally success account : {info['success_count']}\n"
            f"💰 Your balance: {info['balance']} USD\n"
            f"⏰ This post was taken in {info['updated_at']}\n"
        )
        await message.reply(text)
