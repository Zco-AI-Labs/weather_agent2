from google.adk.tools.tool_context import ToolContext
from app.core.hubscape_adk import get_context, require_tool_privilege

@require_tool_privilege
async def save_weather_alert(tool_context: ToolContext, location: str, time: str, enabled: bool = True) -> dict:
    """
    Saves or updates a recurring daily weather alert configuration for a location at a specific time.

    Args:
        location: The city name to set the alert for.
        time: The time of day to trigger the alert, in HH:MM 24-hour format (e.g., "07:00", "18:30").
        enabled: Whether the alert is active (default True).
    """
    context = get_context()
    
    # Normalize location for doc ID
    normalized_loc = location.strip().lower().replace(" ", "_")
    doc_id = f"alert_{normalized_loc}"
    
    alert_data = {
        "id": doc_id,
        "location": location,
        "time": time,
        "enabled": enabled
    }
    
    # Save using context helper
    saved = context.save(
        scope="user",
        collection_name="weather_alerts",
        doc_id=doc_id,
        data=alert_data
    )
    
    status_msg = "enabled" if enabled else "disabled"
    return {
        "status": "success",
        "doc_id": doc_id,
        "alert": saved,
        "message": f"Daily weather alert for {location} at {time} has been {status_msg}."
    }
