## Description

This pull request adds a v2 cookbook for a local MLX troubleshooter. The guide
shows how to combine a measured device profile, a shared compatibility runbook,
and a previous load failure without implying that HydraDB persistence stays on
the Mac.

The companion implementation proves the complete flow against HydraDB and a
local MLX model. A fresh collection starts at 0/3 required facts. After approved
context ingestion, a fresh HydraDB client recalls all three facts and scores
3/3. The local model uses those facts to reject an incompatible KV cache
configuration. The implementation also blocks credential shaped content before
any persistence call.

Companion repository:
https://github.com/ChaiWithJai/hydra-mlx-context

Live proof and CI:
https://github.com/ChaiWithJai/hydra-mlx-context/actions/runs/29659462705

Demo video:
ADD_VIDEO_URL

## Related Issue

Closes #157

## Type of Change

- [ ] Content fix (typo, broken link, incorrect info)
- [x] New content (guide, tutorial, API docs)
- [x] Structural change (navigation, layout)
- [ ] CI/Build

## Checklist

Check each item only after completing it on the upstream branch.

- [ ] I have read the [CONTRIBUTING](../CONTRIBUTING.md) guidelines
- [ ] This PR is linked to an issue
- [ ] My commits are signed off (`git commit -s`) per the DCO
- [ ] `mintlify dev` renders my changes correctly
- [ ] I have not committed any secrets or credentials
- [ ] No internal system details are exposed in the content

## Verification

- [x] The page uses the HydraDB v2 SDK surface.
- [x] Memory and Knowledge examples use one consistent database and collection.
- [x] The guide explains `infer=true` and `infer=false`.
- [x] The guide states that HydraDB persistence is remote.
- [x] The guide sends model generation only to a loopback address.
- [x] The guide treats recalled context as bounded evidence.
- [x] The companion demo passed with a fresh HydraDB client and no simulator fallback.
