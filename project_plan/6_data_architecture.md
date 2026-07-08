## 💾 6. Data Architecture & DB Schemas

We will store user-specific configuration (such as daily weather alert subscriptions and unit preferences) in user-scoped Firestore paths:
*   **User Scope:** `platform_users/{user_id}/agent_data/{agent_id}/{collection_name}`

---

### Collection: `weather_alerts`
*   **Scope:** `user`
*   **Document ID Format:** `alert_{normalized_location}` (e.g., `alert_seattle` for Seattle, WA).

#### Fields Table
| Field Name | Type | Description | Mandatory / Optional |
| :--- | :--- | :--- | :--- |
| `id` | `String` | Document ID (`alert_{normalized_location}`) | Mandatory |
| `created_at` | `Timestamp` | Injected automatically by context helpers | Mandatory |
| `created_by` | `String` | Injected automatically by context helpers | Mandatory |
| `updated_at` | `Timestamp` | Injected automatically by context helpers | Mandatory |
| `updated_by` | `String` | Injected automatically by context helpers | Mandatory |
| `version` | `Integer` | Injected automatically by context helpers | Mandatory |
| `location` | `String` | City name or location query for weather alert | Mandatory |
| `time` | `String` | Trigger time in 24h format (e.g., "07:30") | Mandatory |
| `enabled` | `Boolean` | Flag indicating whether alert is currently active | Mandatory |

---

### Collection: `user_preferences`
*   **Scope:** `user`
*   **Document ID Format:** `preferences` (a single singleton configuration document per user).

#### Fields Table
| Field Name | Type | Description | Mandatory / Optional |
| :--- | :--- | :--- | :--- |
| `id` | `String` | Document ID (`preferences`) | Mandatory |
| `created_at` | `Timestamp` | Injected automatically by context helpers | Mandatory |
| `created_by` | `String` | Injected automatically by context helpers | Mandatory |
| `updated_at` | `Timestamp` | Injected automatically by context helpers | Mandatory |
| `updated_by` | `String` | Injected automatically by context helpers | Mandatory |
| `version` | `Integer` | Injected automatically by context helpers | Mandatory |
| `temp_unit` | `String` | Preferred temperature unit: `"celsius"` or `"fahrenheit"` | Mandatory |
| `default_location` | `String` | User's home or primary location for fast lookups | Optional |
