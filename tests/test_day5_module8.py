import json
import os
import subprocess
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts" / "day5"
SCHEMA = ROOT / "schemas" / "day5_summary.schema.json"

def jload(p):
    return json.loads(p.read_text(encoding="utf-8"))

def test_day5_summary_and_artifacts():
    env = os.environ.copy()
    assert env.get("STUDENT_TOKEN")
    assert env.get("STUDENT_NAME")
    assert env.get("STUDENT_GROUP")

    r = subprocess.run(
        ["python", "src/day5_summary_builder.py"],
        cwd=str(ROOT), env=env, capture_output=True, text=True
    )
    assert r.returncode in (0, 2), r.stderr

    assert (ART / "summary.json").exists()
    summary = jload(ART / "summary.json")
    schema = jload(SCHEMA)
    jsonschema.validate(instance=summary, schema=schema)

    assert summary["yang"]["ok"] is True
    assert summary["webex"]["room_title_contains_hash8"] is True
    assert summary["pt"]["empty_ticket_seen"] is True

    for fn in [
        "yang/ietf-interfaces.yang", "yang/pyang_version.txt", "yang/pyang_tree.txt",
        "webex/me.json", "webex/rooms_list.json", "webex/room_create.json",
        "webex/message_post.json", "webex/messages_list.json",
        "pt/external_access_check.json", "pt/serviceTicket.txt",
        "pt/network_devices.json", "pt/hosts.json"
    ]:
        assert (ART / fn).exists(), f"missing {fn}"
