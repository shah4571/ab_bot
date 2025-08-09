import sqlite3, datetime, os
from bot import config as cfg

DB_PATH = cfg.DB_PATH

schema = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    phone TEXT,
    verified INTEGER DEFAULT 0,
    balance REAL DEFAULT 0.0,
    success_count INTEGER DEFAULT 0,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS withdrawals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    currency TEXT,
    amount REAL,
    address TEXT,
    tx_id TEXT,
    created_at TEXT
);
'''

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(schema)
    conn.commit()
    conn.close()

init_db()

def get_conn():
    return sqlite3.connect(DB_PATH)

def create_or_get_user(user_id: int):
    conn = get_conn(); cur = conn.cursor()
    cur.execute('SELECT id FROM users WHERE id=?', (user_id,))
    row = cur.fetchone()
    if row:
        conn.close(); return True
    now = datetime.datetime.datetime.utcnow().isoformat()
    cur.execute('INSERT INTO users (id, created_at, updated_at) VALUES (?, ?, ?)', (user_id, now, now))
    conn.commit(); conn.close(); return True

def set_user_phone(user_id: int, phone: str):
    conn = get_conn(); cur = conn.cursor()
    cur.execute('UPDATE users SET phone=?, updated_at=? WHERE id=?', (phone, datetime.datetime.datetime.utcnow().isoformat(), user_id))
    conn.commit(); conn.close()

def verify_user_and_add_balance(user_id: int, amount: float):
    conn = get_conn(); cur = conn.cursor()
    cur.execute('UPDATE users SET verified=1, balance = balance + ?, success_count = success_count + 1, updated_at=? WHERE id=?', (amount, datetime.datetime.datetime.utcnow().isoformat(), user_id))
    conn.commit(); conn.close()

def get_user_info(user_id: int):
    conn = get_conn(); cur = conn.cursor()
    cur.execute('SELECT id, phone, verified, balance, success_count, created_at, updated_at FROM users WHERE id=?', (user_id,))
    row = cur.fetchone(); conn.close()
    if not row: return None
    return {'id': row[0], 'phone': row[1], 'verified': bool(row[2]), 'balance': float(row[3]), 'success_count': int(row[4]), 'created_at': row[5], 'updated_at': row[6]}

def create_withdrawal(user_id: int, currency: str, amount: float, address: str, tx_id: str):
    conn = get_conn(); cur = conn.cursor()
    cur.execute('INSERT INTO withdrawals (user_id, currency, amount, address, tx_id, created_at) VALUES (?, ?, ?, ?, ?, ?)', (user_id, currency, amount, address, tx_id, datetime.datetime.datetime.utcnow().isoformat()))
    conn.commit(); conn.close()

def zero_balance(user_id: int):
    conn = get_conn(); cur = conn.cursor()
    cur.execute('UPDATE users SET balance=0, updated_at=? WHERE id=?', (datetime.datetime.datetime.utcnow().isoformat(), user_id))
    conn.commit(); conn.close()

# admin helpers
def add_balance_to_user(user_id: int, amount: float):
    conn = get_conn(); cur = conn.cursor()
    cur.execute('UPDATE users SET balance = balance + ?, updated_at=? WHERE id=?', (amount, datetime.datetime.datetime.utcnow().isoformat(), user_id))
    conn.commit(); conn.close()

def set_verification_time(seconds: int):
    # placeholder: store in-memory
    global VERIFICATION_TIME
    VERIFICATION_TIME = seconds

def list_users():
    conn = get_conn(); cur = conn.cursor()
    cur.execute('SELECT id, balance FROM users')
    rows = cur.fetchall(); conn.close()
    return rows
