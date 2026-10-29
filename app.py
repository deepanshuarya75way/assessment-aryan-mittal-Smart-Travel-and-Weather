"""
Streamlit UI for the AI Multi-Agent Travel Planner.

Run from this folder (recommended):
    streamlit run app.py

Or from a parent directory:
    streamlit run travel_planner_ai/app.py
"""

from __future__ import annotations

import sys
import traceback
from pathlib import Path

# Ensure `travel_planner_ai/` is on sys.path so `agents`, `tools`, `config`, `tasks` resolve.
_APP_DIR = Path(__file__).resolve().parent
if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))

import streamlit as st  # noqa: E402

from config.settings import get_settings  # noqa: E402
from tasks.travel_tasks import TripInputs, run_trip_planning_crew  # noqa: E402


def _init_page() -> None:
    st.set_page_config(
        page_title="AI Travel Planner",
        page_icon="✈️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
          .block-container { padding-top: 1.2rem; }
          div.stButton > button:first-child {
            background: linear-gradient(90deg, #2563eb, #7c3aed);
            color: white;
            border: 0;
            font-weight: 600;
          }
          div.stButton > button:first-child:hover { filter: brightness(1.05); }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _sidebar_help() -> None:
    with st.sidebar:
        st.header("How this works")
        st.markdown(
            """
            This app runs a **CrewAI** crew in **sequential** order:

            1. **Weather Agent** calls OpenWeatherMap (real forecast data).
            2. **Budget Agent** uses a deterministic cost estimator tool + reasoning.
            3. **Planner Agent** builds a day-by-day itinerary using the prior context.
            4. **Final Agent** merges everything into one polished Markdown report.

            **API keys**: create a `.env` beside `app.py` (see `.env.example`).
            """
        )
        st.divider()
        st.caption("Tip: for ambiguous cities, use `City,CC` (e.g. `Springfield,US`).")


def _travel_styles() -> list[str]:
    return [
        "luxury",
        "budget",
        "adventure",
        "family",
        "solo",
        "business",
        "romantic",
    ]


def main() -> None:
    _init_page()

    # CrewAI does not yet support Python 3.14+ on many releases; fail fast with a clear message.
    if sys.version_info >= (3, 14):
        st.error(
            "Python 3.14+ is not supported by CrewAI yet. "
            "Please create a virtual environment using Python 3.10–3.13, then reinstall requirements."
        )
        st.stop()

    _sidebar_help()

    st.title("AI Multi-Agent Travel Planner")
    st.caption("CrewAI + LangChain (Groq) + OpenWeatherMap — modular, production-style layout.")

    col_a, col_b = st.columns((2, 1), gap="large")

    with col_a:
        st.subheader("Trip inputs")
        destination = st.text_input(
            "Destination",
            placeholder="e.g. Lisbon,PT or Kyoto",
            help="City name; add a country code if the name is ambiguous.",
        )
        budget = st.number_input(
            "Total trip budget (your currency)",
            min_value=0.0,
            value=1500.0,
            step=50.0,
        )
        days = st.number_input(
            "Number of days",
            min_value=1,
            max_value=60,
            value=4,
            step=1,
            help="The cost estimator supports up to 60 days.",
        )
        travel_style = st.selectbox("Travel style", _travel_styles(), index=1)

    with col_b:
        st.subheader("What you will get")
        st.markdown(
            """
            - Weather briefing + best windows (from live data)
            - Packing checklist + emergency essentials
            - Budget breakdown + tradeoffs
            - Daily itinerary + timing blocks
            - Food + local transport ideas
            - Travel tips (general guidance)
            """
        )

    generate = st.button("Generate plan", type="primary", use_container_width=True)

    if "last_report" not in st.session_state:
        st.session_state.last_report = ""

    if generate:
        dest = (destination or "").strip()
        if not dest:
            st.error("Please enter a destination.")
            return

        try:
            settings = get_settings()
        except ValueError as exc:
            st.error(str(exc))
            st.info("Copy `.env.example` to `.env` and add your API keys.")
            return

        trip = TripInputs(
            destination=dest,
            budget=float(budget),
            days=int(days),
            travel_style=str(travel_style),
        )

        with st.spinner("Agents are collaborating (this can take a minute)…"):
            try:
                report = run_trip_planning_crew(settings, trip)
                st.session_state.last_report = report
            except Exception:  # noqa: BLE001 — show full traceback in expander for debugging
                st.error("Planning failed. See details below.")
                with st.expander("Error details"):
                    st.code(traceback.format_exc())
                return

        st.success("Plan generated.")

    report = st.session_state.get("last_report") or ""
    if report:
        st.divider()
        st.subheader("Your travel packet")
        st.markdown(report)


if __name__ == "__main__":
    main()


    
import requests
import stramlit as st
API_URL = "https://127.0.0.1:8000"

if s.button("Check Backend"):
    try:
        response = request.get(f'{API_URL}/health,timeout=9')
        response.raise_for_status()
        st.sucess("Backend connected")
        st.json(response.json())
    except request.RequestException as e:
        st.error(f"Backend connection failed:{e}")