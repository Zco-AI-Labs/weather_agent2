## 💬 4. Interaction Scripts & Conversational Flows

### Scenario 1: Inquiry about Current Weather

#### Flow A: Visual Path (Chat UI with widgets)
*   **User:** "What's the weather in Seattle?"
*   **Agent (Behind the Scenes):** Calls `consultAgent` -> calls tool `get_current_weather` with argument `location="Seattle"`.
*   **Agent UI Rendered:** Displays Widget `current_weather_widget` containing Seattle's current conditions: 65°F, Overcast, 70% Humidity.
*   **Agent Message:** "Here is the current weather for Seattle. It is currently 65°F and overcast."
*   **User clicks button:** Clicks "Add to Saved Locations".
*   **Backend Response:** "Seattle has been added to your saved locations list."

#### Flow B: Non-Visual SMS Path (No-UI, Text Only)
*   **User (SMS):** "weather Seattle"
*   **Agent (Behind the Scenes):** Calls tool `get_current_weather` with `location="Seattle"`.
*   **Agent Text Reply:** "Current weather in Seattle: 65°F (18°C), Overcast. Humidity: 70%. Wind: 5 mph S."

#### Flow C: Non-Visual Voice Path (No-UI, Spoken Phone Call)
*   **User (Voice):** "What's the weather like in Seattle?"
*   **Agent (Behind the Scenes):** Calls tool `get_current_weather` with `location="Seattle"`.
*   **Agent Speech Reply:** "In Seattle, it is currently sixty-five degrees and overcast, with seventy percent humidity and south winds at five miles per hour."

---

### Scenario 2: Setting a Daily Weather Alert

#### Flow A: Visual Path (Chat UI with widgets)
*   **User:** "I want to receive daily weather alerts."
*   **Agent (Behind the Scenes):** Returns system instructions to display the alert configuration form.
*   **Agent UI Rendered:** Displays Widget `weather_alerts_widget` containing inputs for city, alert time, and a toggle.
*   **Agent Message:** "Please fill out this form to set up your daily weather alert."
*   **User clicks button:** Enters `Location: Chicago`, `Time: 7:00 AM`, sets toggle to enabled, and clicks "Save Alert".
*   **Backend Response:** "Your daily weather alert for Chicago at 7:00 AM has been saved."

#### Flow B: Non-Visual SMS Path (No-UI, Text Only)
*   **User (SMS):** "Set alert Chicago 7am"
*   **Agent (Behind the Scenes):** Calls tool `save_weather_alert` with `location="Chicago"`, `time="07:00"`, `enabled=True`.
*   **Agent Text Reply:** "Daily weather alert set for Chicago at 7:00 AM."

#### Flow C: Non-Visual Voice Path (No-UI, Spoken Phone Call)
*   **User (Voice):** "Can you set a weather alert for Chicago at seven AM?"
*   **Agent (Behind the Scenes):** Calls tool `save_weather_alert` with `location="Chicago"`, `time="07:00"`, `enabled=True`.
*   **Agent Speech Reply:** "I have set your daily weather alert for Chicago at seven AM."
