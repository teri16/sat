# Terminal Ledger App — Full Detailed Issue Checklist v1

> Strategy: 同時設計、先開發 Android。Domain Layer 必須 UI-independent，未來 PWA 只換 UI + Storage。

Legend:
- [x] done in current repo
- [~] partially done
- [ ] pending

---

## Milestone 0 — Repo Baseline & Conventions
- [~] 0.1 Create repo skeleton + folder boundaries
- [ ] 0.2 Define coding conventions + output format contract
- [x] 0.3 Add docs: v1 spec + PWA plan placeholder

## Milestone 1 — Domain Models & Time
- [x] 1.1 Domain models: Transaction + IDs + flags
- [~] 1.2 Time rules + injectable clock

## Milestone 2 — Validation & Help System
- [x] 2.1 ASCII-only validator (core)
- [ ] 2.2 Help registry (single source of truth)
- [x] 2.3 Help flags support: -h / --help

## Milestone 3 — Parser & Commands
- [x] 3.1 Define command objects (AST)
- [x] 3.2 CommandParser.parse(raw) -> Command or Help/Error
- [ ] 3.3 Default month behavior contract via ExecutionContext

## Milestone 4 — Ledger Engine (Execution)
- [~] 4.1 Storage-agnostic repository interface
- [x] 4.2 Execute: add
- [x] 4.3 Execute: del (soft delete)
- [x] 4.4 Execute: list
- [~] 4.5 Execute: sum (YYYY-MM mode pending)
- [x] 4.6 Monthly summary engine (Top Bar)

## Milestone 5 — ASCII Charts
- [x] 5.1 Pie data aggregation (expense-only)
- [x] 5.2 Pie rendering: Top 6 + Others + fixed width
- [x] 5.3 Execute: pie command

## Milestone 6 — Export / Import
- [~] 6.1 JSON Schema v1 definition (doc + validator)
- [x] 6.2 Export JSON (schema v1)
- [x] 6.3 Export CSV
- [x] 6.4 Import JSON (merge)
- [x] 6.5 Import JSON (replace)
- [ ] 6.6 Round-trip tests

## Milestone 7 — Android Data Layer (Room)
- [ ] 7.1 Room schema: Entity + DAO
- [ ] 7.2 Repository mapping (Room <-> Domain)

## Milestone 8 — Android UI (Compose Terminal)
- [ ] 8.1 Top Bar UI: month navigation + summary
- [ ] 8.2 Terminal output list (vertical scroll + jump-to-bottom)
- [ ] 8.3 Horizontal scroll + wrap off (for ASCII pie)
- [ ] 8.4 Output font size control (A+/A-/A0 + persistence)
- [ ] 8.5 Input prompt + send
- [ ] 8.6 Termux-like extra keys row

## Milestone 9 — Android File I/O (Export/Import UI)
- [ ] 9.1 Export flow UI (SAF recommended)
- [ ] 9.2 Import flow UI (SAF)

## Milestone 10 — End-to-end Integration & QA
- [ ] 10.1 Wire UI -> Domain engine -> Repo
- [ ] 10.2 Error handling & stability (OutputLine contract pending)
- [ ] 10.3 Release checklist

## Milestone 11 — PWA Readiness (Design-only in v1)
- [x] 11.1 PWA parity design note (docs only)

---

## Next recommended tickets (top 5)
1. 定義 `OutputLine(kind,text)` contract，並改為 domain 錯誤回傳不拋出例外
2. 新增 `ExecutionContext(selected_month, timezone, now)` 串到 `list/sum/pie`
3. 實作 `TransactionRepository` interface + in-memory adapter
4. 補 `sum YYYY-MM` 與 round-trip tests
5. 建 Android module skeleton（ui/data/domain）

