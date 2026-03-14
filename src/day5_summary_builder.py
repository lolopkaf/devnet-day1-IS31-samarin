#!/usr/bin/env python3
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ART = Path("artifacts/day5")
SCHEMA_VERSION = "5.0"

def now_utc():
    return datetime.now(timezone.utc).isoformat()

def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def sha256_file(p):
    if not p.exists():
        return ""
    return sha256_text(p.read_text(encoding="utf-8", errors="replace"))

def token_hash8(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()[:8]

def read(p):
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""

def contains(p, needle):
    return needle in read(p)

def main():
    token = os.getenv("STUDENT_TOKEN", "").strip()
    name = os.getenv("STUDENT_NAME", "").strip()
    group = os.getenv("STUDENT_GROUP", "").strip()
    th8 = token_hash8(token) if token else ""

    yang_ok = contains(ART / "yang" / "pyang_tree.txt", "+--rw interfaces")
    webex_room = json.loads(read(ART / "webex" / "room_create.json") or "{}")
    webex_ok = th8 in webex_room.get("title", "")
    pt_ok = contains(ART / "pt" / "external_access_check.json", "empty ticket")
    pt_devices_ok = contains(ART / "pt" / "network_devices.json", "1.0")
    pt_hosts_ok = contains(ART / "pt" / "hosts.json", "1.0")

    summary = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": now_utc(),
        "student": {
            "token": token,
            "token_hash8": th8,
            "name": name,
            "group": group
        },
        "yang": {
            "ok": yang_ok,
            "evidence_sha": {
                "ietf_interfaces_yang": sha256_file(ART / "yang" / "ietf-interfaces.yang"),
                "pyang_version": sha256_file(ART / "yang" / "pyang_version.txt"),
                "pyang_tree": sha256_file(ART / "yang" / "pyang_tree.txt"),
            }
        },
        "webex": {
            "ok": webex_ok,
            "room_title_contains_hash8": webex_ok,
            "evidence_sha": {
                "me": sha256_file(ART / "webex" / "me.json"),
                "rooms_list": sha256_file(ART / "webex" / "rooms_list.json"),
                "room_create": sha256_file(ART / "webex" / "room_create.json"),
                "message_post": sha256_file(ART / "webex" / "message_post.json"),
                "messages_list": sha256_file(ART / "webex" / "messages_list.json"),
            }
        },
        "pt": {
            "ok": pt_ok and pt_devices_ok and pt_hosts_ok,
            "empty_ticket_seen": pt_ok,
            "evidence_sha": {
                "external_access_check": sha256_file(ART / "pt" / "external_access_check.json"),
                "serviceTicket": sha256_file(ART / "pt" / "serviceTicket.txt"),
                "network_devices": sha256_file(ART / "pt" / "network_devices.json"),
                "hosts": sha256_file(ART / "pt" / "hosts.json"),
                "postman_collection": sha256_file(ART / "pt" / "postman_collection.json"),
                "postman_environment": sha256_file(ART / "pt" / "postman_environment.json"),
                "pt_internal_output": sha256_file(ART / "pt" / "pt_internal_output.txt"),
            }
        },
        "validation_passed": bool(yang_ok and webex_ok and pt_ok),
        "run": {
            "python": sys.version.split()[0],
            "platform": sys.platform
        }
    }

    out = ART / "summary.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["validation_passed"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
