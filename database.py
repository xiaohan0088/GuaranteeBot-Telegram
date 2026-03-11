# database.py
import sqlite3
import threading
import json
import time
from typing import Optional, List, Dict, Any
import config

class Database:
    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.conn = sqlite3.connect(config.DATABASE_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()
        self._initialized = True

    def _create_tables(self):
        # 群组授权表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY,
                group_name TEXT,
                group_link TEXT,
                number TEXT UNIQUE,
                deposit INTEGER,
                remaining_deposit INTEGER,
                business TEXT,
                stars INTEGER,
                owner_id INTEGER,
                owner_name TEXT,
                authorized_by INTEGER,
                authorized_by_name TEXT,
                authorized_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duration INTEGER
            )
        ''')
        # 全局配置表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        # 授权码表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS auth (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                auth_code TEXT,
                expiry_time TEXT,
                last_check INTEGER
            )
        ''')
        self.conn.commit()

    # ---------- 群组操作 ----------
    def add_group(self, group_id: int, group_name: str, group_link: str, number: str,
                  deposit: int, business: str, stars: int, owner_id: int, owner_name: str,
                  authorized_by: int, authorized_by_name: str, duration: int) -> bool:
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO groups 
                (group_id, group_name, group_link, number, deposit, remaining_deposit, business, stars,
                 owner_id, owner_name, authorized_by, authorized_by_name, duration)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (group_id, group_name, group_link, number, deposit, deposit, business, stars,
                  owner_id, owner_name, authorized_by, authorized_by_name, duration))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Add group error: {e}")
            return False

    def get_group(self, group_id: int) -> Optional[Dict[str, Any]]:
        self.cursor.execute('SELECT * FROM groups WHERE group_id = ?', (group_id,))
        row = self.cursor.fetchone()
        if row:
            columns = [desc[0] for desc in self.cursor.description]
            return dict(zip(columns, row))
        return None

    def get_group_by_number(self, number: str) -> Optional[Dict[str, Any]]:
        self.cursor.execute('SELECT * FROM groups WHERE number = ?', (number,))
        row = self.cursor.fetchone()
        if row:
            columns = [desc[0] for desc in self.cursor.description]
            return dict(zip(columns, row))
        return None

    def update_group(self, group_id: int, **kwargs) -> bool:
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = ?")
            values.append(value)
        if not fields:
            return False
        values.append(group_id)
        query = f"UPDATE groups SET {', '.join(fields)} WHERE group_id = ?"
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Update group error: {e}")
            return False

    def delete_group(self, group_id: int) -> bool:
        try:
            self.cursor.execute('DELETE FROM groups WHERE group_id = ?', (group_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Delete group error: {e}")
            return False

    # ---------- 全局配置 ----------
    def set_config(self, key: str, value: str):
        self.cursor.execute('INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)', (key, value))
        self.conn.commit()

    def get_config(self, key: str) -> Optional[str]:
        self.cursor.execute('SELECT value FROM config WHERE key = ?', (key,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def delete_config(self, key: str):
        self.cursor.execute('DELETE FROM config WHERE key = ?', (key,))
        self.conn.commit()

    # 按钮配置：存储为JSON列表
    def set_buttons(self, buttons: List[List[str]]):
        self.set_config('buttons', json.dumps(buttons))

    def get_buttons(self) -> List[List[str]]:
        val = self.get_config('buttons')
        return json.loads(val) if val else []

    # ---------- 授权码 ----------
    def set_auth_code(self, auth_code: str, expiry_time: str = ""):
        self.cursor.execute('DELETE FROM auth')
        self.cursor.execute('INSERT INTO auth (auth_code, expiry_time, last_check) VALUES (?, ?, ?)',
                            (auth_code, expiry_time, 0))
        self.conn.commit()

    def get_auth_code(self) -> Optional[str]:
        self.cursor.execute('SELECT auth_code FROM auth')
        row = self.cursor.fetchone()
        return row[0] if row else None

    def update_auth_check(self, expiry_time: str = ""):
        self.cursor.execute('UPDATE auth SET last_check = ?', (int(time.time()),))
        if expiry_time:
            self.cursor.execute('UPDATE auth SET expiry_time = ?', (expiry_time,))
        self.conn.commit()

    def close(self):
        self.conn.close()