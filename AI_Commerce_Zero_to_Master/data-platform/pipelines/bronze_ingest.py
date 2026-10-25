from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sample" / "order_events.jsonl"
BRONZE = ROOT / "lake" / "bronze" / "order_events"


def run() -> list[Path]:
    written: list[Path] = []
    for raw in SOURCE.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        event = json.loads(raw)
        event_time = datetime.fromisoformat(event["occurred_at"].replace("Z", "+00:00")).astimezone(timezone.utc)
        partition = BRONZE / f"dt={event_time:%Y-%m-%d}" / f"hour={event_time:%H}"
        partition.mkdir(parents=True, exist_ok=True)
        out = partition / "events.jsonl"
        envelope = {
            "ingested_at": datetime.now(timezone.utc).isoformat(),
            "source": "commerce-order-events",
            "payload": event,
        }
        with out.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(envelope) + "\n")
        if out not in written:
            written.append(out)
    return written


if __name__ == "__main__":
    for path in run():
        print("BRONZE:", path)
