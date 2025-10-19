import os, json
from pathlib import Path
from datetime import datetime, timezone
import aiohttp

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USERS_JSON = DATA_DIR / "users.json"

def _load_users():
    if USERS_JSON.exists():
        return json.loads(USERS_JSON.read_text("utf-8"))
    return {}

def _save_users(users):
    USERS_JSON.write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")

def ensure_user(users, uid: int):
    s = str(uid)
    if s not in users:
        users[s] = {
            "lang": "ru",
            "consent": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_active": datetime.now(timezone.utc).isoformat(),
        }
        _save_users(users)
    return users[s]

async def send_key_to_backend(url: str, user_id: int, raw_key: str) -> bool:
    """
    ВАЖНО: ключ мы НЕ сохраняем. Только отправляем на ваш backend webhook.
    """
    if not url:
        return False
    try:
        async with aiohttp.ClientSession() as s:
            payload = {"user_id": user_id, "key": raw_key, "event": "connect"}
            async with s.post(url, json=payload, timeout=15) as resp:
                return resp.status in (200, 201, 202)
    except Exception:
        return False
