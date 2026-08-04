# Take-Home Assignment: Research and Build a DTT Agent

Welcome, and thank you for your interest in the position.

This assignment asks you to do two things that professional research-software
work always puts side by side:

1. **Research** a procedure — Discrete Trial Training (DTT) — from credible
   sources, and say clearly what the sources establish and what you decided
   yourself.
2. **Implement** that procedure as a small, deterministic, well-tested Python
   agent.

We deliberately do **not** give you the procedure. Finding it, turning it into
an explicit computational specification, and defending that specification is the
assignment. Two strong submissions may differ from each other; that is expected
and fine.

> **This is a simulation exercise.** It is not a clinical system, it is not
> clinical guidance, and nothing you build here should be described as suitable
> for use with a real learner.

---

## 1. What you are building

A `DTTAgent` that runs one simulated teaching session.

The agent is driven entirely by structured JSON events. Each event says only
what the simulated child's answer was — `correct`, `incorrect`, or
`no_response`. The answers arrive **already classified**. There is no audio, no
video, no text to match, and nothing to recognise or predict.

For every answer, your agent returns one JSON response containing:

- the **actions** it takes (what the agent does next — you define the vocabulary),
- a **state snapshot** (where the session now stands).

The interesting question is the one this repository refuses to answer for you:
*given this answer, in this situation, what should a DTT agent do, and why does
your research support that?*

## 2. What we give you, and what you create

**Given to you (in this repository)**

- the `DTTAgent` method signatures (`src/dtt_agent/agent.py`)
- the child-answer input schema and the response envelope (`src/dtt_agent/contracts.py`)
- a working, protocol-agnostic CLI runner (`src/dtt_agent/cli.py`)
- six input-only scenario files (`scenarios/`)
- public contract tests (`tests/test_public_contract.py`)
- templates for your written deliverables

**Created by you**

- `RESEARCH.md` — what DTT is, from real sources
- `PROTOCOL.md` — your operational specification, traced back to those sources
- a toy learning objective and its content (lesson configuration)
- the agent's state model, action vocabulary, and decision rules
- your handling of correct, incorrect, and absent answers
- your prompting, error-handling, reinforcement, progression and
  session-completion decisions
- tests for the protocol you specified
- `AI_USE.md`
- a short update to this README describing your design (see §11)

The starter `DTTAgent` contains **no** teaching logic and **no** suggested
states. That is on purpose. Do not read the absence of a hint as a trick; there
simply is no intended answer hidden in the scaffolding.

## 3. Expected effort

About **4 to 6 hours**, including the research and writing. We would much rather
see a small, clearly reasoned, well-tested protocol than a large one.

A **45-minute technical conversation** follows, in which you will walk us
through your sources, your specification, your code, and one live change to the
requirements.

## 4. Setup

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS or Linux
source .venv/bin/activate

python -m pip install -e ".[dev]"
python -m pytest
python -m dtt_agent --session-id demo < scenarios/mixed_answers.jsonl
```

In **PowerShell**, `<` is a reserved operator and does not redirect input. Pipe
the scenario in instead — this is equivalent everywhere in this document:

```powershell
Get-Content scenarios\mixed_answers.jsonl | python -m dtt_agent --session-id demo
```

Python **3.11 or newer**. Runtime code uses the **standard library only**;
`pytest` is the one development dependency. The public tests pass against the
untouched skeleton, so you can verify your setup before writing anything.

## 5. The interface

```python
class DTTAgent:
    def start_session(self, session_id: str) -> dict:
        """Start a new simulated teaching session and return the first agent output."""

    def process(self, event: dict) -> dict:
        """Process one structured child-answer event and return one agent output."""

    def get_state(self) -> dict:
        """Return a JSON-serializable snapshot of current agent state."""

    def reset(self) -> None:
        """Clear the session, state, and processed-event history."""
