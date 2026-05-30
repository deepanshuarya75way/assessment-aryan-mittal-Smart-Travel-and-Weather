# AI Multi-Agent Travel Planner

A **Streamlit** app that plans trips using **CrewAI** multi-agent collaboration, **LangChain** `ChatGroq` (Groq LLM), and live **OpenWeatherMap** forecasts.

## Features

- **User inputs**: destination, budget, days, travel style
- **Real weather**: current conditions + 5-day / 3-hour forecast (summarized per day)
- **Multi-agent pipeline** (sequential): Weather → Budget → Planner → Final editor
- **Budget tool**: heuristic per-day cost buckets + trip total range (the LLM interprets and optimizes)
- **Streamlit UI**: wide layout, loading spinner, structured Markdown output, sidebar help

## Project structure

```
travel_planner_ai/
├── agents/
│   ├── weather_agent.py
│   ├── budget_agent.py
│   ├── planner_agent.py
│   └── final_agent.py
├── tools/
│   ├── weather_tool.py
│   └── cost_calculator.py
├── tasks/
│   └── travel_tasks.py
├── config/
│   └── settings.py
├── app.py
├── requirements.txt
├── .env.example
└── README.md
```

## Python version

CrewAI currently publishes wheels for **Python 3.10 through 3.13**. If you are on **Python 3.14+**, create a **3.13** (or 3.12) virtual environment first; otherwise `pip install crewai` may fail.

## Setup

### 1) Create a virtual environment (recommended)

```bash
cd travel_planner_ai
python -m venv .venv
```

Activate:

- **Windows (PowerShell)**: `.\.venv\Scripts\Activate.ps1`
- **macOS/Linux**: `source .venv/bin/activate`

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure API keys

Create a `.env` file in `travel_planner_ai/` (you can start from `.env.example`) and fill in keys:

- **Groq**: `GROQ_API_KEY` from the Groq console
- **OpenWeatherMap**: `WEATHER_API_KEY` from OpenWeatherMap

### 4) Run the app

```bash
streamlit run app.py
```

## API integration steps

### Groq (LLM)

This project uses LangChain’s Groq chat model:

- Package: `langchain-groq`
- Class: `ChatGroq`
- Model default: `llama3-70b-8192` (configured in `config/settings.py`)

### OpenWeatherMap (Weather)

The weather tool performs:

1. **Geocoding**: `GET https://api.openweathermap.org/geo/1.0/direct?q=<city>&appid=<key>`
2. **Current weather**: `GET https://api.openweathermap.org/data/2.5/weather?lat=...&lon=...&units=metric&appid=<key>`
3. **Forecast**: `GET https://api.openweathermap.org/data/2.5/forecast?lat=...&lon=...&units=metric&appid=<key>`

Network calls use **httpx** with **tenacity** retries for transient transport/timeouts.

## Example output shape

The final agent is instructed to output Markdown with headings like:

- `## Executive summary`
- `## Weather insights & best windows`
- `## Packing checklist`
- `## Budget breakdown`
- `## Daily itinerary`
- `## Local food recommendations`
- `## Transport suggestions`
- `## Travel tips`
- `## Emergency essentials`

Exact wording will vary by destination and model output.

## Architecture notes (how the pieces fit)

### How CrewAI agents “communicate”

CrewAI collaboration here is **sequential** (`Process.sequential`):

- Each **Task** completes and produces an output artifact.
- Downstream tasks include `context=[...]` so CrewAI **injects prior task outputs into the prompt** of the next agent.
- This is not free-form chat between agents; it’s a **handoff chain** where later agents must stay consistent with earlier specialist outputs.

### How LangChain integrates with Groq

`langchain_groq.ChatGroq` implements LangChain’s chat-model interface and calls Groq’s HTTP API using `GROQ_API_KEY`. CrewAI agents accept this object as `llm=...`, so tool calling / reasoning is executed by the same LangChain-compatible stack CrewAI expects.

### How weather data is processed

`tools/weather_tool.py` fetches JSON from OpenWeatherMap, then **compresses** it into:

- a compact “current conditions” section
- a **day-bucketed** forecast summary (rolled up from 3-hour samples)

That text is what the Weather Agent sees, reducing hallucinated numbers.

### How itinerary generation works

The Planner Agent does **not** call external POI APIs in this repo. It uses:

- the user’s constraints (days/style/budget)
- **context** from Weather + Budget tasks

…to generate a plausible schedule. Treat venue names as **suggestions** and verify hours, tickets, and closures before booking.

## Troubleshooting

- **Import errors**: run Streamlit with `app.py` path so the folder bootstrap in `app.py` can add this directory to `sys.path`.
- **Ambiguous destination**: use `City,CountryCode` (example: `Portland,US` vs `Portland,OR` is still ambiguous—prefer `Portland,US` plus state context in the destination string if needed).
- **Model unavailable**: update `groq_model` in `config/settings.py` to a currently supported Groq model name.

## License

Use and modify freely for learning and product prototyping.
