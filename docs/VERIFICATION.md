# Verification report: cold local model to learned troubleshooter

**Story:** A local MLX agent starts without the facts required to recommend a
safe model configuration. After approved context is persisted, a fresh session
recalls the measured device profile, compatibility runbook, and prior load
failure, then produces a grounded answer without sending generation to a cloud model.

## Verified on this machine

| Boundary | Status | Evidence |
|---|---:|---|
| Local server discovery | Pass | `/v1/models` returned `ternary-bonsai-27b-mlx` |
| Cold context baseline | Pass | 0/3 required troubleshooting facts available |
| Memory decision | Pass | Measured M4 Pro / 24 GB profile stored with `infer=false` |
| Knowledge decision | Pass | MLX-VLM compatibility runbook stored as Knowledge |
| Learning decision | Pass | Twice-observed July 14 load failure classified as Memory with `infer=true` |
| Secret to policy | Pass | `api_key=...` denied; write count unchanged |
| Fresh context session | Pass | New store object recovered three chunks |
| Context benchmark | Pass | Required facts improved from 0/3 to 3/3 |
| Prompt boundary | Pass | Context capped and labeled `untrusted-evidence` |
| Local response | Pass | Real model cited M4 Pro, 24 GB, and KV cache facts |
| HydraDB cloud | Not run | No key is configured on this machine |

## Observed local-model output

> No, you should not retry the same configuration.
>
> You are using an Apple **M4 Pro with 24 GB** of unified memory. The batched
> vision path does not support **KV cache quantization**, and this model has
> already failed to load twice due to the same conflict. Disable KV cache
> quantization or use a compatible non-batched vision path.

The measured hardware and two original failure timestamps are preserved in the
[sanitized evidence capture](../artifacts/host-and-failure-evidence.txt).

## Automated evidence

- `ruff check .`: passed
- `pytest`: 29 tests passed
- real local-model demo assertions: passed
- non-loopback model URLs: rejected
- denied content reaching a writable store: rejected
- incomplete context benchmark: reports the missing fact labels

## Remaining external proof

The implementation now has a strict proof command:

```bash
HYDRA_DB_API_KEY=... ./demo/run.sh --live
```

The command cannot silently substitute the lab store. It initializes HydraDB,
queries a unique collection for the 0/3 baseline, ingests all three approved
context classes, creates a new SDK client, polls until the complete 3/3 fact set
is queryable, and then calls the local model with those exact retrieved chunks.
The final competition recording is not complete until that command passes with
a dedicated demo key.
