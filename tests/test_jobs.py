import pytest


# set_timer to executed
def test_sets_timer_to_executed_in_db():
    #assert 
    assert True

#test trigegr webhook
def test_trigger_webhook():
    #assert creates post reqest
    # assert request url, data, method=POST
    #assert no job is scheduled
    # assert changes timer_status
    assert True


def test_schedule_timer():
    #mock redis 
    # assert enques timer --> asser in mock_redis_que

    assert True

def schedules_all_not_executed_expired_timers():
    #mock redis, add fake timers
    # assert expired timers in mock redis que
    # assert other timers not in rq

    assert True
