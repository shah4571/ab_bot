from pyrogram import filters
from pyrogram.types import Message
from pyrogram import Client
from bot import config as cfg
from bot.utils.storage import add_balance_to_user, set_verification_time, list_users

def init(app: Client):
    @app.on_message(filters.command('admin') & filters.user(cfg.ADMIN_ID))
    async def admin_help(client: Client, message: Message):
        txt = ("Admin commands:\n"
               "/addbalance <user_id> <amount> - Add USD to user\n"
               "/setverifytime <seconds> - Set verification time window\n"
               "/listusers - List all users (id, balance)\n")
        await message.reply(txt)

    @app.on_message(filters.command('addbalance') & filters.user(cfg.ADMIN_ID))
    async def cmd_addbalance(client: Client, message: Message):
        parts = message.text.split()
        if len(parts) != 3:
            await message.reply('Usage: /addbalance <user_id> <amount>')
            return
        try:
            uid = int(parts[1]); amt = float(parts[2])
        except:
            await message.reply('Invalid args')
            return
        add_balance_to_user(uid, amt)
        await message.reply('Balance updated')

    @app.on_message(filters.command('setverifytime') & filters.user(cfg.ADMIN_ID))
    async def cmd_setverifytime(client: Client, message: Message):
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply('Usage: /setverifytime <seconds>')
            return
        try:
            secs = int(parts[1])
        except:
            await message.reply('Invalid number')
            return
        set_verification_time(secs)
        await message.reply(f'Verification time set to {secs} seconds')

    @app.on_message(filters.command('listusers') & filters.user(cfg.ADMIN_ID))
    async def cmd_listusers(client: Client, message: Message):
        users = list_users()
        txt = '\n'.join([f"{u[0]} -> {u[1]} USD" for u in users]) or 'No users.'
        await message.reply(txt)
