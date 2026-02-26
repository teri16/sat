# sat — Terminal Ledger App v1（Android First / PWA Ready）

> 一句話定位：這是一個「Terminal 風格記帳 App」的 **Domain Core 原型專案**，
> 先把規格與商業邏輯做對，再接 Android UI，最後延伸到 PWA。

---

## README 導引（先看這裡）

如果你是第一次進來，建議照這個順序讀：

1. **先讀〈專案現在做到哪〉**：理解目前不是完整 App，而是核心邏輯層。
2. **再看〈快速上手〉**：先跑測試，確認環境可用。
3. **再讀〈核心流程地圖〉**：從 command 到統計輸出，掌握主幹。
4. **最後看〈下一步落地計畫〉**：知道 Android/PWA 怎麼串接。

這份 README 目標是讓你在 10 分鐘內知道：
- 這個專案要解決什麼問題
- 目前哪些功能已可用
- 下一步該從哪裡開始貢獻

---

## 專案現在做到哪（Current Scope）

目前 repository 已完成 **Domain Layer（核心邏輯）**，可被 Android 與未來 PWA 共用：

- ✅ 指令解析（`add/list/sum/del/pie/export/help`）
- ✅ ASCII-only 規則驗證
- ✅ 月統計（Income / Expense / Net）
- ✅ ASCII 圖表輸出（Top 6 + Others）
- ✅ JSON/CSV 匯出
- ✅ `pytest` 行為測試

> 目前尚未包含 Android 畫面與資料庫整合（Room / IndexedDB）。

---

## 為甚麼先用 Python 編寫？

這一版先用 Python 的目的，是**快速驗證規格與行為是否正確**：

1. **迭代快**：能先把 parser、統計、圖表、輸出格式定下來。
2. **低耦合**：先讓 Domain 跑通，避免過早被平台框架綁住。
3. **測試友善**：`pytest` 能快速把需求變成可執行規格。
4. **學習友善**：程式碼較精簡，適合先理解業務語意。

> 後續可等價移植到 Kotlin Domain module，確保 Android 與 PWA 共用同一套行為定義。

---

## 快速上手（Quick Start）

### 1) 執行測試

```bash
pytest
```

### 2) 你應該看到

- 所有測試通過（目前 4 個核心行為測試）
- 代表 command parsing、加總/刪除流程、ASCII 規則、export/pie 目前可用

---

## 核心流程地圖（你要先理解的主幹）

### 使用者輸入到結果輸出的路徑

```text
Input Command
   ↓
CommandParser (語法/ASCII 驗證)
   ↓
LedgerService.execute()
   ↓
Domain Logic（add/list/sum/del/pie/export）
   ↓
Text Output / JSON / CSV
```

### 你可以先追一條主線

建議從這條開始讀：

`add -> list month -> sum month -> del -> sum month`

這條路徑可以一次看懂：
- 交易如何建立
- 月份如何歸屬
- 軟刪除如何影響統計

---

## 專案結構（讀檔案地圖）

- `src/ledger/models.py`
  - 核心資料模型：`Transaction`, `MonthlyStats`
- `src/ledger/commands.py`
  - 指令 parser、help 規則、ASCII-only 驗證
- `src/ledger/service.py`
  - 主要業務入口 `execute()` 與查詢/統計邏輯
- `src/ledger/pie.py`
  - ASCII 支出圖（expense-only、Top 6 + Others）
- `src/ledger/codec.py`
  - JSON Schema v1 匯入匯出
- `tests/test_ledger.py`
  - 可執行規格（行為測試）

---

## 給新手的 30 分鐘學習路線

1. 先讀 `tests/test_ledger.py`：知道系統預期行為。
2. 再讀 `commands.py`：知道輸入怎麼被解析。
3. 再讀 `service.py`：知道命令如何轉成業務結果。
4. 最後讀 `pie.py` / `codec.py`：知道輸出格式與跨平台邊界。

> 心法：先看「輸入與輸出」，再看「中間邏輯」。

---

## 下一步落地計畫（Roadmap）

1. Android UI：Top Bar / Output / Input / 功能鍵列
2. Android Data Layer：Room（離線持久化）
3. PWA Data Layer：IndexedDB（格式與 Domain 對齊）
4. 補完 Import mode：`merge` / `replace`
5. 支援 `occurred_at` 參數輸入與更完整時間驗證

---

## 貢獻建議（Contribution Guide Lite）

若你要提 PR，建議優先做：

- 小步提交：一次只改一個行為面向（例如只改 `sum` 的篩選）
- 先補測試再改程式：讓需求變化可追溯
- 維持 Domain 純淨：不要在核心層引入 Android/Web API

