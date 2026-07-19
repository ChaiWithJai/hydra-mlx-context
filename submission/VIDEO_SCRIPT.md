# Video script and shot list

## Recording setup

- Use a terminal window with large text.
- Load `ternary-bonsai-27b-mlx` in LM Studio.
- Start the LM Studio local server.
- Keep the HydraDB dashboard and `.env` out of view.
- Close notifications and unrelated windows.
- Use `./demo/run.sh --live`.
- Record at 1080p or higher.
- Keep the finished video between 60 and 90 seconds after editing.

Hydra indexing can take several minutes. Record the complete run, then shorten
the waiting period in the edit. Keep the status changes in their original
order. Do not replace the output or claim that indexing was instant.

## Spoken script

### 0 to 8 seconds

"A local model starts every new session without knowing this Mac or what failed
yesterday. This demo shows how HydraDB stops it from repeating the same setup
mistake."

Show the project name and `MODE: LIVE · NO FALLBACK`.

### 8 to 18 seconds

"The model is a 27 billion parameter MLX model running through LM Studio on
localhost. The isolated Hydra collection starts with none of the three facts it
needs, so the cold score is zero out of three."

Show the local model line and the cold baseline.

### 18 to 36 seconds

"We store the measured M4 Pro and 24 GB profile as explicit Memory. We store the
shared compatibility rule as Knowledge. We let Hydra infer a durable Memory
from the earlier load failure."

Show the context learning line. If useful, place the three labels on screen.

### 36 to 45 seconds

"Local generation does not mean every part of the system stays local. This
policy gate stops a credential before the code can send it to HydraDB."

Show the egress gate result.

### 45 to 62 seconds

"Hydra processes each source in the background. The demo waits until three
focused searches recover the device, rule, and earlier failure. It then creates
a fresh Hydra client so chat history cannot explain the result."

Show a short section of the indexing states, followed by the fresh session
result and the 0/3 to 3/3 score.

### 62 to 80 seconds

"The local model now rejects the unchanged configuration. It cites the M4 Pro,
24 GB of memory, and the unsupported KV cache setting, then recommends disabling
KV cache quantization."

Show the model answer.

### 80 to 90 seconds

"HydraDB keeps the approved evidence across sessions. MLX keeps generation on
the Mac. The policy gate makes the network boundary clear."

End on `DEMO RESULT: PASS` and the live proof line.

## Edit check

- [ ] The first ten seconds state the problem.
- [ ] The cold 0/3 score is readable.
- [ ] The three context types are understandable.
- [ ] The credential denial is visible.
- [ ] The fresh client and 3/3 score are readable.
- [ ] The local model answer is readable.
- [ ] The final proof line is visible.
- [ ] No credential, email address, or private log appears.
- [ ] Captions match the spoken words.
- [ ] The video link works in a signed out browser window.

