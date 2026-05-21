from __future__ import annotations

from typing import Sequence
from crewai import Agent

from tools.cost_calculator import TripCostEstimatorTool


def create_budget_agent(
    llm,
    tools: Sequence[TripCostEstimatorTool],
) -> Agent:

    return Agent(
        role="Travel Finance Analyst",

        goal=(
            "Estimate travel cost (hotel, food, transport). "
            "Compare with budget and give simple savings tips."
        ),

        backstory=(
            "You estimate travel costs and suggest budget-friendly options."
        ),

        tools=list(tools),

        llm=llm,

        verbose=False,

        allow_delegation=False,

        use_system_prompt=False,

        max_iter=1
    )