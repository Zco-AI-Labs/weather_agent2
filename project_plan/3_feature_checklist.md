## 📂 3. Feature Checklist & Interaction Modes

### Feature 1: Current Weather Inquiry
*   **Description:** Allows users to query the current weather condition, temperature, wind speed, humidity, and location metadata.
*   **Visual Interaction Mode:**
    *   *Trigger:* User types "What's the weather like in New York?" or clicks a "Check Weather" button.
    *   *UI Rendered:* `current_weather_widget` containing weather condition icons, temperature text, humidity bar, and location details.
    *   *Form Actions:* Button to "Add to Saved Locations" or "Set Alert".
*   **Non-Visual Interaction Mode (SMS/Voice Fallback):**
    *   *SMS Transcript Flow:* "Current weather in New York: 72°F (22°C), Sunny. Humidity: 45%. Wind: 8 mph from NW."
    *   *Voice/Phone Flow:* "In New York, it is currently seventy-two degrees and sunny with a humidity of forty-five percent and wind from the northwest at eight miles per hour."
    *   *Natural Language Parameters Extracted:* `location` (string)
*   **Acceptance Criteria (Given-When-Then):**
    *   *Scenario A (Happy Path):*
        *   **GIVEN** a valid location is requested.
        *   **WHEN** the user inquires about the current weather.
        *   **THEN** the agent fetches weather data from the weather API, returns success, and renders the current weather widget.
    *   *Scenario B (Fallback/Error Path):*
        *   **GIVEN** an invalid location is requested or the weather API is unreachable.
        *   **WHEN** the user inquires about the current weather.
        *   **THEN** the agent reports that the location could not be found or that service is temporarily unavailable, and prompts the user to check the location spelling.

### Feature 2: 3-Day Weather Forecast
*   **Description:** Displays weather forecasts for the upcoming three days, including high/low temperatures and conditions.
*   **Visual Interaction Mode:**
    *   *Trigger:* User types "Show me the forecast for London."
    *   *UI Rendered:* `weather_forecast_widget` showing three columns/cards with daily forecast parameters.
    *   *Form Actions:* Buttons to toggle Celsius/Fahrenheit units.
*   **Non-Visual Interaction Mode (SMS/Voice Fallback):**
    *   *SMS Transcript Flow:* "3-Day Forecast for London: Thu: 68/50°F (Cloudy), Fri: 70/52°F (Sunny), Sat: 65/48°F (Rain)."
    *   *Voice/Phone Flow:* "The three-day forecast for London is: Thursday, high of sixty-eight and low of fifty with cloudy skies. Friday, high of seventy and low of fifty-two, sunny. Saturday, high of sixty-five and low of forty-eight, rain."
    *   *Natural Language Parameters Extracted:* `location` (string)
*   **Acceptance Criteria (Given-When-Then):**
    *   *Scenario A (Happy Path):*
        *   **GIVEN** a valid location.
        *   **WHEN** the user asks for a forecast.
        *   **THEN** the agent retrieves forecast data, renders the forecast widget, and lists the daily high/low temperatures and skies.
    *   *Scenario B (Fallback/Error Path):*
        *   **GIVEN** the forecast service returns no data.
        *   **WHEN** the user asks for a forecast.
        *   **THEN** the agent explains that forecast data is currently unavailable and provides the current conditions as a fallback.

### Feature 3: Daily Weather Alerts
*   **Description:** Set up, view, or remove a recurring daily weather update alert for a chosen city at a specified time.
*   **Visual Interaction Mode:**
    *   *Trigger:* User types "Set up a daily weather alert."
    *   *UI Rendered:* `weather_alerts_widget` containing form inputs for Location, Time, and Alert toggle.
    *   *Form Actions:* Submit form button to save or modify alerts.
*   **Non-Visual Interaction Mode (SMS/Voice Fallback):**
    *   *SMS Transcript Flow:* User texts "Alert Miami 8:00 AM". Agent replies: "Daily weather alert set for Miami at 8:00 AM."
    *   *Voice/Phone Flow:* User says: "Can you set an alert for Miami at eight in the morning?". Agent replies: "I have set your daily weather alert for Miami at eight AM."
    *   *Natural Language Parameters Extracted:* `location` (string), `time` (string), `enabled` (boolean)
*   **Acceptance Criteria (Given-When-Then):**
    *   *Scenario A (Happy Path):*
        *   **GIVEN** a valid location and time.
        *   **WHEN** the user submits the daily alert form.
        *   **THEN** the agent saves the alert configuration to the user-scoped Firestore database and shows a success confirmation.
    *   *Scenario B (Fallback/Error Path):*
        *   **GIVEN** the location provided is invalid.
        *   **WHEN** the user submits the alert.
        *   **THEN** the agent reports the invalid location and asks the user to provide a valid city name.
