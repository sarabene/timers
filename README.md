# Sendcloud Technical Assignment

This is my solution for the Sendcloud Technical Assignment. 

## Setup 

### Prerequisites 

- Python 3.10
- Pipenv
- Docker


### Project Setup

1. Download the source code:

(Or, clone the git repository: )

```
git clone https://github.com/sarabene/timers.git
``` 

2. You can create a virtual environment to install the project dependencies:

```
pipenv shell
pipenv install --dev
```

3. To build and run the services, use:
```
docker compose up
```

4. To run unittests, run the following inside the virtual env: 
```
pytest
```

5. To test the endpoints manually: 
Easiest way to do this is to use Swagger UI: 

* Navigate to http://localhost:8000/docs
* Try out creating a timer and then querying it. 
* After the specified time passes, you should see logs from redis-worker indicating that jobs have been executed.
