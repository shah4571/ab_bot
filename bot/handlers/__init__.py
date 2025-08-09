# bot/handlers/__init__.py

from .start import init as start_init
from .cap import init as cap_init
from .account import init as account_init
from .withdraw import init as withdraw_init
from .support import init as support_init
from .admin import init as admin_init


def register_handlers(app):
    """
    Register all bot handlers safely.
    If a handler fails to load, log the error but keep the bot running.
    """
    handlers = [
        ("start", start_init),
        ("cap", cap_init),
        ("account", account_init),
        ("withdraw", withdraw_init),
        ("support", support_init),
        ("admin", admin_init)
    ]

    for name, init_func in handlers:
        try:
            init_func(app)
            print(f"✅ Loaded handler: {name}")
        except Exception as e:
            print(f"❌ Failed to load handler '{name}': {e}")
