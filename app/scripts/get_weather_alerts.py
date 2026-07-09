from google.adk.tools.tool_context import ToolContext
from app.core.hubscape_adk import get_context, require_tool_privilege

@require_tool_privilege
async def get_weather_alerts(tool_context: ToolContext) -> dict:
    """
    Retrieves all active daily weather alerts configured for the current user.
    """
    context = get_context()
    
    # Retrieve all alerts from scoped collection
    alerts = context.list(
        scope="user",
        collection_name="weather_alerts"
    )
    
    # Filter or return all alerts
    return {
        "status": "success",
        "alerts": alerts,
        "message": f"Successfully retrieved {len(alerts)} weather alerts."
    }
