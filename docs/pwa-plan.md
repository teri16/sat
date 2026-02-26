# PWA Plan (Design-only, v1 phase)

## Purpose
本文件描述與 Android parity 的設計對照，作為 v2 PWA 開發前置規劃。

## Parity Mapping
- Domain logic: 共用（命令解析、統計、ASCII pie、JSON schema）
- UI layer: Web terminal view（`<pre>`/monospace layout）
- Storage layer: IndexedDB（替代 Android Room）

## UI Notes
- 終端輸出：垂直捲動 + 水平捲動 + nowrap
- 字級控制：A+ / A- / A0（pinch optional）
- Output contract：保留 kind（INFO/OK/WARN/ERR）擴充 rich output

## Storage Notes
- IndexedDB schema 對齊 Transaction domain fields
- 保留 deleted 旗標（soft delete）
- 匯出/匯入沿用 JSON schema v1

## Risks
- Browser storage quota 與資料清除風險
- 行動裝置橫向捲動與字級可讀性

## Acceptance (Design phase)
- 有清楚 parity 表
- 無平台路徑耦合（schema 不包含 Android /Download）
- 可直接轉為 implementation tickets

