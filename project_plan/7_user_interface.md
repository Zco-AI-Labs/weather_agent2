## 🎨 7. User Interface & Widgets Specification

We will define three dynamic widgets using the Hubscape Lego UI element schema.

### Widget 1: `current_weather_widget`
*   **Type:** Current Weather Summary Card
*   **Theme Token Default:** `indigo`
*   **Layout JSON Structure:**
```json
{
  "type": "container",
  "props": {
    "className": "flex flex-col gap-4 p-5 bg-gradient-to-br from-indigo-500 to-blue-600 text-white rounded-2xl shadow-md"
  },
  "children": [
    {
      "type": "text",
      "props": {
        "text": "{{location}}",
        "className": "text-2xl font-bold"
      }
    },
    {
      "type": "container",
      "props": {
        "className": "flex items-center justify-between"
      },
      "children": [
        {
          "type": "text",
          "props": {
            "text": "{{temp}}°{{unit}}",
            "className": "text-5xl font-extrabold"
          }
        },
        {
          "type": "text",
          "props": {
            "text": "{{condition}}",
            "className": "text-lg font-medium opacity-90"
          }
        }
      ]
    },
    {
      "type": "container",
      "props": {
        "className": "grid grid-cols-2 gap-4 mt-2 border-t border-white/20 pt-4"
      },
      "children": [
        {
          "type": "text",
          "props": {
            "text": "💨 Wind: {{wind}}",
            "className": "text-sm"
          }
        },
        {
          "type": "text",
          "props": {
            "text": "💧 Humidity: {{humidity}}%",
            "className": "text-sm"
          }
        }
      ]
    }
  ]
}
```

---

### Widget 2: `weather_forecast_widget`
*   **Type:** 3-Day Forecast Table Card
*   **Theme Token Default:** `blue`
*   **Layout JSON Structure:**
```json
{
  "type": "container",
  "props": {
    "className": "flex flex-col gap-4 p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl"
  },
  "children": [
    {
      "type": "text",
      "props": {
        "text": "3-Day Weather Forecast: {{location}}",
        "className": "font-bold text-lg text-slate-800 dark:text-white"
      }
    },
    {
      "type": "table",
      "props": {
        "paginated": false,
        "columns": [
          { "key": "date", "name": "Date", "width": "30%" },
          { "key": "condition", "name": "Condition", "width": "40%" },
          { "key": "temp", "name": "Min/Max Temp", "width": "30%" }
        ],
        "rows": "{{forecast_rows}}"
      }
    }
  ]
}
```

---

### Widget 3: `weather_alerts_widget`
*   **Type:** Weather Alert Subscription Form
*   **Theme Token Default:** `emerald`
*   **Layout JSON Structure:**
```json
{
  "type": "container",
  "props": {
    "className": "flex flex-col gap-4 p-4 bg-slate-50 dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800"
  },
  "children": [
    {
      "type": "text",
      "props": {
        "text": "Daily Weather Alert Subscription",
        "className": "font-bold text-lg text-slate-800 dark:text-white"
      }
    },
    {
      "type": "input",
      "props": {
        "name": "location",
        "label": "Location",
        "placeholder": "Enter city name..."
      }
    },
    {
      "type": "input",
      "props": {
        "name": "time",
        "label": "Alert Time (24h format)",
        "inputType": "time"
      }
    },
    {
      "type": "toggle",
      "props": {
        "name": "enabled",
        "label": "Enable Daily Updates",
        "variant": "switch",
        "size": "md"
      }
    },
    {
      "type": "button",
      "props": {
        "label": "Save Alert Setting",
        "actionUrl": "/api/plugins/{{agent_id}}/save_alert",
        "className": "bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg mt-2"
      }
    }
  ]
}
```
