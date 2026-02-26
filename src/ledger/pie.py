"""ASCII pie-chart style renderer.

繁中：輸出純文字比例圖，確保 Android Terminal / PWA Console 都可重用。
English: Produces text-only proportional charts for Android terminal and PWA console reuse.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from .models import Transaction


def render_expense_pie(transactions: list[Transaction], width: int = 40) -> str:
    """產生支出 ASCII 圖 / Render an ASCII expense chart.

    繁中：僅計算 amount < 0、排除 deleted、Top 6 + Others、固定 bar 寬度。
    English: Counts only amount < 0, excludes deleted rows, keeps Top 6 + Others, fixed bar width.
    """

    by_category: dict[str, Decimal] = {}
    for tx in transactions:
        # 繁中：只計入未刪除支出。/ English: Include only non-deleted expense rows.
        if tx.deleted or tx.amount >= 0:
            continue
        by_category[tx.category] = by_category.get(tx.category, Decimal("0")) + abs(tx.amount)

    if not by_category:
        return "No expense data."

    # 繁中：依金額排序。/ English: Sort by descending amount.
    ordered = sorted(by_category.items(), key=lambda x: x[1], reverse=True)
    top = ordered[:6]

    # 繁中：其餘合併 Others。/ English: Merge remaining categories into Others.
    if len(ordered) > 6:
        others = sum((v for _, v in ordered[6:]), Decimal("0"))
        top.append(("Others", others))

    total = sum((v for _, v in top), Decimal("0"))

    lines = ["Expense Pie (ASCII)"]
    for category, amount in top:
        pct = amount / total
        # 繁中：轉換為固定寬度 bar。/ English: Convert ratio into a fixed-width bar.
        bar_len = int((pct * width).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        bar = ("#" * bar_len).ljust(width)
        lines.append(f"{category:<12} |{bar}| {amount} ({(pct * 100):.1f}%)")

    return "\n".join(lines)
