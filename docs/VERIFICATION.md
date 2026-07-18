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
| HydraDB cloud | Pass | Strict live run used database `hydra_mlx_context` and an isolated collection |
| No-fallback guarantee | Pass | Run declared `MODE: LIVE · NO FALLBACK`; missing key is fatal |

## Observed local-model output

> Based on the device profile and compatibility runbook, you should **not**
> retry the same configuration.
>
> The failure occurred on your Apple M4 Pro with 24 GB of unified memory because
> the batched vision path does not support KV cache quantization. The runbook
> explicitly states that you must **disable KV cache quantization** before
> retrying, or alternatively use a compatible non-batched path.

The measured hardware and two original failure timestamps are preserved in the
[sanitized evidence capture](../artifacts/host-and-failure-evidence.txt).

## Automated evidence

- `ruff check .`: passed
- `pytest`: 31 tests passed
- strict real-HydraDB and real-local-model demo assertions: passed
- non-loopback model URLs: rejected
- denied content reaching a writable store: rejected
- incomplete context benchmark: reports the missing fact labels
- focused probes: prevent a similar runbook chunk from masking a missing failure Memory

## Live proof command and observed result

The implementation now has a strict proof command:

```bash
HYDRA_DB_API_KEY=... ./demo/run.sh --live
```

The command cannot silently substitute the lab store. On July 18, 2026 it:

1. queried a unique collection and established a 0/3 cold baseline;
2. ingested the device Memory, compatibility Knowledge, and inferred failure Memory;
3. rejected a credential-shaped write before the Hydra adapter;
4. observed Hydra indexing states and polled focused queries until each source's
   required fact was searchable;
5. created a fresh SDK client and scored 3/3; and
6. passed the exact recalled chunks to the localhost model.

The final line was:

```text
PROVEN LIVE: HydraDB database=hydra_mlx_context collection=local_mlx_troubleshooting_b5f37384db; fresh client recall; localhost generation; no simulator fallback.
```

The collection identifier is evidence, not a credential. No API key appears in
the transcript or repository.
