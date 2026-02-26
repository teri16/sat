"""JSON export/import codec.

繁中：使用平台中立 JSON schema，方便 Android 與 PWA 共用。
English: Uses a platform-neutral JSON schema so Android and PWA can share data.
"""

from __future__ import annotations

import json
from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from .models import Transaction


def export_json(transactions: list[Transaction], timezone: str, currency: str = "TWD") -> str:
    """匯出 JSON Schema v1 / Export JSON Schema v1."""

    payload = {
        "schema_version": "v1",
        "timezone": timezone,
        "currency": currency,
        "transactions": [
            {
                "amount": str(tx.amount),
                "category": tx.category,
                "note": tx.note,
                "occurred_at": tx.occurred_at.isoformat(),
                "created_at": tx.created_at.isoformat(),
                "deleted": tx.deleted,
            }
            for tx in transactions
        ],
    }
    # 繁中：確保 ASCII 可讀。/ English: Keep output ASCII-safe for terminal environments.
    return json.dumps(payload, ensure_ascii=True, indent=2)


def import_json(payload: str) -> tuple[str, list[Transaction]]:
    """由 JSON 匯入交易 / Import transactions from JSON."""

    data = json.loads(payload)
    tz = data["timezone"]
    # 繁中：驗證時區。/ English: Validate timezone string.
    _ = ZoneInfo(tz)

    rows: list[Transaction] = []
    for i, tx in enumerate(data.get("transactions", []), start=1):
        rows.append(
            Transaction(
                id=i,
                # 繁中：轉 Decimal 防止浮點誤差。/ English: Use Decimal to avoid float precision errors.
                amount=Decimal(tx["amount"]),
                category=tx["category"],
                note=tx.get("note"),
                occurred_at=datetime.fromisoformat(tx["occurred_at"]),
                created_at=datetime.fromisoformat(tx["created_at"]),
                deleted=tx.get("deleted", False),
            )
        )

    return tz, rows
