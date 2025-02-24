import datetime
from fakeredis import FakeStrictRedis
from app.database import RedisDatabase
from app.models import Timer


class TestRedisDatabase:
    def setup_method(self):
        self.db = RedisDatabase()
        self.db.client = FakeStrictRedis()
        self.timer = Timer(
            webhook_url="https://example.com/", timestamp=datetime.datetime.now()
        )

    def test_can_save_a_timer_object_to_redis(self):
        assert len(self.db.client.keys()) == 0
        self.db.save_timer(self.timer)
        assert len(self.db.client.keys()) == 1
