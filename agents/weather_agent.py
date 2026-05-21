from __future__ import annotations

from typing import Sequence, Any

from crewai import Agent
from tools.weather_tool import OpenWeatherMapTool


def create_weather_agent(
    llm: Any,
    tools: Sequence[OpenWeatherMapTool],
) -> Agent:

    return Agent(
        role="Lead Meteorologist & Packing Strategist",

        goal=(
            "Get weather for destination and give short travel advice."
        ),

        backstory=(
            "You convert weather data into short travel recommendations."
        ),

        tools=list(tools),

        llm=llm,

        verbose=False,

        allow_delegation=False,

        use_system_prompt=False,

        max_iter=1
    )