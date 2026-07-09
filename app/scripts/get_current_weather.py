import os
import httpx
from google.adk.tools.tool_context import ToolContext
from app.core.hubscape_adk import get_context, require_tool_privilege

@require_tool_privilege
async def get_current_weather(tool_context: ToolContext, location: str) -> dict:
    """
    Fetches the current weather conditions for a specified city or location.

    Args:
        location: The name of the city, region, or latitude/longitude coordinates (e.g. "Seattle", "London", "40.7128,-74.0060").
    """
    context = get_context()
    
    # Check if we should use mock data for testing
    is_mock = os.getenv("INTEGRATION_TEST") == "TRUE"
    api_key = os.getenv("WEATHER_API_KEY")
    
    # Resolve client modality features from raw context directly
    mode = context.raw_context.get("mode") or "chat_pc"
    has_ui = context.raw_context.get("has_ui", True) if "has_ui" in context.raw_context else (mode != "sms" and mode != "voice_call")

    # Load user preference unit if available
    pref = context.get(scope="user", collection_name="user_preferences", doc_id="preferences") or {}
    unit_pref = pref.get("temp_unit", "fahrenheit")
    
    if is_mock or not api_key:
        temp_f = 72.0
        temp_c = 22.0
        condition = "Sunny"
        humidity = 45
        wind = "8 mph NW"
        
        if unit_pref == "celsius":
            temp_str = f"{temp_c}"
            unit_str = "C"
        else:
            temp_str = f"{temp_f}"
            unit_str = "F"
            
        if has_ui:
            context.show_widget("current_weather_widget", {
                "location": location,
                "temp": temp_str,
                "unit": unit_str,
                "condition": condition,
                "humidity": str(humidity),
                "wind": wind
            })
            
        return {
            "status": "success",
            "location": location,
            "temp": temp_str,
            "unit": unit_str,
            "condition": condition,
            "humidity": humidity,
            "wind": wind,
            "message": f"Current weather in {location}: {temp_str}°{unit_str}, {condition}."
        }

    # Make outbound call to weather API
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key,
        "q": location
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
        if response.status_code != 200:
            return {
                "status": "error",
                "message": f"Failed to fetch weather data from API (HTTP {response.status_code})."
            }
            
        data = response.json()
        loc_name = data["location"]["name"]
        temp_c = data["current"]["temp_c"]
        temp_f = data["current"]["temp_f"]
        condition = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]
        wind_mph = data["current"]["wind_mph"]
        wind_dir = data["current"]["wind_dir"]
        
        if unit_pref == "celsius":
            temp_str = f"{temp_c}"
            unit_str = "C"
        else:
            temp_str = f"{temp_f}"
            unit_str = "F"
            
        if has_ui:
            context.show_widget("current_weather_widget", {
                "location": loc_name,
                "temp": temp_str,
                "unit": unit_str,
                "condition": condition,
                "humidity": str(humidity),
                "wind": f"{wind_mph} mph {wind_dir}"
            })
            
        return {
            "status": "success",
            "location": loc_name,
            "temp": temp_str,
            "unit": unit_str,
            "condition": condition,
            "humidity": humidity,
            "wind": f"{wind_mph} mph {wind_dir}",
            "message": f"Current weather in {loc_name}: {temp_str}°{unit_str}, {condition}."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"An error occurred while fetching weather: {str(e)}"
        }
