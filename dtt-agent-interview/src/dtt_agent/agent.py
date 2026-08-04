"""The agent you are asked to build.

The class below is deliberately empty of decision logic. It starts, it accepts
answers, it reports state -- and it currently refuses to do anything else,
returning a structured ``NOT_IMPLEMENTED`` rejection so the CLI and the public
contract tests run before you write a line of your own code.

What to do with an answer, how many attempts a task gets, what the agent says
and when, when a session is finished: none of that is decided here, and none of
it is hinted at anywhere in this package. Those rules come out of your research
(``RESEARCH.md``) and your specification (``PROTOCOL.md``), and this class is
where you implement them.

You are free to restructure: add modules, dataclasses, enums, a state machine,
a configuration file for your lesson content. The only fixed points are the four
public methods below, the event schema in ``contracts.py``, and the response
envelope the CLI prints.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from . import contracts


class DTTAgent:
    """A deterministic, stateful agent driven by child-answer events."""

    def __init__(self) -> None:
        # --- Fields backing the required state snapshot -----------------
        # `protocol_state` is a label of your choosing; the scaffolding never
        # reads it. The rest are reported verbatim in every response.
        self._session_id: Optional[str] = None
        self._status: str = contracts.STATUS_IDLE
        self._trial_number: Optional[int] = None
        self._completed_trials: int = 0
        self._protocol_state: Optional[str] = None

        # --- Processed-event history ------------------------------------
        # Duplicate `event_id` values must be handled idempotently, so the
        # agent has to remember what it already answered. Keep whatever shape
        # you need; `reset()` must clear it.
        self._responses_by_event_id: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # Public interface -- these four signatures must stay compatible.
    # ------------------------------------------------------------------

    def start_session(self, session_id: str) -> dict:
        """Start a new simulated teaching session and return the first agent output.

        Requirements that hold whatever protocol you design:

        * the response uses ``in_reply_to: None``;
        * an accepted start returns at least one action;
        * the state snapshot reflects where the session actually is.

        TODO(candidate): replace the rejection below with your own start logic.
        """
        return contracts.rejected_response(
            in_reply_to=None,
            code=contracts.ERROR_NOT_IMPLEMENTED,
            message="start_session() has not been implemented yet.",
            state=self.get_state(),
        )

    def process(self, event: dict) -> dict:
        """Process one structured child-answer event and return one agent output.

        Software rules to honour (these are contract rules, not teaching rules):

        * validate the event -- ``contracts.validate_event_shape`` covers the
          schema; answers arriving before ``start_session()`` and answers
          carrying the wrong ``session_id`` depend on your state, so they are
          checked here;
        * a rejected event must leave the agent's state exactly as it was;
        * a repeated ``event_id`` must not advance anything a second time --
          returning the original response is the recommended behaviour;
        * the same session replayed with the same answers must produce the same
          outputs, byte for byte;
        * never raise out of this method; return a structured rejection instead.

        TODO(candidate): replace the rejection below with your own logic.
        """
        in_reply_to = event.get("event_id") if isinstance(event, dict) else None
        if not isinstance(in_reply_to, str):
            in_reply_to = None
        return contracts.rejected_response(
            in_reply_to=in_reply_to,
            code=contracts.ERROR_NOT_IMPLEMENTED,
            message="process() has not been implemented yet.",
            state=self.get_state(),
        )

    def get_state(self) -> dict:
        """Return a JSON-serializable snapshot of current agent state.

        The snapshot returned here must be the same snapshot embedded in every
        response envelope.
        """
        return contracts.make_state(
            session_id=self._session_id,
            status=self._status,
            trial_number=self._trial_number,
            completed_trials=self._completed_trials,
            protocol_state=self._protocol_state,
        )

    def reset(self) -> None:
        """Clear the session, state, and processed-event history.

        After ``reset()`` the agent must be indistinguishable from a freshly
        constructed one. If you add state of your own, clear it here too.
        """
        self._session_id = None
        self._status = contracts.STATUS_IDLE
        self._trial_number = None
        self._completed_trials = 0
        self._protocol_state = None
        self._responses_by_event_id.clear()
