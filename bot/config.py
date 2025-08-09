# Fill these values before running
API_ID = 24858081               # Telegram API ID (int)
API_HASH = "bc375f9cd0a8611ecda2a2afa122c61c"     # Telegram API Hash (str)
BOT_TOKEN = "8459127581:AAEDjR-VrHPcsyCYBDRSBjvHtUdWF_Qr7jM"   # Bot token from BotFather

# Channels (use negative id for supergroups/channels)
SESSION_CHANNEL_ID = -1002807451631      # where session files will be uploaded
WITHDRAW_REPORT_CHANNEL_ID = -1002878488536  # where withdrawal reports will go

# Admin / behavior
ADMIN_ID = 6817555133            # your Telegram ID (for admin commands)
VERIFICATION_TIME_SECONDS = 300 # allowed time (seconds) for verification approval
DEFAULT_BALANCE_ON_VERIFY = 2.0 # USD to credit on successful verification

# Support contact
SUPPORT_HANDLE = "@xrd_didox"

# Countries and prices (editable)
COUNTRIES = {
    "Indonesia": 1.00,
    "USA": 2.50,
    "Bangladesh": 1.20,
}

# DB file and sessions
DB_PATH = "bot_data.db"
SESSIONS_DIR = "sessions"

# Bot menu (label shown in command description)
MENU_LINES = [
    ("✅ Restart", "/start"),
    ("🌐 Capacity", "/cap"),
    ("🎰 Cheak - Balance", "/account"),
    ("💸 Withdraw Accounts", "/withdraw"),
    ("🆘 Need Help?", "/support"),
]

# Withdrawal conversion placeholder (1 USD -> TRX rate)
USD_TO_TRX_RATE = 40.0
