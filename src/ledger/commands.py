"""Command parser and command models.

繁中：將使用者輸入字串解析為命令物件，並在此層做語法與 ASCII 規則驗證。
English: Parses raw user input into command objects and validates syntax/ASCII rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CommandParseError(ValueError):
    """繁中：指令格式錯誤。/ English: Raised when command format is invalid."""


class ImportMode(str, Enum):
    """繁中：import 模式。/ English: Import mode enum."""

    MERGE = "merge"
    REPLACE = "replace"


class Command:
    """繁中：命令基底型別。/ English: Marker base command type."""


@dataclass
class Help(Command):
    """繁中：顯示說明。/ English: Show help text."""


@dataclass
class Add(Command):
    """繁中：新增交易。/ English: Add transaction."""

    amount: str
    category: str
    note: str | None


@dataclass
class ListCmd(Command):
    """繁中：列出交易。/ English: List transactions."""

    scope: str | None


@dataclass
class Sum(Command):
    """繁中：加總查詢。/ English: Sum query."""

    scope: str | None


@dataclass
class Del(Command):
    """繁中：刪除交易（軟刪除）。/ English: Delete transaction (soft delete)."""

    tx_id: int


@dataclass
class Pie(Command):
    """繁中：顯示 ASCII 支出圖。/ English: Show ASCII expense chart."""

    month: str | None


@dataclass
class Export(Command):
    """繁中：資料匯出。/ English: Export data."""

    fmt: str


@dataclass
class Import(Command):
    """繁中：資料匯入。/ English: Import data."""

    mode: ImportMode
    payload: str


class CommandParser:
    """繁中：指令解析器。/ English: Command parser."""

    @staticmethod
    def _ascii_only(value: str) -> bool:
        """繁中：檢查是否 ASCII。/ English: Check whether text is ASCII-only."""

        return value.isascii()

    @classmethod
    def parse(cls, raw: str) -> Command:
        """解析命令 / Parse a command string.

        繁中：支援全域 help、命令層級 help、add 的 ASCII 驗證與 import。
        English: Supports global help, command-level help, add ASCII validation, and import.
        """

        text = raw.strip()
        if not text:
            raise CommandParseError("Empty command")

        # 繁中：以空白切詞。/ English: Tokenize by whitespace.
        parts = text.split()
        cmd = parts[0].lower()

        # 繁中：help 快捷鍵。/ English: Global help aliases.
        if text in {"help", "-h", "--help"}:
            return Help()
        # 繁中：子命令 help。/ English: Command-level help.
        if len(parts) > 1 and parts[1] in {"-h", "--help"}:
            return Help()

        if cmd == "add":
            if len(parts) < 3:
                raise CommandParseError("Usage: add <amount> <category> [note]")
            # 繁中：命令與 category 必須 ASCII。/ English: command/category must be ASCII.
            if not cls._ascii_only(parts[0]) or not cls._ascii_only(parts[2]):
                raise CommandParseError("command/category must be ASCII-only")
            # 繁中：保留帶空白 note。/ English: Preserve trailing note with spaces.
            split_with_note = text.split(maxsplit=3)
            note = split_with_note[3] if len(split_with_note) > 3 else None
            return Add(parts[1], parts[2], note)

        if cmd == "list":
            return ListCmd(parts[1] if len(parts) > 1 else None)

        if cmd == "sum":
            return Sum(parts[1] if len(parts) > 1 else None)

        if cmd == "del":
            if len(parts) != 2 or not parts[1].isdigit():
                raise CommandParseError("Usage: del <id>")
            return Del(int(parts[1]))

        if cmd == "pie":
            return Pie(parts[1] if len(parts) > 1 else None)

        if cmd == "export":
            if len(parts) != 2:
                raise CommandParseError("Usage: export csv|json")
            return Export(parts[1].lower())

        if cmd == "import":
            split_import = text.split(maxsplit=2)
            if len(split_import) != 3:
                raise CommandParseError("Usage: import <merge|replace> <json_payload>")
            mode_raw = split_import[1].lower()
            try:
                mode = ImportMode(mode_raw)
            except ValueError as exc:
                raise CommandParseError("Usage: import <merge|replace> <json_payload>") from exc
            return Import(mode=mode, payload=split_import[2])

        raise CommandParseError(f"Unknown command: {cmd}")
