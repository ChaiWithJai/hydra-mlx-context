# Verification report: local context to MLX response

**Story:** A developer approves a user preference, blocks a secret, recalls the
approved context, and gets a personalized response from a real MLX model through
LM Studio on localhost.

## Flow status

| Boundary | Status | Evidence |
|---|---:|---|
| Local server discovery | Pass | `/v1/models` returned `ternary-bonsai-27b-mlx` |
| Policy to persistence | Pass | Explicit preference classified as Memory with `infer=false` |
| Secret to policy | Pass | `api_key=...` classified `deny`; write count stayed unchanged |
| Persistence to recall | Pass | One scoped chunk returned with source ID `demo_answer_style` |
| Recall to prompt | Pass | Existing tests prove capped chunks and `untrusted-evidence` label |
| Prompt to local model | Pass | LM Studio returned a non-empty answer containing “concise” |
| Response behavior | Pass | Output followed the recalled three-bullet preference |
| HydraDB cloud | Not run | No API key was present; production adapter remains contract-tested |

## Runtime evidence

The full immutable transcript is in
[`artifacts/demo-transcript.txt`](../artifacts/demo-transcript.txt).

The observed model output was:

> 1. I will provide concise code explanations for every query.
> 2. I will strictly use exactly three short bullets per response.
> 3. I will prioritize direct solutions over lengthy discussions.

## Automated evidence

- Ruff: passed
- Pytest: 17 tests passed
- Live demo assertions: passed
- Model host restriction: only `127.0.0.1`, `localhost`, or `::1` accepted

## Remaining proof for the competition recording

Provide a dedicated HydraDB demo key, run `hydra-mlx init`, ingest the preference,
wait for indexing, and rerun recall through `HydraV2Store`. Record the returned
source ID but never show the key. Until that run exists, the project must say
“Hydra-compatible demo” rather than “live HydraDB demo.”
