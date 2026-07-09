import os
import unittest
try:
    import pytest
except ImportError:
    class MockPytest:
        class Mark:
            @staticmethod
            def asyncio(f): return f
        mark = Mark()
    pytest = MockPytest()
from google.adk.tools.tool_context import ToolContext
from app.core.hubscape_adk import RemoteContext, context_session
from app.scripts.get_current_weather import get_current_weather
from app.scripts.get_weather_forecast import get_weather_forecast
from app.scripts.save_weather_alert import save_weather_alert
from app.scripts.get_weather_alerts import get_weather_alerts
from app.scripts.set_temp_unit import set_temp_unit

# In-memory Firestore Mock for unit testing
class MockDocumentReference:
    def __init__(self, path, db_dict):
        self.path = path
        self.db_dict = db_dict
        
    def get(self):
        class MockSnapshot:
            def __init__(self, exists, data, doc_id):
                self.exists = exists
                self._data = data
                self.id = doc_id
            def to_dict(self):
                return self._data
        exists = self.path in self.db_dict
        data = self.db_dict.get(self.path, {})
        doc_id = self.path.split("/")[-1]
        return MockSnapshot(exists, data, doc_id)
        
    def set(self, data, merge=True):
        if merge and self.path in self.db_dict:
            self.db_dict[self.path].update(data)
        else:
            self.db_dict[self.path] = data.copy()
            
    def delete(self):
        self.db_dict.pop(self.path, None)

class MockCollectionReference:
    def __init__(self, path, db_dict):
        self.path = path
        self.db_dict = db_dict
        
    def stream(self):
        class MockDoc:
            def __init__(self, doc_id, data):
                self.id = doc_id
                self._data = data
            def to_dict(self):
                return self._data
                
        results = []
        for p, data in self.db_dict.items():
            if p.startswith(self.path):
                subpath = p[len(self.path):].lstrip("/")
                if "/" not in subpath:
                    results.append(MockDoc(subpath, data))
        return results

class MockFirestoreClient:
    def __init__(self):
        self.db_dict = {}
        
    def document(self, path):
        return MockDocumentReference(path, self.db_dict)
        
    def collection(self, path):
        return MockCollectionReference(path, self.db_dict)

class TestWeatherAgent(unittest.TestCase):
    def setUp(self):
        os.environ["INTEGRATION_TEST"] = "TRUE"
        self.ctx = RemoteContext(
            user_id="test_user",
            agent_id="weather_agent",
            org_id="test_org",
            hub_id="test_hub",
            project_id="test_project",
            raw_context={"mode": "chat_pc"}
        )
        self.mock_db = MockFirestoreClient()
        self.ctx._db = self.mock_db
        self.tool_ctx = ToolContext(type('Mock', (), {'session': type('Session', (), {'state': {}})()})())

    def test_current_weather(self):
        with context_session(self.ctx):
            async def run_test():
                res = await get_current_weather(self.tool_ctx, "Seattle")
                self.assertEqual(res["status"], "success")
                self.assertEqual(res["location"], "Seattle")
                self.assertEqual(res["temp"], "72.0")
                self.assertEqual(res["unit"], "F")
                
            import asyncio
            asyncio.run(run_test())

    def test_weather_forecast(self):
        with context_session(self.ctx):
            async def run_test():
                res = await get_weather_forecast(self.tool_ctx, "London", days=2)
                self.assertEqual(res["status"], "success")
                self.assertEqual(len(res["forecast_rows"]), 2)
                self.assertEqual(res["forecast_rows"][0]["date"], "Thu")
                self.assertEqual(res["forecast_rows"][0]["temp"], "50 / 68 °F")
                
            import asyncio
            asyncio.run(run_test())

    def test_save_and_get_alerts(self):
        with context_session(self.ctx):
            async def run_test():
                # Test save
                save_res = await save_weather_alert(self.tool_ctx, "Seattle", "08:00", enabled=True)
                self.assertEqual(save_res["status"], "success")
                self.assertEqual(save_res["doc_id"], "alert_seattle")
                
                # Test get
                get_res = await get_weather_alerts(self.tool_ctx)
                self.assertEqual(get_res["status"], "success")
                self.assertEqual(len(get_res["alerts"]), 1)
                self.assertEqual(get_res["alerts"][0]["location"], "Seattle")
                self.assertEqual(get_res["alerts"][0]["time"], "08:00")
                self.assertTrue(get_res["alerts"][0]["enabled"])
                
            import asyncio
            asyncio.run(run_test())

    def test_set_temp_unit(self):
        with context_session(self.ctx):
            async def run_test():
                # Set unit to celsius
                res = await set_temp_unit(self.tool_ctx, "celsius")
                self.assertEqual(res["status"], "success")
                
                # Test that current weather adapts to Celsius unit preference
                weather_res = await get_current_weather(self.tool_ctx, "Seattle")
                self.assertEqual(weather_res["unit"], "C")
                self.assertEqual(weather_res["temp"], "22.0")
                
            import asyncio
            asyncio.run(run_test())

# Wrapper functions for pytest compatibility
@pytest.mark.asyncio
async def test_current_weather_pytest():
    suite = TestWeatherAgent()
    suite.setUp()
    await get_current_weather(suite.tool_ctx, "Seattle")

@pytest.mark.asyncio
async def test_weather_forecast_pytest():
    suite = TestWeatherAgent()
    suite.setUp()
    await get_weather_forecast(suite.tool_ctx, "London", days=2)

@pytest.mark.asyncio
async def test_alerts_pytest():
    suite = TestWeatherAgent()
    suite.setUp()
    await save_weather_alert(suite.tool_ctx, "Seattle", "08:00", enabled=True)
    await get_weather_alerts(suite.tool_ctx)

@pytest.mark.asyncio
async def test_unit_preference_pytest():
    suite = TestWeatherAgent()
    suite.setUp()
    await set_temp_unit(suite.tool_ctx, "celsius")
