# Demo narrative

## The one-sentence story

A local MLX model remembers how the user wants coding answers, rejects a secret
before persistence, recalls the approved preference as untrusted evidence, and
uses it to produce a personalized response without calling a cloud model.

## Run it

Load a chat model in LM Studio, start its local server, then run:

```bash
./demo/run.sh
```

The runner discovers the first non-embedding model from the localhost `/models`
endpoint. Override either value when needed:

```bash
LOCAL_LLM_BASE_URL=http://127.0.0.1:8080/v1 \
LOCAL_LLM_MODEL=your-model-id \
./demo/run.sh
```

## 90-second spoken narrative

**0–12 seconds — the problem**

“Local models give us private, low-latency inference, but they forget everything
when the session ends. Adding cloud memory can quietly break the privacy promise.”

**12–25 seconds — the architecture**

“Hydra MLX Context separates those concerns. MLX or LM Studio generates on this
Mac. A policy gate decides what may become Hydra Memory or Knowledge. Recalled
content comes back inside a bounded, explicitly untrusted context block.”

**25–42 seconds — the correct memory decision**

Point to `[2/5]`. “This preference is about one user, so it is Memory. It is
already an explicit fact, so `infer` is false. We do not ask Hydra to reinterpret
something we already know.”

**42–55 seconds — the trust moment**

Point to `[3/5]`. “Now I try a credential-shaped value. It is denied before the
persistence adapter is called. The write counter does not change. Local inference
is not used as an excuse to obscure remote data movement.”

**55–75 seconds — recall and generation**

Point to `[4/5]` and the model output. “The context store returns one scoped
preference. The prompt builder labels it untrusted evidence. The actual MLX model
running in LM Studio uses that preference and answers concisely in three bullets.”

**75–90 seconds — why Hydra**

“The demo store is deterministic because this machine has no Hydra key configured.
The production adapter is already wired to HydraDB v2’s database, context ingestion,
and unified query APIs. Add the key and the persistence boundary swaps in without
changing the model or prompt pipeline. That is the developer journey this guide fixes.”

## What the proof establishes

| Boundary | Evidence |
|---|---|
| Local server is real | `/v1/models` returns the loaded MLX model and chat completion succeeds |
| Memory decision works | Explicit preference becomes Memory with `infer=false` |
| Secret gate works | Credential is denied before the store write counter changes |
| Recall contract works | The persisted preference returns through `ContextStore.recall` |
| Prompt boundary works | Context is bounded and labeled `untrusted-evidence` |
| Generation works | The localhost model’s output reflects the recalled preference |
| Hydra SDK contract works | Adapter tests use the installed HydraDB 2.x response fields |

## Honest limitation

This proof does not claim a live HydraDB cloud write when `HYDRA_DB_API_KEY` is
absent. The demo uses a deterministic in-memory implementation of the exact same
`ContextStore` interface. A live submission recording should rerun with a dedicated
demo key and show the Hydra source ID and successful recall without exposing the key.
