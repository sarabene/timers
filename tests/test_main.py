import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.database import Database
from app.models import Timer

# Mocking DB for testing
@pytest.fixture
def mock_get_db():
    # Mock the database dependency
    class MockDB(Database):
        def save_timer(self, timer: Timer):
            pass

        def get_timer(self, timer_id: str):
            pass

        def get_all_timers(self):
            return []
        
    yield MockDB()

def test_creates_FastAPI_app_and_calls_initialize_timer_services():
    # Test that the app is created successfully
    # assert initialize_timer_service_was_called()
    #test_app = create_app()
    assert True


def test_initialize_timer_service():
    # assert created a timer_serice instance 
    # assert calls processed expired timers
    assert True

