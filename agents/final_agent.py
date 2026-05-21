from __future__ import annotations

from crewai import Agent


def create_final_agent(llm) -> Agent:

    return Agent(
        role="Executive Travel Editor",

        goal=(
            "Combine weather, budget, and itinerary into a simple travel plan."
        ),

        backstory=(
            "You create short, clean travel summaries without repetition."
        ),

        tools=[],

        llm=llm,

        verbose=False,

        allow_delegation=False,

        use_system_prompt=False,

        max_iter=1
    )