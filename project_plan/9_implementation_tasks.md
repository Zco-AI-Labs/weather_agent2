## 📋 9. Implementation Tasks

### Phase 1: Configuration & Metadata
- [ ] Set display name ("Weather Agent") and agent description in `app/agent.py`.
- [ ] Initialize system instructions inside the `app/SKILL.md` file detailing weather personality and modality handling.

### Phase 2: Business Logic & Tool Implementation
- [ ] Implement `app/scripts/get_current_weather.py`:
  - Fetch weather from `https://api.weatherapi.com/v1/current.json` using `httpx`.
  - Perform validation on location arguments.
  - Render `current_weather_widget` UI card when client supports visual modality (`context.client.has_ui` is true).
  - Format plain-text fallback response for SMS/Voice modalities.
- [ ] Implement `app/scripts/get_weather_forecast.py`:
  - Fetch 3-day forecast from `https://api.weatherapi.com/v1/forecast.json` using `httpx`.
  - Parse and map daily forecast data.
  - Render `weather_forecast_widget` layout.
- [ ] Implement `app/scripts/save_weather_alert.py`:
  - Save alert settings using `context.save_agent_data` to `user` scope collection `weather_alerts` with key `alert_{normalized_location}`.
- [ ] Implement `app/scripts/get_weather_alerts.py`:
  - Query all documents in user scope collection `weather_alerts` using `context.list_agent_data` and return active subscriptions.
- [ ] Register tools in `app/agent.py` under `root_agent = AdkAgent(..., tools=[...])`.
- [ ] Add sandbox secrets retrieve fallback: `await context.get_agent_secret("WEATHER_API_KEY") or os.environ.get("WEATHER_API_KEY")`.

### Phase 3: UI/Widgets Definition
- [ ] Create widget templates under `app/ui/widgets/`:
  - [NEW] `app/ui/widgets/current_weather_widget.json`
  - [NEW] `app/ui/widgets/weather_forecast_widget.json`
  - [NEW] `app/ui/widgets/weather_alerts_widget.json`
- [ ] Verify that all JSON formats align with `docs/UI_ELEMENTS.md` schemas.

### Phase 4: Verification & Testing
- [ ] Create mock API unit tests for each weather script inside the `tests/` folder.
- [ ] Verify functionality via sandbox local Holodeck by checking UI output, SMS text response, and Voice Call replies.
