"""
Heuristic cost estimation tool.

This does not call external pricing APIs; it produces reasonable ranges
so the Budget Agent can reason within the user's stated budget.
"""

from __future__ import annotations

import json
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field, field_validator


class CostEstimatorInput(BaseModel):
    destination: str = Field(description="Trip destination city/region.")
    days: int = Field(description="Trip length in days", ge=1, le=60)

    travel_style: str = Field(
        description="luxury, budget, adventure, family, solo, business, romantic"
    )

    total_budget: float = Field(
        description="Total trip budget",
        ge=0
    )

    @field_validator("travel_style")
    @classmethod
    def normalize_style(cls, v: str):
        return (v or "").strip().lower()


def _style_multipliers(style: str):

    table = {
        "luxury": {
            "hotel":420,
            "food":140,
            "transport":90,
            "activities":160
        },

        "budget":{
            "hotel":70,
            "food":35,
            "transport":25,
            "activities":40
        },

        "adventure":{
            "hotel":110,
            "food":55,
            "transport":60,
            "activities":120
        },

        "family":{
            "hotel":160,
            "food":75,
            "transport":45,
            "activities":90
        },

        "solo":{
            "hotel":120,
            "food":60,
            "transport":40,
            "activities":70
        },

        "business":{
            "hotel":200,
            "food":80,
            "transport":55,
            "activities":40
        },

        "romantic":{
            "hotel":220,
            "food":110,
            "transport":50,
            "activities":100
        }
    }

    return table.get(style, table["budget"])


class TripCostEstimatorTool(BaseTool):

    name: str = "trip_cost_estimator"

    description: str = (
        "Estimate trip cost based on destination, days, style and budget."
    )

    args_schema: Type[BaseModel] = CostEstimatorInput

    def _run(
        self,
        destination: str,
        days: int,
        travel_style: str,
        total_budget: float
    ) -> str:

        style = travel_style.lower()

        mult = _style_multipliers(style)

        dest = destination.lower()

        index = 1.0

        high_cost = [
            "tokyo",
            "london",
            "paris",
            "new york",
            "singapore"
        ]

        low_cost = [
            "kolkata",
            "hanoi",
            "bali",
            "cairo"
        ]

        if any(x in dest for x in high_cost):
            index = 1.15

        elif any(x in dest for x in low_cost):
            index = 0.90

        daily = {
            k: round(v*index,2)
            for k,v in mult.items()
        }

        daily_total = sum(daily.values())

        trip_total = daily_total * days

        low = round(trip_total*0.75,2)
        high = round(trip_total*1.35,2)

        result = {
            "destination":destination,
            "days":days,
            "travel_style":style,
            "daily_costs":daily,
            "trip_range":{
                "low":low,
                "mid":round(trip_total,2),
                "high":high
            },
            "user_budget":total_budget
        }

        return json.dumps(result, indent=2)


def build_cost_tool():
    return TripCostEstimatorTool()