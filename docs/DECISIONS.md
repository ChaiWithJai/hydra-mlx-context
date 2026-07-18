# Context decision guide

## Memory vs. Knowledge

Ask: **who should be able to recall this later?**

| Input | Store | Scope | Example |
|---|---|---|---|
| Personal preference | Memory | User collection | “Prefer terse answers.” |
| Conversation outcome | Memory | User or session collection | “Chose SQLite for the prototype.” |
| Raw interaction signal | Memory | User collection | Repeated requests for Python examples |
| Project README or API docs | Knowledge | Project collection | `README.md` |
| Shared runbook | Knowledge | Team collection | Release procedure |
| Secret, credential, private advisory note | Neither | Local only | API key or confidential feedback |

Do not use metadata filters as an isolation boundary. HydraDB v2 treats the
database as the hard boundary and a collection as the logical partition.

## `infer` decision

| Input shape | `infer` | Reason |
|---|---:|---|
| Raw, consented dialogue with an implicit preference | `true` | HydraDB derives the durable signal |
| Consented behavioral events | `true` | The useful fact is not written directly |
| Explicit fact already distilled by the app | `false` | Store exactly what the app supplied |
| Decision record that must remain verbatim | `false` | Avoid semantic reinterpretation |
| Ambiguous or sensitive input | Do not send | Clarify or retain locally |

`custom_instructions` belongs only with `infer: true`. It narrows extraction; it
does not make sensitive input safe to send.

## Query mode

| Need | Query shape |
|---|---|
| Fast project RAG | `type="knowledge"`, `mode="fast"`, 5–10 results |
| Personalization only | `type="memory"`, same user collection |
| Personalized grounded answer | `type="all"`, same scoped collection, `mode="thinking"` |
| Exact error code or symbol | `query_by="text"`, `operator="phrase"` |

For a single-developer local assistant, keeping both project Knowledge and user
Memory in the same user-controlled collection makes `type="all"` predictable.
For a multi-user product, plan shared and private scopes explicitly; do not rely
on a single convenience query until the cross-scope behavior is verified.
