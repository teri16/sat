"""Ledger domain service (UI-agnostic).

繁中：核心業務層，處理命令執行、查詢、統計與匯出。
English: Core business layer handling command execution, querying, stats, export, and import.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from zoneinfo import ZoneInfo

from .codec import export_json, import_json
from .commands import Add, CommandParseError, CommandParser, Del, Export, Help, Import, ImportMode, ListCmd, Pie, Sum
from .models import MonthlyStats, Transaction
from .pie import render_expense_pie


class LedgerService:
    """記帳服務 / Ledger service.

    繁中：目前用 in-memory 儲存，後續可替換 Room/IndexedDB。
    English: Uses in-memory storage now; can later be replaced with Room/IndexedDB.
    """

    def __init__(self, timezone: str = "Asia/Taipei") -> None:
        # 繁中：預設時區。/ English: Default timezone.
        self.timezone = timezone
        self._txs: list[Transaction] = []
        self._next_id = 1

    def now(self) -> datetime:
        """取得目前時間 / Get current zoned time."""

        return datetime.now(tz=ZoneInfo(self.timezone))

    def execute(self, raw: str) -> str:
        """命令入口 / Command entrypoint."""

        cmd = CommandParser.parse(raw)

        if isinstance(cmd, Help):
            return self.help_text()

        if isinstance(cmd, Add):
            try:
                amount = Decimal(cmd.amount)
            except InvalidOperation as exc:
                raise CommandParseError("Invalid amount") from exc
            if amount == 0:
                raise CommandParseError("amount cannot be zero")

            now = self.now()
            # 繁中：未提供 occurred_at 時用系統時間。/ English: Default occurred_at to system time.
            tx = Transaction(
                id=self._next_id,
                amount=amount,
                category=cmd.category,
                note=cmd.note,
                occurred_at=now,
                created_at=now,
                deleted=False,
            )
            self._next_id += 1
            self._txs.append(tx)
            return f"Added #{tx.id} {tx.amount} {tx.category}"

        if isinstance(cmd, ListCmd):
            return self._list(cmd.scope)

        if isinstance(cmd, Sum):
            return self._sum(cmd.scope)

        if isinstance(cmd, Del):
            # 繁中：軟刪除。/ English: Soft delete (mark only).
            for i, tx in enumerate(self._txs):
                if tx.id == cmd.tx_id:
                    self._txs[i] = Transaction(**{**tx.__dict__, "deleted": True})
                    return f"Deleted #{cmd.tx_id}"
            return "Not found"

        if isinstance(cmd, Pie):
            return render_expense_pie(self._month_filter(cmd.month))

        if isinstance(cmd, Export):
            if cmd.fmt == "json":
                return export_json(self._txs, self.timezone)
            if cmd.fmt == "csv":
                lines = ["id,amount,category,note,occurred_at,created_at,deleted"]
                for t in self._txs:
                    lines.append(
                        f"{t.id},{t.amount},{t.category},{t.note or ''},"
                        f"{t.occurred_at.isoformat()},{t.created_at.isoformat()},{t.deleted}"
                    )
                return "\n".join(lines)
            return "Unsupported export format"

        if isinstance(cmd, Import):
            return self.import_data(cmd.mode, cmd.payload)

        raise ValueError("Unhandled command")

    def import_data(self, mode: ImportMode, payload: str) -> str:
        """匯入資料 / Import data.

        繁中：
        - merge：保留原有資料並追加。
        - replace：先清空再匯入。

        English:
        - merge: keep existing rows and append imported rows.
        - replace: clear existing rows before import.
        """

        timezone, imported_rows = import_json(payload)
        self.timezone = timezone

        if mode == ImportMode.REPLACE:
            self._txs = []
            self._next_id = 1

        for tx in imported_rows:
            self._txs.append(
                Transaction(
                    id=self._next_id,
                    amount=tx.amount,
                    category=tx.category,
                    note=tx.note,
                    occurred_at=tx.occurred_at,
                    created_at=tx.created_at,
                    deleted=tx.deleted,
                )
            )
            self._next_id += 1

        return f"Imported {len(imported_rows)} records ({mode.value})"

    def monthly_stats(self, ym: str) -> MonthlyStats:
        """月份統計 / Monthly stats by YYYY-MM."""

        month_rows = [t for t in self._txs if not t.deleted and t.occurred_at.strftime("%Y-%m") == ym]
        income = sum((t.amount for t in month_rows if t.amount > 0), Decimal("0"))
        expense = sum((t.amount for t in month_rows if t.amount < 0), Decimal("0"))
        return MonthlyStats(income=income, expense=expense, net=income + expense)

    def _month_filter(self, month: str | None) -> list[Transaction]:
        """月份篩選 / Filter by month."""

        target = month or self.now().strftime("%Y-%m")
        return [t for t in self._txs if t.occurred_at.strftime("%Y-%m") == target]

    def _list(self, scope: str | None) -> str:
        """list 邏輯 / list command logic."""

        rows = [t for t in self._txs if not t.deleted]
        now = self.now()

        if scope in (None, "month"):
            rows = [t for t in rows if t.occurred_at.strftime("%Y-%m") == now.strftime("%Y-%m")]
        elif scope == "today":
            rows = [t for t in rows if t.occurred_at.date() == now.date()]
        elif scope == "7d":
            rows = [t for t in rows if t.occurred_at >= now - timedelta(days=7)]
        elif scope and len(scope) == 7 and scope[4] == "-":
            rows = [t for t in rows if t.occurred_at.strftime("%Y-%m") == scope]

        if not rows:
            return "No records"

        return "\n".join(
            f"#{t.id} {t.occurred_at.date()} {t.amount} {t.category} {t.note or ''}".rstrip() for t in rows
        )

    def _sum(self, scope: str | None) -> str:
        """sum 邏輯 / sum command logic."""

        rows = [t for t in self._txs if not t.deleted]
        now = self.now()

        if scope in (None, "month"):
            rows = [t for t in rows if t.occurred_at.strftime("%Y-%m") == now.strftime("%Y-%m")]
        elif scope == "today":
            rows = [t for t in rows if t.occurred_at.date() == now.date()]
        elif scope == "7d":
            rows = [t for t in rows if t.occurred_at >= now - timedelta(days=7)]
        else:
            rows = [t for t in rows if t.category.lower() == scope.lower()]

        total = sum((t.amount for t in rows), Decimal("0"))
        return f"SUM {scope or 'month'}: {total}"

    @staticmethod
    def help_text() -> str:
        """回傳說明 / Return help text."""

        return (
            "Commands:\n"
            "  add <amount> <category> [note]\n"
            "  list [today|7d|month|YYYY-MM]\n"
            "  sum [today|7d|month|category]\n"
            "  del <id>\n"
            "  pie [month]\n"
            "  export csv|json\n"
            "  import <merge|replace> <json_payload>\n"
            "  help|-h|--help"
        )
