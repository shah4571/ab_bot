from .start import init as start_init
from .cap import init as cap_init
from .account import init as account_init
from .withdraw import init as withdraw_init
from .support import init as support_init
from .admin import init as admin_init

def register_handlers(app):
    start_init(app)
    cap_init(app)
    account_init(app)
    withdraw_init(app)
    support_init(app)
    admin_init(app)
