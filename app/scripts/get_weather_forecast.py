import os
import httpx
from google.adk.tools.tool_context import ToolContext
from app.core.hubscape_adk import get_context, require_tool_privilege

@require_tool_privilege
async def get_weather_forecast(tool_context: ToolContext, location: str, days: int = 3) -> dict:
    """
    Fetches a weather forecast for the specified location for up to 3 days.

    Args:
        location: The name of the city or location (e.g. "Seattle", "London").
        days: Number of days for the forecast (default 3, max 3).
    """
    context = get_context()
    
    # Cap days at 3
    days = min(max(days, 1), 3)
    
    is_mock = os.getenv("INTEGRATION_TEST") == "TRUE"
    api_key = os.getenv("WEATHER_API_KEY")
    
    # Resolve client modality features from raw context directly
    mode = context.raw_context.get("mode") or "chat_pc"
    has_ui = context.raw_context.get("has_ui", True) if "has_ui" in context.raw_context else (mode != "sms" and mode != "voice_call")

    pref = context.get(scope="user", collection_name="user_preferences", doc_id="preferences") or {}
    unit_pref = pref.get("temp_unit", "fahrenheit")
    
    if is_mock or not api_key:
        # Mock forecast data
        forecast_rows = []
        mock_days = ["Thu", "Fri", "Sat"]
        mock_conditions = ["Cloudy", "Sunny", "Rain"]
        mock_temps_f = [("50", "68"), ("52", "70"), ("48", "65")]
        mock_temps_c = [("10", "20"), ("11", "21"), ("9", "18")]
        
        for i in range(days):
            if unit_pref == "celsius":
                temp_range = f"{mock_temps_c[i][0]} / {mock_temps_c[i][1]} °C"
            else:
                temp_range = f"{mock_temps_f[i][0]} / {mock_temps_f[i][1]} °F"
                
            forecast_rows.append({
                "date": mock_days[i],
                "condition": mock_conditions[i],
                "temp": temp_range
            })
            
        if has_ui:
            context.show_widget("weather_forecast_widget", {
                "location": location,
                "forecast_rows": forecast_rows
            })
            
        msg = f"3-Day Forecast for {location}: " + ", ".join([f"{r['date']}: {r['temp']} ({r['condition']})" for r in forecast_rows])
        return {
            "status": "success",
            "location": location,
            "forecast_rows": forecast_rows,
            "message": msg
        }

    # API call to WeatherAPI.com
    url = "https://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": api_key,
        "q": location,
        "days": days
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
        if response.status_code != 200:
            return {
                "status": "error",
                "message": f"Failed to fetch forecast from API (HTTP {response.status_code})."
            }
            
        data = response.json()
        loc_name = data["location"]["name"]
        forecast_list = data["forecast"]["forecastday"]
        
        forecast_rows = []
        for day_data in forecast_list:
            date_str = day_data["date"]
            cond_str = day_data["day"]["condition"]["text"]
            
            mintemp_c = day_data["day"]["mintemp_c"]
            maxtemp_c = day_data["day"]["maxtemp_c"]
            mintemp_f = day_data["day"]["mintemp_f"]
            maxtemp_f = day_data["day"]["maxtemp_f"]
            
            if unit_pref == "celsius":
                temp_range = f"{mintemp_c} / {maxtemp_c} °C"
            else:
                temp_range = f"{mintemp_f} / {maxtemp_f} °F"
                
            forecast_rows.append({
                "date": date_str,
                "condition": cond_str,
                "temp": temp_range
            })
            
        if has_ui:
            context.show_widget("weather_forecast_widget", {
                "location": loc_name,
                "forecast_rows": forecast_rows
            })
            
        msg = f"Forecast for {loc_name}: " + ", ".join([f"{r['date']}: {r['temp']} ({r['condition']})" for r in forecast_rows])
        return {
            "status": "success",
            "location": loc_name,
            "forecast_rows": forecast_rows,
            "message": msg
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"An error occurred while fetching forecast: {str(e)}"
        }
