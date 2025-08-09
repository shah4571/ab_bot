from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from pyrogram import Client
import datetime

from bot.utils.storage import get_user_info, create_withdrawal, zero_balance
from bot import config as cfg

pending_withdraws = {}  # uid -> {'currency'}

def init(app: Client):
    @app.on_message(filters.command('withdraw') & filters.private)
    async def withdraw_cmd(client: Client, message: Message):
        uid = message.from_user.id
        info = get_user_info(uid)
        if not info:
            await message.reply('No account found. Please /start first.')
            return
        text = (
            "🎫 Your user account in the bot:\n\n"
            f"👤 ID: {info['id']}\n"
            f"🥅 Total successful accounts: {info['success_count']}\n"
            f"💰 Your balance: {info['balance']} USD\n"
            f"⏰ Last updated: {info['updated_at']}\n"
        )
        kb = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("USDT (Bep 20)", callback_data="wd_USDT")],
                [InlineKeyboardButton("TRX", callback_data="wd_TRX")],
                [InlineKeyboardButton("BKASH", callback_data="wd_BKASH")]
            ]
        )
        await message.reply(text, reply_markup=kb)

    @app.on_callback_query(filters.regex(r'^wd_'))
    async def on_withdraw_choice(client, callback):
        uid = callback.from_user.id
        currency = callback.data.split('_', 1)[1]
        await callback.message.reply(
            f"Okay. Send your wallet address for {currency}:",
            reply_markup=ForceReply(selective=True)
        )
        pending_withdraws[uid] = {'currency': currency}
        await callback.answer()

    @app.on_message(filters.private & ~filters.command(["start", "withdraw"]))
    async def handle_wallet_address(client: Client, message: Message):
        uid = message.from_user.id
        if uid not in pending_withdraws:
            return  # Not in withdraw process, ignore

        data = pending_withdraws.pop(uid)
        currency = data['currency']
        address = message.text.strip()

        info = get_user_info(uid)
        if not info:
            await message.reply('No account found. Please /start first.')
            return

        amount_usd = info['balance']
        if amount_usd <= 0:
            await message.reply('You have no balance to withdraw.')
            return

        amount_trx = amount_usd * cfg.USD_TO_TRX_RATE
        tx_id = 'TX' + datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')

        create_withdrawal(uid, currency, amount_usd, address, tx_id)
        zero_balance(uid)

        await message.reply('✅ Withdrawal request received. Our team will process it shortly.')

        report = (
            "📤 Withdrawal successful\n\n"
            f"🔹 Transaction No: {tx_id}\n"
            f"🔹 User ID: {uid}\n"
            f"🔹 Balance: {amount_usd} USD\n"
            f"🔹 Currency: {currency}\n"
            f"🔹 Amount (TRX): {amount_trx}\n"
            f"🔹 Address: {address}\n"
            f"🔹 Transaction ID: {tx_id}\n"
        )
        try:
            await client.send_message(cfg.WITHDRAW_REPORT_CHANNEL_ID, report)
        except Exception as e:
            print('Failed to send withdraw report:', e)
