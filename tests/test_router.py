import pytest
import uuid
import datetime
import json
from pydantic import HttpUrl
from fastapi.testclient import TestClient

from app.main import create_app
from app.dependencies import get_db, get_redis_queue
from app.models import Timer
from .mock_dependecies import Mock_DB, Mock_RQ

valid_request = {
  "hours": 0,
  "minutes": 0,
  "seconds": 1,
  "webhook_url": "https://example.com/"
}

invalid_requests = {
    "invalid_url" : {
        "hours": 0,
        "minutes": 0,
        "seconds": 1,
        "webhook_url": "not a url"  
    },
    "negative_numbers": {
        "hours": -1,
        "minutes": 0,
        "seconds": 1,
        "webhook_url": "https://example.com/"
    },
    "not integers": {
        "hours": "one",
        "minutes": 0,
        "seconds": 1,
        "webhook_url": "https://example.com/"
    },
    "too long duration": {
        "hours": 999999999999999,
        "minutes": 0,
        "seconds": 0,
        "webhook_url": "https://example.com/"
    },
    "empty json": {},
    "incomplete json": {
        "minutes": 1,
        "seconds": 0,
        "webhook_url": "https://example.com/"
    }
}

FAKE_TIME = datetime.datetime(2025, 2, 15, 0, 0, 0, 0)

#override datetime.datetime.now() for easier testing
@pytest.fixture
def patch_datetime_now(monkeypatch):
    class Mock_Datetime(datetime.datetime):
        @classmethod
        def now(cls):
            return FAKE_TIME

    monkeypatch.setattr(datetime, 'datetime', Mock_Datetime)

class TestCreateTimerEndpoint():
    def setup_method(self):
        #create app and use DI to use the mocked database and job queue
        app = create_app()
        self.test_client = TestClient(app)
        #initalize mock database and job queue
        self.mocked_db = Mock_DB(timers={})
        self.mocked_rq = Mock_RQ(jobs=[])

        app.dependency_overrides[get_db] = lambda : self.mocked_db  
        app.dependency_overrides[get_redis_queue] = lambda : self.mocked_rq

    def test_request_sent_with_valid_data(self, patch_datetime_now):
        response = self.test_client.post("/timer", json=valid_request)
        response_data = json.loads(response.content)

        created_timer = list(self.mocked_db.timers.values())[0]
        expected_timestamp = FAKE_TIME + datetime.timedelta(seconds=1)

        # a timer resource is created
        assert len(self.mocked_db.timers) == 1
        assert str(created_timer.webhook_url) == valid_request["webhook_url"]
        assert created_timer.timestamp == expected_timestamp
        
        # a job is scheduled
        assert len(self.mocked_rq.jobs) == 1
        # jobs are stored in the mocked_rq as tuples, with the timestamp as the first arg
        assert self.mocked_rq.jobs[0][0] == expected_timestamp

        # endpoint responds with timer id and time left
        assert response.status_code == 200
        assert response_data['id'] == str(created_timer.id)
        assert response_data['time_left'] == 1

    @pytest.mark.parametrize("request_data", [
        (invalid_requests["invalid_url"]),
        (invalid_requests["negative_numbers"]),
        (invalid_requests["not integers"]),
        (invalid_requests["too long duration"]),
        (invalid_requests["empty json"]),
        (invalid_requests["incomplete json"]),
    ])
    def test_request_sent_with_invalid_data(self, request_data):
        response = self.test_client.post("/timer", json=request_data)

        # Timer isn't saved and job isn't crated
        assert response.status_code == 422
        assert len(self.mocked_db.timers) == 0
        assert len(self.mocked_rq.jobs) == 0

class TestGetTimerEndpoint():
    def setup_method(self, patch_datetime_now):
        #initalize mock database with timers
        expired_timer_id = str(uuid.uuid4())
        not_expired_timer_id =str( uuid.uuid4())

        self.expired_timer = Timer (
            id=expired_timer_id, 
            webhook_url=HttpUrl('https://example.com/'),
            timestamp= FAKE_TIME - datetime.timedelta(seconds=15)
        )
        self.not_expired_timer = Timer(
            id=not_expired_timer_id, 
            webhook_url=HttpUrl('https://example.com/'),

            timestamp = FAKE_TIME + datetime.timedelta(seconds=15)
        )

        self.mocked_db = Mock_DB(timers={
            expired_timer_id : self.expired_timer,
            not_expired_timer_id: self.not_expired_timer
            })
        
        self.mocked_rq = Mock_RQ(jobs=[])

        #create app and use DI to use the mocked database and job queue
        app = create_app()
        self.test_client = TestClient(app)

        app.dependency_overrides[get_db] = lambda : self.mocked_db  
        app.dependency_overrides[get_redis_queue] = lambda : self.mocked_rq

    def test_query_not_expired_timer(self, patch_datetime_now):
        response = self.test_client.get(f"/timer/{str(self.not_expired_timer.id)}")
        response_data = json.loads(response.content)

        assert response.status_code == 200
        assert response_data['id'] == str(self.not_expired_timer.id)
        assert response_data['time_left'] == 15

    def test_query_expired_timer(self, patch_datetime_now):
        response = self.test_client.get(f"/timer/{str(self.expired_timer.id)}")
        response_data = json.loads(response.content)

        assert response.status_code == 200
        assert response_data['id'] == str(self.expired_timer.id)
        assert response_data['time_left'] == 0

    def test_query_non_existing_timer(self):
        response = self.test_client.get(f"/timer/{str(uuid.uuid4())}")
        assert response.status_code == 404
