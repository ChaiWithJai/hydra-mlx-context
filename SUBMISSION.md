# Submission control center

This page is the source of truth for the HydraDB Docs Challenge submission.

## Current status

The project is built, tested, published, and proven against HydraDB. The final
challenge submission is not complete. We have not recorded or uploaded the
video. We have not opened the upstream pull request because issue 157 still
needs a maintainer acknowledgment.

The submission deadline is July 24, 2026.

## Proof links

| Item | Link | Status |
|---|---|---|
| Companion repository | [hydra-mlx-context](https://github.com/ChaiWithJai/hydra-mlx-context) | Ready |
| Live proof commit | [a32fb2e](https://github.com/ChaiWithJai/hydra-mlx-context/commit/a32fb2e) | Ready |
| CI run | [29659462705](https://github.com/ChaiWithJai/hydra-mlx-context/actions/runs/29659462705) | Passed |
| Upstream issue | [usecortex/mintlify-docs issue 157](https://github.com/usecortex/mintlify-docs/issues/157) | Waiting for acknowledgment |
| Live transcript | [artifacts/demo-transcript.txt](artifacts/demo-transcript.txt) | Ready |
| Verification report | [docs/VERIFICATION.md](docs/VERIFICATION.md) | Ready |
| Cookbook draft | [contribution/local-model-context.mdx](contribution/local-model-context.mdx) | Ready to copy upstream |
| Video | Not uploaded | Missing |
| Upstream pull request | Not opened | Blocked by acknowledgment |
| Discord post | Not posted | Waiting for pull request and video links |

## What is proven

- [x] The demo uses a HydraDB live key and does not fall back to the simulator.
- [x] A fresh collection starts with zero of the three required facts.
- [x] HydraDB stores the device Memory, compatibility Knowledge, and failure Memory.
- [x] The code uses both `infer=false` and `infer=true` for clear reasons.
- [x] The policy gate rejects a credential before any persistence call.
- [x] A fresh HydraDB client recalls all three required facts.
- [x] The measured score improves from 0/3 to 3/3.
- [x] The local `ternary-bonsai-27b-mlx` model cites the recalled facts.
- [x] The test suite passes 31 tests.
- [x] A new Python 3.11 environment installs the project and passes all checks.
- [x] GitHub CI passes on the published commit.
- [x] No HydraDB key is tracked by Git.

## What remains

### Do now while waiting for acknowledgment

- [ ] Record the video with [submission/VIDEO_SCRIPT.md](submission/VIDEO_SCRIPT.md).
- [ ] Trim pauses during Hydra indexing without changing the order of events.
- [ ] Check the video for API keys, email addresses, and private browser content.
- [ ] Upload the video as an unlisted YouTube or Loom link.
- [ ] Add the video link to this page and the prepared messages.
- [ ] Confirm the correct HydraDB Discord submission channel.

### Do after a maintainer acknowledges issue 157

- [ ] Fork `usecortex/mintlify-docs` under `ChaiWithJai`.
- [ ] Create the branch `feat/local-mlx-troubleshooter`.
- [ ] Copy the cookbook to `cookbooks/v2/local-mlx-troubleshooter.mdx`.
- [ ] Add the cookbook to the v2 cookbook list in `docs.json`.
- [ ] Run the Mintlify preview and check every link and code block.
- [ ] Scan the upstream diff for secrets and private information.
- [ ] Commit with `git commit -s` so the DCO check passes.
- [ ] Open the pull request with [submission/PR_BODY.md](submission/PR_BODY.md).
- [ ] Confirm all upstream checks pass.
- [ ] Post [submission/DISCORD_POST.md](submission/DISCORD_POST.md) in Discord.

## Recommended order

1. Record and upload the video.
2. Ask for acknowledgment with [submission/ORGANIZER_MESSAGE.md](submission/ORGANIZER_MESSAGE.md).
3. Build and verify the upstream documentation branch after acknowledgment.
4. Open the pull request.
5. Add the final pull request and video links to the Discord post.
6. Post in Discord before July 24.
7. Save screenshots of the pull request, Discord post, and video page.

## Who handles each step

Codex can prepare and verify the upstream branch after acknowledgment. Codex can
also update the pull request body and Discord post with the final links. You
need to provide or approve the final recording, choose where to upload it, and
confirm the correct Discord channel. A HydraDB maintainer needs to acknowledge
issue 157.

## Final release check

Do not call the entry submitted until every item below is complete.

- [ ] The video link opens without requiring the judge to request access.
- [ ] The public companion repository opens and its CI is green.
- [ ] The upstream pull request references issue 157.
- [ ] The pull request commit contains a valid DCO sign off.
- [ ] The upstream documentation preview renders correctly.
- [ ] The Discord post contains the project, pull request, and video links.
- [ ] The Discord post was sent before the deadline.
