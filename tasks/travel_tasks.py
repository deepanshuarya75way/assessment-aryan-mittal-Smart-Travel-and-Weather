from __future__ import annotations

from dataclasses import dataclass
import time
import random

from crewai import Crew, Process, Task, LLM

from agents.budget_agent import create_budget_agent
from agents.final_agent import create_final_agent
from agents.planner_agent import create_planner_agent
from agents.weather_agent import create_weather_agent

from tools.cost_calculator import build_cost_tool
from tools.weather_tool import build_weather_tool


@dataclass(frozen=True)
class TripInputs:
    destination: str
    budget: float
    days: int
    travel_style: str


# -------------------------
# LLM
# -------------------------
def build_llm(settings):

    return LLM(
        model="groq/llama-3.1-8b-instant",
        api_key=settings.groq_api_key,
        temperature=0.2,
        max_tokens=400,   # increased for stability
        stream=False
    )


# -------------------------
# CREW
# -------------------------
def build_crew(settings):

    llm = build_llm(settings)

    weather_agent = create_weather_agent(
        llm,
        [build_weather_tool(settings)]
    )

    budget_agent = create_budget_agent(
        llm,
        [build_cost_tool()]
    )

    planner_agent = create_planner_agent(llm)

    final_agent = create_final_agent(llm)

    # WEATHER
    weather_task = Task(
        description="""
Get weather for {destination}.

Return ONLY:
- temperature
- rain chance
- 1 packing tip
""",
        expected_output="Concise weather report",
        agent=weather_agent
    )

    # BUDGET
    budget_task = Task(
        description="""
Estimate trip cost.

Destination: {destination}
Days: {days}
Budget: {budget}

Return ONLY:
- estimated total cost
- over or under budget
- 1 saving tip
""",
        expected_output="Concise budget report",
        agent=budget_agent
    )

    # ITINERARY
    planner_task = Task(
        description="""
Create a simple itinerary for {destination} for {days} days.

Rules:
- maximum 3 places per day
- concise format
- no explanations
""",
        expected_output="Short itinerary",
        agent=planner_agent
    )

    # FINAL REPORT
    final_task = Task(
        description="""
Combine all previous task outputs into ONE clean travel plan.

Rules:
- maximum 200 words
- avoid repetition
- clear formatting
""",
        expected_output="Complete travel summary",
        agent=final_agent
    )

    return Crew(
        agents=[
            weather_agent,
            budget_agent,
            planner_agent,
            final_agent
        ],
        tasks=[
            weather_task,
            budget_task,
            planner_task,
            final_task
        ],
        process=Process.sequential,
        memory=False,
        verbose=True
    )


# -------------------------
# RUN CREW
# -------------------------
def run_trip_planning_crew(settings, trip):

    crew = build_crew(settings)

    for attempt in range(3):

        try:

            result = crew.kickoff(
                inputs={
                    "destination": trip.destination,
                    "budget": trip.budget,
                    "days": trip.days,
                    "travel_style": trip.travel_style
                }
            )

            # ---- SAFE RESULT HANDLING ----
            if result is None:
                raise ValueError("Crew returned None")

            result_text = str(result).strip()

            if not result_text:
                raise ValueError("Crew returned empty response")

            if result_text.lower() == "none":
                raise ValueError("LLM returned literal None")

            return result_text

        except Exception as e:

            error_text = str(e)

            # Retry for transient failures
            retry_errors = [
                "RateLimitError",
                "None or empty",
                "Invalid response from LLM call",
                "timeout",
            ]

            if any(err.lower() in error_text.lower() for err in retry_errors):

                sleep_time = (2 ** attempt) + random.uniform(1, 2)
                time.sleep(sleep_time)
                continue

            return f"Trip planning failed:\n\n{error_text}"

    return (
        "Trip planning failed after multiple retries. "
        "The model may be overloaded right now."
    )