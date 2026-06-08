import hashlib
import json
import os
import random
from pathlib import Path

import requests

VIDEO_ID = os.environ["YOUTUBE_VIDEO_ID"]
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

THUMBNAIL_URL = f"https://i.ytimg.com/vi/{VIDEO_ID}/maxresdefault.jpg?v={random.randint(0, 0xFFFFFFFF):08x}"
HASH_FILE = Path("thumbnail_hash.json")


def fetch_thumbnail() -> bytes:
    resp = requests.get(THUMBNAIL_URL, timeout=15)
    resp.raise_for_status()
    if "image" not in resp.headers.get("Content-Type", ""):
        raise ValueError(f"画像が取得できませんでした: {THUMBNAIL_URL}")
    return resp.content


def compute_hash(image_bytes: bytes) -> str:
    return hashlib.sha256(image_bytes).hexdigest()


def load_saved_hash() -> str | None:
    if HASH_FILE.exists():
        return json.loads(HASH_FILE.read_text()).get(VIDEO_ID)
    return None


def save_hash(hash_value: str) -> None:
    data = json.loads(HASH_FILE.read_text()) if HASH_FILE.exists() else {}
    data[VIDEO_ID] = hash_value
    HASH_FILE.write_text(json.dumps(data, indent=2))


def post_to_discord(image_bytes: bytes) -> None:
    requests.post(
        DISCORD_WEBHOOK_URL,
        data={"content": "@everyone こよじゅーるが更新されました。"},
        files={"file": ("thumbnail.jpg", image_bytes, "image/jpeg")},
        timeout=15,
    ).raise_for_status()


def main():
    image_bytes = fetch_thumbnail()
    current_hash = compute_hash(image_bytes)
    saved_hash = load_saved_hash()

    if current_hash != saved_hash:
        print("変更あり\nDiscord へ通知します...")
        post_to_discord(image_bytes)
        save_hash(current_hash)
        print("通知完了")
    else:
        print("変更なし")


if __name__ == "__main__":
    main()
