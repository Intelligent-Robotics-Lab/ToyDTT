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

Click **Fork** in the top right to create your own copy — you'll work from your
fork, not the original. Please don't open a pull request against this
repository; you'll send us a link to your own copy at the end.

Note that **a fork of a public repository is always public**, so anyone can read
your solution. That is fine by us — if you would rather keep your work to
yourself, see [working privately](#working-privately) below.

### 2. Clone your fork

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
git remote add upstream https://github.com/Intelligent-Robotics-Lab/ToyDTT.git
```

The `upstream` remote is there in case we publish a correction while you are
working — `git fetch upstream && git merge upstream/main` picks it up.

Work on `main` or on a branch, whichever you prefer, and commit as you go. We
like seeing how the work developed.

### 3. Set up and install

```bash
cd dtt-agent-interview
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

Python 3.11 or newer. Runtime code uses the standard library only; `pytest` is
the single development dependency.

### 4. Verify it works

```bash
python -m pytest                                    # passes on the untouched starter
python -m dtt_agent --session-id demo < scenarios/mixed_answers.jsonl
```

**On Windows PowerShell**, `<` is a reserved operator and will not redirect
input. Pipe the file in instead — the runner behaves identically:

```powershell
python -m pytest
Get-Content scenarios\mixed_answers.jsonl | python -m dtt_agent --session-id demo
```

Both should work **before you write any code**. The starter agent contains no
teaching logic and no suggested protocol states — it returns structured
`NOT_IMPLEMENTED` responses, and the runner prints one JSON line per input line.
That is exactly what you should see at this point, so it is a good way to check
your setup. If either command misbehaves, fix that before going further.

### 5. Then follow this order

1. Read [`dtt-agent-interview/README.md`](dtt-agent-interview/README.md) — the
   brief: contracts, engineering requirements, deliverables, and how the work is
   evaluated. Everything below is described there in full.
2. **Research first, code second.** Find your sources and write `RESEARCH.md`
   from `RESEARCH_TEMPLATE.md`. Keep what the sources say separate from what you
   decide.
3. **Specify before you implement.** Write `PROTOCOL.md` from
   `PROTOCOL_TEMPLATE.md`: states, transitions, actions, and the rule for each
   answer value. Fill in the traceability table as you go — it is much harder to
   reconstruct afterwards.
4. **Implement** your protocol in `src/dtt_agent/`, and choose your toy lesson.
   Keep the four public methods and the CLI behaviour compatible.
5. **Test your own rules**, not just the provided contract. The public tests in
   `tests/` cover the envelope; your tests cover your protocol.
6. Fill in `AI_USE.md` from `AI_USE_TEMPLATE.md`, and update
   `dtt-agent-interview/README.md` with your architecture, assumptions, and
   tradeoffs.
7. Work through `SUBMISSION_CHECKLIST.md`, push, and send us the link.

Budget roughly **4 to 6 hours** in total, research included. A small, clearly
reasoned, well-tested protocol beats a large one. If you get stuck on an
ambiguity, make a decision, write down why, and move on — labelled assumptions
are exactly what we want to talk about in the interview.

## Working privately

Optional, and only if you would rather your solution not be public. Create an
empty **private** repository under your account, then clone this one and point
it there instead of forking:

```bash
git clone https://github.com/Intelligent-Robotics-Lab/ToyDTT.git
cd ToyDTT
git remote set-url origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

Add the person who sent you the assignment as a collaborator so we can read it,
or send a zip of the repository instead. A zip is perfectly acceptable — please
include the `.git` directory if you have one.
