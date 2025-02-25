import httpx
import datetime
from fakeredis import FakeStrictRedis
from unittest.mock import patch, MagicMock
from app.queue import RedisQueue
from app.jobs import TimerSerivce, trigger_webhook
from app.models import Timer

timer = Timer(
    webhook_url="https://example.com/",
    timestamp=datetime.datetime.now()
)

def test_schedules_timer():
    fake_redis_queue = RedisQueue(redis_connection=FakeStrictRedis())

    timer_service_with_fake_redis = TimerSerivce(redis_queue=fake_redis_queue)
    job = timer_service_with_fake_redis.schedule_timer(timer)
    
    assert job.get_status().name == "SCHEDULED"
    assert job.func_name is not None

def test_trigger_webhook_makes_post_request():
    with patch('httpx.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        response = trigger_webhook(timer)
        
        mock_post.assert_called_once()
        mock_post.assert_called_with(url=str(timer.webhook_url), data={"id": timer.id})
        assert response == 200

def test_trigger_webhook_handles_httpx_errors():

    with patch('httpx.post') as mock_post:
        mock_post.side_effect = httpx.HTTPError("Mocked HTTP error")

        response = trigger_webhook(timer)

        #test would fail if error wouldn't be handled
        assert response is None
