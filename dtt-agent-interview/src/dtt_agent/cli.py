"""JSON Lines runner for the agent.

Usage::

    python -m dtt_agent --session-id demo < scenarios/mixed_answers.jsonl

The runner is deliberately thin and protocol-agnostic:

1. construct the agent,
2. call ``start_session()`` and print its output as one JSON line,
3. read one JSON object per line from stdin,
4. call ``process()`` for each one and print one JSON line per input line,
5. keep reading until EOF -- even after the agent reaches a terminal state, so
   that whatever it does with post-terminal events stays visible,
6. answer a malformed line with a structured ``INVALID_JSON`` line instead of
   crashing.

Blank lines are ignored. Output lines have sorted keys so two runs of the same
scenario can be compared with ``diff``.

This file already satisfies the CLI contract; you should not need to change it,
but you may if your design calls for it.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, IO, List, Optional, Sequence

from . import contracts
from .agent import DTTAgent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m dtt_agent",
        description=(
            "Run one simulated session: start a session, then feed one "
            "child-answer JSON object per stdin line."
        ),
    )
    parser.add_argument(
        "--session-id",
        default="demo",
        help="session id passed to start_session() (default: demo)",
    )
    return parser


def run(
    agent: DTTAgent,
    session_id: str,
    stream: IO[str],
    out: IO[str],
) -> List[Dict[str, Any]]:
    """Drive ``agent`` over ``stream`` and return every emitted response."""
    emitted: List[Dict[str, Any]] = []

    def emit(response: Dict[str, Any]) -> None:
        emitted.append(response)
        out.write(json.dumps(response, sort_keys=True) + "\n")
        out.flush()

    emit(agent.start_session(session_id))

    for raw_line in stream:
        line = raw_line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            emit(_invalid_json(agent, f"line is not valid JSON: {exc}"))
            continue
        if not isinstance(event, dict):
            emit(_invalid_json(agent, "line is valid JSON but not an object"))
            continue
        emit(agent.process(event))

    return emitted


def _invalid_json(agent: DTTAgent, message: str) -> Dict[str, Any]:
    return contracts.rejected_response(
        in_reply_to=None,
        code=contracts.ERROR_INVALID_JSON,
        message=message,
        state=agent.get_state(),
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    run(DTTAgent(), args.session_id, sys.stdin, sys.stdout)
    return 0


if __name__ == "__main__":  # pragma: no cover - `python -m dtt_agent.cli`
    raise SystemExit(main())
