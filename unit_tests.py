from multiprocessing.pool import ThreadPool
import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ls_all_default():
    response = client.post("/ls")
    assert response.status_code == 200

def test_ls_explicit_default():
    payload = {'folders': ["."],
               'parameters': None}
    response = client.post("/ls", json=payload)
    assert response.status_code == 200

def test_ls_parameters():
    payload = {'parameters': ['l', 'all']}
    response = client.post("/ls", json=payload)
    assert response.status_code == 200

def test_ls_parameters_fail():
    payload = {'parameters': ['234']}
    response = client.post("/ls", json=payload)
    assert response.status_code == 400
    assert response.json()['detail'] == 'Bad request. Unrecognized option for parameter value.'

def test_blocking_call():
    def default_call(client):
        time.sleep(1)
        start_time = time.time()
        response = client.post("/ls")
        end_time = time.time()
        return {'response': response,
                'start_time': start_time,
                'end_time': end_time}

    def blocking_call(client):
        start_time = time.time()
        response = client.post("/blocking_ls")
        end_time = time.time()
        return {'response': response,
                'start_time': start_time,
                'end_time': end_time}

    pool = ThreadPool(processes=2)
    default_result = pool.apply_async(default_call, (client, ))
    blocking_result = pool.apply_async(blocking_call, (client, ))
    assert default_result.get()['response'].status_code == 200
    assert blocking_result.get()['response'].status_code == 200
    assert default_result.get()['end_time'] < blocking_result.get()['end_time']
    assert default_result.get()['start_time'] > blocking_result.get()['start_time']

