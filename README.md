# sat — Terminal Ledger App v1（Android First / PWA Ready）

這個 repository 目前先完成 **Domain Layer（核心邏輯）**，作為 Android UI 與未來 PWA UI 的共用基礎。

## 為甚麼先用 Python 編寫？

這一版先用 Python 的原因是「**快速把規格落地並驗證 domain 行為**」：

1. **開發與迭代速度快**：可先把 command parser、統計、ASCII 圖表、匯出格式做對。
2. **跨平台原型友善**：Domain 層先以純邏輯實作，不綁 Android API，便於後續移植。
3. **測試門檻低**：`pytest` 可以快速建立規格測試，讓需求討論有可執行依據。
4. **便於教學**：語法相對精簡，適合新手先專注理解業務規則，而非框架細節。

> 這不代表最終 Android 版本一定使用 Python。當規格穩定後，可等價移植到 Kotlin Domain module，
> 並讓 Android / PWA 共用一致行為與資料格式。

## 專案結構

- `src/ledger/models.py`
  - 核心資料模型：`Transaction`, `MonthlyStats`。
- `src/ledger/commands.py`
  - 指令 parser 與命令模型。
  - 支援 `help / -h / --help` 與子命令 help。
  - 內建 ASCII-only 驗證（command/category）。
- `src/ledger/service.py`
  - Domain service（UI 無關）。
  - 提供 `add/list/sum/del/pie/export`。
  - 月統計 `monthly_stats(YYYY-MM)`。
- `src/ledger/pie.py`
  - ASCII 圓餅圖（expense-only、Top 6 + Others、固定寬度 bar）。
- `src/ledger/codec.py`
  - JSON Schema v1 匯出格式（`schema_version/timezone/currency/transactions[]`）。
- `tests/test_ledger.py`
  - v1 核心流程測試。

## 已落地的規格重點

- 指令系統：`add/list/sum/del/pie/export/help`
- Help 規則：`help`、`-h`、`--help`、`<cmd> -h`
- ASCII-only（核心層）
- 月統計：Income / Expense / Net
- ASCII Pie：支出統計、Top 6 + Others
- Export：`csv`、`json`
- 時區：預設 `Asia/Taipei`（可擴充）

## 給新手的學習順序

1. 先讀 `commands.py` 了解指令語法與限制。
2. 再讀 `service.py`，從 `execute()` 走一次 add/list/sum 的主流程。
3. 讀 `pie.py` 理解純文字圖表如何在 Domain 層生成。
4. 最後看 `tests/test_ledger.py`，用測試案例快速掌握行為規格。

## 執行測試

```bash
pytest
```

## 下一步建議

1. Android UI（Top Bar / Terminal Output / Input / 功能鍵列）串接 `LedgerService`。
2. Data Layer：Android 端接 Room，Web 端接 IndexedDB。
3. 補上 Import（merge/replace）入口。
4. 增加 `occurred_at` 參數輸入與完整格式驗證。
