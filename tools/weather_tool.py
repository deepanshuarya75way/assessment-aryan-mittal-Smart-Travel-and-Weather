"""
OpenWeatherMap tool for CrewAI agents
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Optional, Type
from urllib.parse import quote

import httpx
from pydantic import BaseModel, Field
from crewai.tools import BaseTool   # CHANGED

from config.settings import Settings, get_settings


class WeatherInput(BaseModel):
    city: str = Field(
        description="City name optionally with country code, example: Paris,FR"
    )


def _utc_now_iso():
    return datetime.now(timezone.utc).replace(
        microsecond=0
    ).isoformat()


def _fetch_weather_bundle_sync(
    city: str,
    settings: Settings
) -> dict[str, Any]:

    key = settings.weather_api_key
    timeout = settings.weather_timeout_s

    geo_url = (
        "https://api.openweathermap.org/geo/1.0/direct"
        f"?q={quote(city)}&limit=1&appid={key}"
    )

    with httpx.Client(timeout=timeout) as client:

        geo_resp = client.get(geo_url)
        geo_resp.raise_for_status()

        geo = geo_resp.json()

        if not geo:
            raise ValueError(
                f"No city found for {city}"
            )

        lat = geo[0]["lat"]
        lon = geo[0]["lon"]

        name = geo[0]["name"]
        country = geo[0].get("country", "")

        current_url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&units=metric&appid={key}"
        )

        forecast_url = (
            "https://api.openweathermap.org/data/2.5/forecast"
            f"?lat={lat}&lon={lon}&units=metric&appid={key}"
        )

        current = client.get(current_url)
        current.raise_for_status()

        forecast = client.get(forecast_url)
        forecast.raise_for_status()

    return {
        "resolved_query":
            f"{name}, {country}",

        "current":
            current.json(),

        "forecast":
            forecast.json()
    }


def _summarize_forecast(forecast):

    items = forecast.get("list", [])

    by_day = defaultdict(list)

    for item in items:

        day = item["dt_txt"].split(" ")[0]
        by_day[day].append(item)

    result = []

    for day, samples in list(by_day.items())[:5]:

        temps = [
            x["main"]["temp"]
            for x in samples
        ]

        result.append(
            f"{day}: "
            f"{min(temps):.1f}°C"
            f" - "
            f"{max(temps):.1f}°C"
        )

    return "\n".join(result)


class OpenWeatherMapTool(BaseTool):

    name: str = "openweather_forecast"

    description: str = (
        "Fetches current weather and forecast"
    )

    args_schema: Type[BaseModel] = WeatherInput

    settings: Optional[Settings] = None

    def _run(self, city: str) -> str:

        settings = self.settings or get_settings()

        try:

            data = _fetch_weather_bundle_sync(
                city,
                settings
            )

            current = data["current"]

            weather = f"""
Place: {data['resolved_query']}

Current temperature:
{current['main']['temp']}°C

Humidity:
{current['main']['humidity']}%

Conditions:
{current['weather'][0]['description']}

Forecast:
{_summarize_forecast(data['forecast'])}

Time:
{_utc_now_iso()}
"""

            return weather

        except Exception as e:
            return f"Weather error: {str(e)}"


def build_weather_tool(
    settings=None
):
    return OpenWeatherMapTool(
        settings=settings
    )