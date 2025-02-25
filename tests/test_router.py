from app.router import router


# test create timer
def test_request_sent_with_valid_data():
    #assert timer is created in db with correct data
    #assert job is scheduled
    #assert response.status code is 200
    #assert response returns timer id and time left
    assert True

def test_request_sent_with_invalid_data():
    #cases: invalid json, too many hour, negative hours? 
    #assert timer isnt created
    #assert no job is scheduled
    #assert response code 422
    assert True



# test get timer

def queries_existing_timer():
    #cases: expired timer, live timer
    #assert response.status code 200
    #assert response.time left is correct/0
    assert True

# returns 404 for non existing timer
def returns_not_found_for_not_existing_timer():
    #assert response. status code is 404
    assert True

