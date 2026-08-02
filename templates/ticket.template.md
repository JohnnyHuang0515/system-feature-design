# {NN} — {Ticket title}

**What to build:** the end-to-end behaviour this ticket makes work, from the user's
perspective — not a layer-by-layer implementation list.

**Blocked by:** {the numbers/titles of the tickets that gate this one}
（沒有阻塞就寫 `None — can start immediately`）

**Status:** ready-for-agent

## Acceptance criteria

- [ ] {AC-X.Y 原文照抄}
- [ ] {AC-X.Y 原文照抄}

## Spec references

- FR: {FR-N}
- UF: {UF-N}
- ADR: {D-NNNN}（受哪些決策約束，無則省略）

<!--
一張票 = 一個 tracer bullet：切穿 schema / API / UI / tests 的一條窄但完整的路徑，
做完可以獨立 demo，塞得進一個全新的 context window。

不要寫檔案路徑或 code snippet — 會過期，而且會把實作 agent 指到錯的檔案。
唯一例外：prototype 產出的、比散文更精確的 decision snippet（state machine /
reducer / schema / type shape），註明出處並只留 decision-rich 的部分。
-->
