## 🧪 8. Verification & QA Plan

### Automated Tests
Run the project unit and integration tests using pytest:
```bash
uv run pytest tests/
```

We will also use the ADK evaluation framework to run eval case verification:
```bash
agents-cli eval generate
agents-cli eval grade
```

### Manual Verification Checklist
1. `[ ]` **Current Weather Widget Render:** In Holodeck sandbox, ask the agent for current weather in "New York" and verify the `current_weather_widget` renders with temperature, condition, humidity, and wind.
2. `[ ]` **Forecast Table Render:** Ask for the weather forecast in "London" and verify that a 3-day data table displays correct forecast columns.
3. `[ ]` **Daily Alerts Form submission:** Verify that clicking "Save Alert Setting" in the `weather_alerts_widget` correctly calls `/api/plugins/{{agent_id}}/save_alert` and stores alert parameters in the Firestore sandbox emulator.
4. `[ ]` **Incorrect Location Validation:** Verify that typing an invalid city name (e.g. "xyzabc") returns a fallback validation message asking the user to confirm the location.
5. `[ ]` **SMS Modality Fallback:** Set the sandbox client mode to `"sms"` and query the weather. Verify that the response is pure plain text (no markdown or HTML tags).
6. `[ ]` **Voice Modality Fallback:** Set the sandbox client mode to `"voice_call"` and query the weather. Verify that the response contains concise, verbally friendly statements (e.g. "seventy-two degrees" instead of "72°F").
