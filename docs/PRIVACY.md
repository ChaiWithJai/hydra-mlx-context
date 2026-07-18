# Privacy and trust contract

## The honest boundary

“Runs a model locally” is not the same as “all data stays local.” In this design:

- prompts and generation go to a loopback MLX/LM Studio server;
- recalled context travels from HydraDB to the local process;
- only writes explicitly approved with `--allow-egress` travel to HydraDB;
- likely secrets and private advisory material are denied before any write call.

## Data classes

| Class | Default | Example |
|---|---|---|
| Public project information | Ask / allow | Public README |
| Device-specific fact | Ask / allow as Memory | Approved chip and RAM profile |
| Shared project knowledge | Ask / allow as Knowledge | MLX-VLM compatibility runbook |
| Runtime outcome | Ask / summarize as Memory | Consented load-failure result |
| Credential or token | Deny | `sk-...`, private key |
| Private advisory note | Deny | Unpublished reviewer feedback |
| Captured conversation | Deny unless deliberately summarized | Raw transcript |

The scanner is a guardrail, not a proof of safety. Human consent remains the
authorization boundary.

## Advisory and attribution policy

Private advisory guides, unpublished feedback, and internal names must not be
committed. Public figures or communities may be used internally as design-review
personas, but the public repository must not imply that they:

- advised this project;
- endorsed it;
- reviewed the implementation; or
- are associated with the submission.

Any named attribution requires a public source or direct permission. Popularity
claims such as model download counts require a dated, reproducible source and
must not be converted into implied user endorsement.

## Repository controls

- `private/`, `private-*.md`, and `captures/` are gitignored.
- `.env` is gitignored; `.env.example` contains no credentials.
- tests cover common secret patterns.
- the CLI does not accept file uploads in the first release.
- no telemetry or cloud-model fallback is implemented.
