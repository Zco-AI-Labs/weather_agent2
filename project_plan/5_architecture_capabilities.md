## 🛠️ 5. Architecture & Capabilities

### System Instructions (`app/SKILL.md`)
```text
You are a highly efficient Weather Agent. Your purpose is to help users check current weather conditions, retrieve multi-day forecasts, and set up daily weather alerts for their desired locations.

Formatting Rules:
1. Always format responses clearly using standard markdown.
2. Keep conversational responses concise and friendly.
3. When rendering widgets, present them clearly to the user.
4. Ensure text-only or voice responses do not contain markdown syntax or JSON structures.
```

### Tool Implementations (`app/scripts/`)
We will implement the following Python tools inside the `app/scripts/` directory:

#### [NEW] `app/scripts/get_current_weather.py`
```python
from google.adk.tools.tool_context import ToolContext

async def get_current_weather(tool_context: ToolContext, location: str) -> dict:
    """
    Fetches the current weather conditions for a specified city or location.

    Args:
        location: The name of the city, region, or latitude/longitude coordinates (e.g. "Seattle", "London", "40.7128,-74.0060").
    """
    # Tool implementation logic...
```

#### [NEW] `app/scripts/get_weather_forecast.py`
```python
from google.adk.tools.tool_context import ToolContext

async def get_weather_forecast(tool_context: ToolContext, location: str, days: int = 3) -> dict:
    """
    Fetches a weather forecast for the specified location for up to 3 days.

    Args:
        location: The name of the city or location (e.g. "Seattle", "London").
        days: Number of days for the forecast (default 3, max 3).
    """
    # Tool implementation logic...
```

#### [NEW] `app/scripts/save_weather_alert.py`
```python
from google.adk.tools.tool_context import ToolContext

async def save_weather_alert(tool_context: ToolContext, location: str, time: str, enabled: bool = True) -> dict:
    """
    Saves or updates a recurring daily weather alert configuration for a location at a specific time.

    Args:
        location: The city name to set the alert for.
        time: The time of day to trigger the alert, in HH:MM 24-hour format (e.g., "07:00", "18:30").
        enabled: Whether the alert is active (default True).
    """
    # Tool implementation logic...
```

#### [NEW] `app/scripts/get_weather_alerts.py`
```python
from google.adk.tools.tool_context import ToolContext

async def get_weather_alerts(tool_context: ToolContext) -> dict:
    """
    Retrieves all active daily weather alerts configured for the current user.
    """
    # Tool implementation logic...
```

### 🔑 Tool Privileges Matrix
Since all actions are user-scoped, any authenticated user can invoke these tools.

| Privilege Name | Description of Granted Capabilities / Tools |
| :--- | :--- |
| `ADMIN` | Full capabilities to retrieve weather data and manage user-scoped weather alerts. |

### Model Context Protocol (MCP) & Agent-to-Agent (A2A) Connections
None. Outbound weather data queries will be made using standard async HTTP client calls (`httpx`) to the WeatherAPI.com REST API.

### Required Secrets (Agent Secrets Vault)
These secrets must be supplied to the platform Secrets Vault for production deployment.

| Secret Name | Description | Required? (True/False) |
| :--- | :--- | :--- |
| `WEATHER_API_KEY` | API Key for WeatherAPI.com used to authenticate weather data fetch requests. | True |
