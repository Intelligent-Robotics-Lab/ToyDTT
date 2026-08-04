# PROTOCOL.md (template)

Copy this file to `PROTOCOL.md` and fill it in. Delete the guidance text as you
go.

`RESEARCH.md` says what the literature contains. **This** document is the
specification your code implements: complete enough that another engineer could
reimplement your agent from it and get the same behaviour, without reading your
code and without asking you a question.

Anything your agent does that is not in here is undocumented behaviour.
Anything in here that your agent does not do is a bug.

---

## 1. Toy learning objective

The lesson you chose, what it teaches, and how many items it contains. State
where the content lives (configuration file or code) and why.

Note explicitly that the lesson is a demonstration and is not claimed to be
clinically appropriate for any real learner.

## 2. Session and trial structure

How a session is built out of trials. What "one trial" means in your design,
and how a trial begins and ends.

## 3. Agent states

Every `protocol_state` value your agent can report, with a one-line meaning for
each. Also state which of `idle`, `running`, `paused`, `complete`, `terminated`
you use for `status`, and when.

| `protocol_state` | Meaning | `status` reported alongside |
| --- | --- | --- |
|  |  |  |

## 4. Allowed transitions

Every legal transition, with what triggers it. A table or a diagram is fine —
an ASCII or Mermaid diagram plus a table works well.

| From | Answer / trigger | To | Actions emitted |
| --- | --- | --- | --- |
|  |  |  |  |

Say what happens to an answer that arrives in a state where it is not expected.

## 5. Action vocabulary

Every action `type` your agent emits, what it means, what `text` carries, and
what keys appear in `data`. This is the taxonomy you are defining; it needs to
be stable and documented.

| Action `type` | Meaning | `text` | `data` keys |
| --- | --- | --- | --- |
|  |  |  |  |

## 6. Handling each answer

State the rule for each of the three answer values, in each state where it can
arrive:

- `correct`
- `incorrect`
- `no_response`

Be explicit about whether `incorrect` and `no_response` are treated the same. If
they are, say why; if not, say why not.

## 7. Prompting strategy

What a prompt is in your agent, when one is delivered, whether prompting changes
across attempts or trials, and how (or whether) prompting fades.

## 8. Error-correction strategy

What happens after an unsuccessful attempt, and when the agent stops
re-attempting an item.

## 9. Reinforcement strategy

When reinforcement is delivered, whether it differs by how the answer was
achieved, and whether it changes over the session.

## 10. Trial completion rules

What ends a trial, and what outcome values a completed trial can carry.

## 11. Session completion, pause, and termination

The conditions for reaching `complete`, `paused`, or `terminated` (whichever
your design uses), and what the agent does with events that arrive afterwards.

## 12. Data recorded per trial

The record your agent keeps for each trial, field by field, and where it is
exposed (state snapshot, action `data`, or both).

## 13. Repeated incorrect or absent answers

Your rule for a run of unsuccessful answers, including a run that spans several
trials. What changes, and after how many?

## 14. Safety bound

The explicit bound that guarantees a session cannot run forever, and where it
is enforced in code. State what happens when the bound is hit.

## 15. Assumptions and exclusions

**Assumptions** — decisions you made that your sources do not settle. One line
each, with your reasoning. These are expected; hiding them is the problem.

**Exclusions** — parts of real DTT you deliberately left out, and why.

## 16. Source-to-rule traceability

One row per protocol rule. A rule may be source-supported, an explicit
engineering assumption, or both — but every rule must appear.

| Protocol rule | Source support | Applicant assumption | Code location | Test location |
| --- | --- | --- | --- | --- |
|  | `[1] §…` or `none` | yes / no + one-line reason | `src/…py:NN` | `tests/…py::test_…` |
