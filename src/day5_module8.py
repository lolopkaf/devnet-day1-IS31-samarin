#!/usr/bin/env python3
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

ART = Path("artifacts/day5/webex")
WEBEX_BASE = "https://webexapis.com/v1"

def now_utc():
    return datetime.now(timezone.utc).isoformat()

def dump_json(obj, path):
    text = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")
    return text

def token_hash8(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()[:8]

def main():
    st_token = os.getenv("STUDENT_TOKEN", "").strip()
    webex_token = os.getenv("WEBEX_TOKEN", "").strip()
    st_name = os.getenv("STUDENT_NAME", "").strip()
    st_group = os.getenv("STUDENT_GROUP", "").strip()

    if not webex_token:
        print("ERROR: set WEBEX_TOKEN", file=sys.stderr)
        return 1

    th8 = token_hash8(st_token)
    ART.mkdir(parents=True, exist_ok=True)

    headers = {
        "Authorization": f"Bearer {webex_token}",
        "Content-Type": "application/json"
    }

    # 1) Get me
    r = requests.get(f"{WEBEX_BASE}/people/me", headers=headers)
    me = r.json()
    dump_json(me, ART / "me.json")
    print(f"me: {me.get('displayName', 'unknown')}")

    # 2) List rooms
    r = requests.get(f"{WEBEX_BASE}/rooms", headers=headers)
    rooms = r.json()
    dump_json(rooms, ART / "rooms_list.json")
    print(f"rooms: {len(rooms.get('items', []))}")

    # 3) Create room
    room_title = f"DevNet Day5 {th8} {st_name}"
    r = requests.post(f"{WEBEX_BASE}/rooms",
                      headers=headers,
                      json={"title": room_title})
    room = r.json()
    dump_json(room, ART / "room_create.json")
    room_id = room.get("id")
    print(f"room created: {room_title}")

    # 4) Post message
    msg_text = f"Hello from {st_name} token_hash8={th8}"
    r = requests.post(f"{WEBEX_BASE}/messages",
                      headers=headers,
                      json={"roomId": room_id, "text": msg_text})
    msg = r.json()
    dump_json(msg, ART / "message_post.json")
    print(f"message posted: {msg_text}")

    # 5) List messages
    r = requests.get(f"{WEBEX_BASE}/messages",
                     headers=headers,
                     params={"roomId": room_id})
    msgs = r.json()
    dump_json(msgs, ART / "messages_list.json")
    print(f"messages: {len(msgs.get('items', []))}")

    print("Webex done!")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
