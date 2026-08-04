# Submission checklist

We highly recommend you work through this before you send your submission. It takes a few minutes and
catches most of what we would look for. Don't seek the perfection. It is completely fine if you are not covering everything and do as much as you can.

## Documents

- [ ] `RESEARCH.md` exists, roughly 300–500 words.
- [ ] At least three credible sources are cited.
- [ ] At least two are peer-reviewed, university, government, or recognised
      professional sources.
- [ ] Every reference has a working URL or DOI and an access date.
- [ ] I opened every source I cite and confirmed it says what I claim.
- [ ] At least one point of variation or disagreement between sources is
      discussed.
- [ ] Decisions that are my own assumptions are labelled as assumptions, not
      presented as sourced.
- [ ] Limitations of turning a human-delivered intervention into a toy agent are
      stated, along with the note that this is a simulation and not clinical
      guidance.
- [ ] `PROTOCOL.md` exists and covers every section of the template.
- [ ] The source-to-rule traceability table is filled in, with a code location
      and a test location for each rule.
- [ ] `AI_USE.md` exists and is accurate.
- [ ] `README.md` describes setup, how to run the tests and the CLI, my
      architecture, my assumptions, and one or two tradeoffs.

## Implementation

- [ ] `start_session()`, `process()`, `get_state()`, and `reset()` all work and
      keep their signatures.
- [ ] `start_session()` returns at least one action.
- [ ] Every `protocol_state` value my agent reports appears in `PROTOCOL.md`.
- [ ] Every action `type` my agent emits appears in `PROTOCOL.md`.
- [ ] `status` is only ever `idle`, `running`, `paused`, `complete`, or
      `terminated`.
- [ ] Invalid events are rejected with a structured error and leave state
      untouched.
- [ ] An answer before `start_session()` is rejected.
- [ ] A mismatched `session_id` is rejected.
- [ ] A duplicate `event_id` does not advance the protocol twice.
- [ ] `reset()` clears the session, the state, and the processed-event history.
- [ ] The demonstration session has a documented bounded path to `complete`,
      `paused`, or `terminated`.
- [ ] `process()` never raises — it returns a structured rejection instead.
- [ ] My lesson content is finite, reproducible, and non-sensitive.

## Behaviour

- [ ] `python -m pytest` passes from a clean checkout.
- [ ] The public contract tests are unmodified, or every change to them is
      explained in `README.md`.
- [ ] I added my own protocol tests, covering correct, incorrect, and absent
      answers, repeated unsuccessful answers, terminal behaviour, duplicates,
      invalid input, and `reset()`.
- [ ] Every provided scenario runs through the CLI without crashing:
      ```bash
      for f in scenarios/*.jsonl; do python -m dtt_agent --session-id demo --input "$f" > /dev/null; done
      ```
      ```powershell
      Get-ChildItem scenarios\*.jsonl | ForEach-Object { python -m dtt_agent --session-id demo --input $_ | Out-Null }
      ```
- [ ] Running the same scenario twice produces byte-identical output.
- [ ] Feeding 100 valid answers terminates promptly and does not grow memory
      without bound.

## Hygiene

- [ ] Runtime code imports only the Python standard library.
- [ ] No networking, external services, or LLM calls; no audio, video, or
      sensor input; no machine learning; no database, web server, or GUI.
- [ ] No credentials, API keys, or tokens anywhere in the repository.
- [ ] No virtual environment, `__pycache__`, `.pytest_cache`, or build artefacts
      committed.
- [ ] The project runs on a machine other than mine (no absolute paths, no
      OS-specific assumptions).

## Interview readiness

- [ ] I can walk through my state machine from memory.
- [ ] I can point from any rule in `PROTOCOL.md` to the code that implements it
      and the test that covers it.
- [ ] I can explain which of my decisions came from sources and which are mine.
- [ ] I can replay one provided scenario and explain each transition.
- [ ] I can discuss how I would make one of my policies configurable without
      changing today's default behaviour.
