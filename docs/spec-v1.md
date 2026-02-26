# Terminal Ledger App — Spec v1 (Current Domain Baseline)

## Goal
建立一個 **UI-independent** 的記帳核心（Domain Layer），讓 Android 與未來 PWA 能共用命令解析、統計、圖表與匯出格式。

## Command Set
- add `<amount>` `<category>` `[note]`
- list `[today|7d|month|YYYY-MM]`
- sum `[today|7d|month|category]`
- del `<id>`
- pie `[YYYY-MM]`
- export `json|csv`
- import `<merge|replace>` `<json_payload>`
- help / -h / --help / `<cmd> -h`

## Core Rules
- ASCII-only：command keyword 與 category 必須 ASCII。
- Timezone-aware：使用 service timezone（預設 Asia/Taipei）。
- Soft delete：`del` 僅標記 deleted。
- Pie：僅統計支出（amount < 0），Top 6 + Others。

## Data Model
Transaction fields:
- id
- amount
- category
- note
- occurred_at
- created_at
- deleted

## JSON Schema v1
Envelope fields:
- schema_version
- timezone
- currency
- transactions[]

Transaction export fields:
- amount
- category
- note
- occurred_at
- created_at
- deleted

## Current Non-goals
- Android Compose UI implementation
- Room repository implementation
- PWA runtime implementation

