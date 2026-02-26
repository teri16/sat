"""Domain layer behavioral tests.

繁中：可當作規格範例，先看輸入再看預期輸出。
English: Serves as executable spec examples: inspect input commands and expected outputs.
"""

from ledger.commands import CommandParseError
from ledger.service import LedgerService


def test_help_aliases() -> None:
    """繁中：help alias 測試。/ English: Verify help aliases."""

    svc = LedgerService()
    assert "Commands" in svc.execute("help")
    assert "add <amount>" in svc.execute("-h")
    assert "sum [today|7d|month|category]" in svc.execute("sum -h")


def test_add_list_sum_del_flow() -> None:
    """繁中：主流程測試。/ English: Core add/list/sum/delete flow."""

    svc = LedgerService()
    svc.execute("add 100 salary monthly")
    svc.execute("add -60 food lunch")

    assert "salary" in svc.execute("list month")
    assert "40" in svc.execute("sum month")
    assert svc.execute("del 1") == "Deleted #1"


def test_ascii_only_rule() -> None:
    """繁中：非 ASCII category 應失敗。/ English: Non-ASCII category should fail."""

    svc = LedgerService()
    try:
        svc.execute("add 100 餐飲 note")
    except CommandParseError:
        pass
    else:
        raise AssertionError("Expected CommandParseError")


def test_pie_and_export_json() -> None:
    """繁中：pie/export 測試。/ English: Verify pie and JSON export."""

    svc = LedgerService()
    svc.execute("add -100 food")
    svc.execute("add -50 transport")

    assert "Expense Pie" in svc.execute("pie")
    assert "schema_version" in svc.execute("export json")


def test_import_merge_and_replace() -> None:
    """繁中：驗證 import merge/replace。/ English: Verify import merge/replace behavior."""

    source = LedgerService()
    source.execute("add 200 salary")
    source.execute("add -30 food")
    payload = source.execute("export json").replace("\n", " ")

    target = LedgerService()
    target.execute("add 10 misc")

    merge_result = target.execute(f"import merge {payload}")
    assert "Imported 2 records (merge)" == merge_result
    assert "SUM month: 180" in target.execute("sum month")

    replace_result = target.execute(f"import replace {payload}")
    assert "Imported 2 records (replace)" == replace_result
    assert "SUM month: 170" in target.execute("sum month")
