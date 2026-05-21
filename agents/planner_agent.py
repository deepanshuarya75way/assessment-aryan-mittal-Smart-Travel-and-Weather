from __future__ import annotations

from typing import Any
from crewai import Agent


def create_planner_agent(llm: Any) -> Agent:

    return Agent(
        role="Senior Travel Planner",

        goal=(
            "Create a simple day-wise itinerary with main places and basic timing."
        ),

        backstory=(
            "You design short, practical travel plans with minimal details."
        ),

        tools=[],

        llm=llm,

        verbose=False,

        allow_delegation=False,

        use_system_prompt=False,

        max_iter=1
    )