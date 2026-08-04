# ToyDTT

Research Discrete Trial Training (DTT) from credible sources, turn that research
into an explicit computational protocol, and implement the protocol as a
deterministic, stateful Python agent driven by simulated child-answer events.

The assignment lives in **[`dtt-agent-interview/`](dtt-agent-interview/)** —
start with its [`README.md`](dtt-agent-interview/README.md).

You are given an interface, a JSON event schema, a generic response envelope,
input-only scenario files, a command-line runner, and public contract tests. You
are **not** given a DTT protocol, a state machine, a prompting strategy, a retry
count, a reinforcement rule, an error-correction procedure, or a mastery rule.
Deriving those from your own research, documenting where each one came from, and
defending them is the assignment.

This is a simulation exercise. It is not a clinical system and not clinical
guidance.

## Quick start
 
### 1. Fork the repo
Click **Fork** in the top right to create your own copy — you'll work from your fork, not the original.
 
### 2. Clone your fork
 
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>/dtt-agent-interview
```
 
### 3. Set up and install
 
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```
 
### 4. Verify it works
 
```bash
python -m pytest                                    # passes on the untouched starter
python -m dtt_agent --session-id demo < scenarios/mixed_answers.jsonl
```

The starter agent contains no teaching logic and no suggested protocol states.
It returns structured `NOT_IMPLEMENTED` responses, so the runner and the public
tests work before you write anything — which makes them a good way to check your
setup first.

## What to read, in order

1. [`dtt-agent-interview/README.md`](dtt-agent-interview/README.md) — the brief:
   contracts, requirements, deliverables, and how the work is evaluated.
2. `RESEARCH_TEMPLATE.md` and `PROTOCOL_TEMPLATE.md` — the two written
   deliverables, and the structure we expect from them.
3. `AI_USE_TEMPLATE.md` — AI tools are allowed, with disclosure.
4. `SUBMISSION_CHECKLIST.md` — work through it before you send anything.
