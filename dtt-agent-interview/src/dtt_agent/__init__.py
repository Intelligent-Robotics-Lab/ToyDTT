"""Starter package for the simulated teaching-agent assignment.

Public surface:

* :class:`dtt_agent.agent.DTTAgent` -- the class you implement.
* :mod:`dtt_agent.contracts` -- provided event/response contracts.
* :mod:`dtt_agent.cli` -- the provided JSON Lines runner.
"""

from .agent import DTTAgent

__all__ = ["DTTAgent"]
__version__ = "0.1.0"
