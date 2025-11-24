"""Simple agent-system example for S0711CITY1_BOT.

This file demonstrates a minimal, extensible agent pattern:
- `Agent` objects perform small tasks and report results.
- `AgentManager` schedules and runs agents sequentially (can be extended to concurrency).

Use this as a pattern for creating background workers or testable agent modules.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Callable, List, Dict, Any


@dataclass
class TaskResult:
    name: str
    success: bool
    data: Dict[str, Any]


class Agent:
    """Base agent. Subclass and override `run()` to implement behaviour."""

    def __init__(self, name: str, handler: Callable[[], Dict[str, Any]]):
        self.name = name
        self.handler = handler

    def run(self) -> TaskResult:
        start = time.time()
        try:
            data = self.handler()
            elapsed = time.time() - start
            return TaskResult(name=self.name, success=True, data={"elapsed": elapsed, **data})
        except Exception as e:
            elapsed = time.time() - start
            return TaskResult(name=self.name, success=False, data={"error": str(e), "elapsed": elapsed})


class AgentManager:
    """Simple manager that runs agents in order and aggregates results."""

    def __init__(self):
        self.agents: List[Agent] = []

    def register(self, agent: Agent) -> None:
        self.agents.append(agent)

    def run_all(self) -> List[TaskResult]:
        results: List[TaskResult] = []
        for ag in self.agents:
            print(f"[agent] running: {ag.name}")
            result = ag.run()
            print(f"[agent] result: {ag.name} success={result.success} data={result.data}")
            results.append(result)
        return results


def example_handler_ping() -> Dict[str, Any]:
    # lightweight check: simulate work and return a small payload
    time.sleep(0.2)
    return {"msg": "pong"}


def example_handler_config_check() -> Dict[str, Any]:
    # read a few important env vars and return a safe summary
    bot_token_present = bool(os.getenv("BOT_TOKEN"))
    webhook_url = os.getenv("WEBHOOK_URL") or "<not-set>"
    return {"bot_token_present": bot_token_present, "webhook_url": webhook_url}


def main() -> int:
    manager = AgentManager()

    # Register two simple agents as examples
    manager.register(Agent("ping-agent", example_handler_ping))
    manager.register(Agent("config-check", example_handler_config_check))

    results = manager.run_all()

    # Return non-zero if any agent failed
    failed = [r for r in results if not r.success]
    if failed:
        print(f"{len(failed)} agent(s) failed")
        return 2
    print("All agents finished successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
