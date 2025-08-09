from bot import config as cfg

def usd_to_trx(usd_amount: float) -> float:
    return usd_amount * cfg.USD_TO_TRX_RATE