```

Add whatever else you need — modules, dataclasses, enums, a state machine, a
lesson configuration file. Reorganise freely. These four public methods and the
CLI behaviour must keep working.

## 6. Input contract: child-answer events

`process()` receives child-answer events and nothing else.

```json
{
  "event_id": "evt-001",
  "type": "child_response",
  "session_id": "session-001",
  "answer": "correct"
}
```

`answer` is one of exactly three values:

```text
correct
incorrect
no_response
```

### Validation rules

These are **software-contract** rules. They are not DTT rules, and they tell you
nothing about the procedure.

- `event_id`, `type`, and `session_id` must be non-empty strings.
- `type` must equal `child_response`.
- `answer` must be one of the three allowed strings (exact match — `"CORRECT"`
  is invalid).
- An answer arriving before `start_session()` must be rejected.
- An answer whose `session_id` does not match the running session must be rejected.
- An invalid event must not mutate protocol state.
- A duplicate `event_id` must be handled idempotently. Returning the original
  response is the recommended behaviour.

`contracts.validate_event_shape()` covers the schema-level checks for you. The
rules that depend on the agent's own state are yours to implement.

## 7. Output contract: the response envelope

### Accepted

```json
{
  "in_reply_to": "evt-001",
  "accepted": true,
  "actions": [
    {
      "type": "candidate_defined_action",
      "text": "Optional agent-facing or child-facing text.",
      "data": {}
    }
  ],
  "state": {
    "session_id": "session-001",
    "status": "running",
    "trial_number": 1,
    "completed_trials": 0,
    "protocol_state": "candidate_defined_state"
  }
}
```

### Rejected

```json
{
  "in_reply_to": "evt-001",
  "accepted": false,
  "actions": [],
  "error": {
    "code": "INVALID_EVENT",
    "message": "Human-readable explanation."
  },
  "state": {
    "session_id": "session-001",
    "status": "running",
    "trial_number": 1,
    "completed_trials": 0,
    "protocol_state": "candidate_defined_state"
  }
}
```

### Rules

- Every output must be JSON serializable.
- `actions` must be a list.
- Every action must have a non-empty `type` string; `text` is a string or
  `null`; `data` is an object.
- **You** define and document the action taxonomy.
- **You** define and document the `protocol_state` values.
- `status` must be one of `idle`, `running`, `paused`, `complete`, `terminated`.
  Which of those your protocol actually uses is your decision.
- `trial_number` is an integer or `null`; `completed_trials` is a non-negative
  integer.
- `start_session()` uses `in_reply_to: null`.

`contracts.describe_response_violations()` will tell you when an envelope you
built breaks one of these rules — useful in your own tests.

## 8. Engineering requirements

Independent of whichever protocol you design:

1. `start_session()` returns at least one structured action.
2. Every valid child answer produces a deterministic response.
3. The state snapshot reflects the agent's current protocol position.
4. Replaying the same session with the same answer sequence produces the same
   outputs.
5. Invalid input never corrupts state.
6. A duplicate event never advances the protocol twice.
7. `reset()` returns the agent to a clean idle state.
8. Your demonstration session has a **documented bounded path** to `complete`,
   `paused`, or `terminated` — a session must not be able to run forever.
9. Feeding up to 100 valid answers must not loop forever or grow memory without
   bound.
10. No networking, external services, or LLM calls; no audio, video, or sensor
    input; no machine learning; no database, web server, or GUI. None of them
    are needed, and adding them counts against the submission.

## 9. The toy lesson

Define one simple, non-sensitive demonstration lesson — colour identification,
shape or symbol matching, or another small discrete-answer task. We do not
supply lesson content; choosing something finite and reproducible is part of the
exercise.

Storing the lesson in a JSON or YAML configuration file is preferred over
hard-coding it in Python, but either is acceptable if you explain the choice.

Do not claim the lesson is clinically appropriate for any real child.

## 10. Scenarios and the CLI

```bash
python -m dtt_agent --session-id demo < scenarios/mixed_answers.jsonl
```

```powershell
# PowerShell equivalent
Get-Content scenarios\mixed_answers.jsonl | python -m dtt_agent --session-id demo
```

The runner constructs the agent, calls `start_session("demo")`, prints that
output as one JSON line, then prints one JSON line per input line until EOF.
It keeps reading after the agent reaches a terminal state, so you can see what
your agent does with events that arrive too late. Blank lines are ignored, and a
malformed line produces a structured `INVALID_JSON` line rather than a crash.

Provided scenarios (**inputs only — no expected outputs**):

| File | Contents |
| --- | --- |
| `scenarios/all_correct.jsonl` | correct answers only |
| `scenarios/mixed_answers.jsonl` | a mixture of all three answer values |
| `scenarios/repeated_incorrect.jsonl` | a long run of incorrect answers |
| `scenarios/repeated_no_response.jsonl` | a long run of absent answers |
| `scenarios/duplicate_event.jsonl` | repeated `event_id` values, including one repeat with reordered keys |
| `scenarios/invalid_values.jsonl` | schema violations, a session mismatch, two unparseable lines |

The scenarios deliberately do **not** tell you which event belongs to a first
attempt, a prompted attempt, a new trial, or anything else. Your state machine
decides that. A scenario may contain more answers than your session needs —
what happens to the extra ones is a design decision you should document.

## 11. What to submit

Your fork or copy of this repository — see the [quick
start](../README.md#quick-start) in the top-level README — or an archive of it,
containing:

1. **`RESEARCH.md`** — roughly 800–1,500 words. Start from
   `RESEARCH_TEMPLATE.md`.
2. **`PROTOCOL.md`** — your operational specification, including the
   source-to-rule traceability table. Start from `PROTOCOL_TEMPLATE.md`.
3. **Your implementation**, including your lesson content.
4. **Your tests**, alongside the provided public tests. `python -m pytest` must
   pass.
5. **`AI_USE.md`** — from `AI_USE_TEMPLATE.md`.
6. **An updated `README.md`** with: how to run everything, a short description
   of your architecture, your key assumptions, and one or two tradeoffs you
   weighed.

No credentials, API keys, virtual environments, or unrelated files. Please work
through `SUBMISSION_CHECKLIST.md` before you send it.

## 12. Research expectations

Use real sources and read them. At least three credible sources, of which at
least two are peer-reviewed, university, government, or recognised professional
sources. Give working URLs or DOIs and the date you accessed each one.

We do not provide a starting bibliography — finding and judging sources is part
of what we are assessing.

You will find genuine variation between sources on how DTT is delivered. Say so.
Where you had to decide something the sources do not settle, label it plainly as
your own engineering assumption. An explicit, defensible assumption is a good
answer. A rule presented as sourced when it is not is a serious problem.

## 13. Using AI tools

AI tools are allowed. If you use them, submit `AI_USE.md` describing which tools
you used, the important prompts or tasks you delegated, which generated code you
kept, and how you verified it.

You remain responsible for every source, statement, design choice, and line of
code in your submission. Invented citations, or an inability to explain your own
submission in the interview, are serious concerns. Using AI well is not held
against you; not understanding what you submitted is.

## 14. How we evaluate

| Area | Points |
| --- | ---: |
| Research quality | 25 |
| Protocol formalization | 25 |
| Implementation quality | 25 |
| Testing and robustness | 15 |
| Communication and interview defense | 10 |

A polished implementation of a weakly researched or undocumented protocol will
not score well. Neither will strong research with an implementation that does
not match it. We are looking for the line running from *source* to *rule* to
*code* to *test* — and for you to be able to walk us along it.

Good luck, and enjoy the problem.
