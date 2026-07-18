# Demo narrative

## The one-sentence story

Hydra keeps a local MLX agent from repeating the same setup mistake: it
remembers the Mac, learns from an actual LM Studio load failure, and never
uploads secrets.

## Run it

Load a chat model in LM Studio, start its local server, then choose the proof level.

```bash
# Development: deterministic persistence simulator + real local model
./demo/run.sh

# Final recording: real HydraDB + real local model, with fallback prohibited
HYDRA_DB_API_KEY=... ./demo/run.sh --live
```

The runner discovers the first non-embedding localhost model. Override
`LOCAL_LLM_BASE_URL`, `LOCAL_LLM_MODEL`, `HYDRA_DATABASE`, or
`HYDRA_COLLECTION` when needed.

## 90-second spoken narrative

**0–10 seconds — the human problem**

“Local models are private and fast, but they repeat setup mistakes because a new
session does not know this Mac or what failed yesterday.”

**10–20 seconds — establish the baseline**

Point to `COLD BASELINE 0/3`. “The demo queries a unique, isolated Hydra
collection before ingestion. It has none of the three facts needed for a safe
recommendation: the device, the compatibility rule, or the previous failure.”

**20–40 seconds — show why Hydra is necessary**

Point to `CONTEXT LEARNING`. “The measured M4 Pro with 24 GB is personal Memory.
The MLX-VLM compatibility runbook is Knowledge. The July 14 log records two load
failures caused by KV cache quantization; that raw interaction becomes Memory
with inference enabled, so Hydra can derive a durable outcome.”

**40–52 seconds — earn trust**

Point to `EGRESS GATE`. “Local inference does not mean all data stays local.
Every write requires consent, and this credential is rejected before the Hydra
adapter is called.”

**52–70 seconds — prove persistence, not chat history**

Point to `FRESH SESSION` and `0/3 → 3/3`. “I create a new Hydra client and query
again. All three facts return across the session boundary. This is the measured
difference between a cold local model and a context-aware one.”

**70–86 seconds — the winner moment**

Point to the model response. “The actual 27B MLX model running on this Mac cites
the M4 Pro, 24 GB profile, compatibility rule, and two previous failures. It
rejects the unchanged configuration and recommends disabling KV cache
quantization.”

**86–90 seconds — close**

“Hydra remembers and relates the evidence; MLX keeps generation local; the
policy gate makes the boundary honest.”

## What each mode proves

| Claim | Lab mode | `--live` mode |
|---|---:|---:|
| Real localhost model discovery and generation | Yes | Yes |
| Memory/Knowledge/inference decisions | Yes | Yes |
| Secret blocked before adapter call | Yes | Yes |
| Fresh-session recovery and 0/3 → 3/3 benchmark | Deterministic simulator | HydraDB |
| Live HydraDB write and query | No | Yes |
| Silent fallback possible | No; mode is labeled | No; missing key is fatal |

## Recording checklist

- Keep the terminal large enough to show the mode and seven checks.
- Start the recording only after the local model and Hydra database are ready.
- Run `./demo/run.sh --live`; never record lab mode as Hydra proof.
- Show the database and collection names printed at the end, never the key.
- End on the 0/3 → 3/3 line and the grounded local response.
