from google.adk.tools.tool_context import ToolContext
from app.core.hubscape_adk import get_context, require_tool_privilege

@require_tool_privilege
async def set_temp_unit(tool_context: ToolContext, unit: str) -> dict:
    """
    Sets the preferred temperature unit for the user (celsius or fahrenheit).

    Args:
        unit: The temperature unit preference. Must be "celsius" or "fahrenheit".
    """
    context = get_context()
    
    clean_unit = unit.strip().lower()
    if clean_unit not in ["celsius", "fahrenheit"]:
        return {
            "status": "error",
            "message": "Invalid temperature unit. Please specify either 'celsius' or 'fahrenheit'."
        }
        
    pref_data = {
        "id": "preferences",
        "temp_unit": clean_unit
    }
    
    saved = context.save(
        scope="user",
        collection_name="user_preferences",
        doc_id="preferences",
        data=pref_data
    )
    
    return {
        "status": "success",
        "preferences": saved,
        "message": f"Your temperature unit preference has been set to {clean_unit}."
    }
