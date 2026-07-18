# Competition plan

## Verified brief

The HydraDB × Docs hackathon is virtual, runs July 17–24, 2026, and offers ten
$50 awards. Participants must fork `usecortex/mintlify-docs`, use Mintlify,
submit a pull request by July 24, and share it in the HydraDB Discord channel.
The prompt is to pick a confusing developer journey and fix it completely.

## Chosen journey

**Persistent context for a local Apple Silicon model, with an explicit privacy
boundary and a clear Memory/Knowledge/`infer` decision path.**

This is stronger than a broad “MLX integration” page because it produces a
single demonstrable outcome and resolves the exact conceptual choices named in
the event brief.

## Judging thesis

1. **Completeness:** decision tree, architecture, working reference code, tests,
   failure modes, and a PR-ready Mintlify guide.
2. **Timeliness:** local inference is a fast-growing workflow, but durable memory
   remains fragmented across runners.
3. **Truthfulness:** the guide makes the remote context boundary explicit instead
   of using “local AI” as a blanket privacy claim.
4. **Documentation leverage:** it translates HydraDB’s primitives into an
   end-to-end developer journey and highlights the current v1/v2 docs mismatch.
5. **Ecosystem reach:** one OpenAI-compatible local adapter supports LM Studio and
   other MLX servers without coupling the guide to one GUI.

## Competitive frame

| Alternative | Strength | Gap this entry targets |
|---|---|---|
| Local runner chat history | Simple and private | Usually siloed, flat, runner-specific |
| Local vector store | Fully local and controllable | Developer owns extraction, graphing, lifecycle, and sync |
| Generic cloud memory SDK | Fast integration | Often obscures local-vs-remote data boundary |
| HydraDB + this guide | Persistent graph-aware context with local generation | Requires explicit egress and scope discipline |

We should not claim HydraDB “replaces” every local vector database. The winning
claim is narrower: Hydra provides managed persistent context while MLX provides
local inference, and the policy gate makes that composition legible.

## Delivery sequence

1. Validate the v2 SDK example against a test key or maintainer confirmation.
2. Open a Hydra docs feature-request issue and obtain acknowledgment, as required
   by `CONTRIBUTING.md`.
3. Fork `usecortex/mintlify-docs`; add the cookbook and navigation entry.
4. Run Mintlify preview, link checks, repository checks, and DCO sign-off.
5. Record a 60–90 second demo: remember preference → ask local model → show
   personalized answer → show a denied secret.
6. Submit the PR and post it in the event Discord channel before July 24.

## Acceptance checklist

- [ ] A clean install works on Apple Silicon with Python 3.11+.
- [ ] LM Studio localhost completion is demonstrated.
- [ ] An MLX-native server configuration is documented.
- [ ] Memory and Knowledge each have one successful ingestion example.
- [ ] `infer: true` and `infer: false` each have one justified example.
- [ ] A likely secret is blocked before a network call.
- [ ] Recalled context is bounded and marked untrusted.
- [ ] No private advisory content or implied endorsements are present.
- [ ] The Mintlify page renders and links only to current v2 primitives.
- [ ] The upstream issue, PR, DCO sign-off, and Discord submission are complete.
