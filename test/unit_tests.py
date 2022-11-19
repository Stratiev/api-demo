from multiprocessing.pool import ThreadPool
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ls_all_default():
    payload = {}
    response = client.post("/ls", json=payload)
    assert response.status_code == 200

def test_ls_explicit_default():
    payload = {'folders': ['.'],
               'parameters': ['']}
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

def test_ls_permission_denied():
    payload = {'folders': ["/root"]}
    response = client.post("/ls", json=payload)
    assert response.status_code == 403

def test_ls_directory_not_found():
    payload = {'folders': ["/qwerty1234"]}
    response = client.post("/ls", json=payload)
    assert response.status_code == 404

def test_ls_blocking_call():
    def default_call(client):
        time.sleep(1)
        start_time = time.time()
        response = client.post("/ls", json={})
        end_time = time.time()
        return {'response': response,
                'start_time': start_time,
                'end_time': end_time}

    def blocking_call(client):
        start_time = time.time()
        response = client.post("/blocking_ls", json={})
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

def test_probability_all_default():
    payload = {}
    response = client.post("/probability", json=payload)
    assert response.status_code == 200

def test_ls_explicit_default():
    payload = {'team_1': 'Djurgarden',
               'team_2': 'Hammarby'}
    response = client.post("/probability", json=payload)
    assert response.status_code == 200

def test_probability_invalid_team_name():
    payload = {'team_1': 'Djurgardn',
               'team_2': 'Hammarby'}
    response = client.post("/probability", json=payload)
    assert response.status_code == 400

def test_probability_blocking_call():
    def default_call(client):
        time.sleep(1)
        start_time = time.time()
        response = client.post("/probability", json={})
        end_time = time.time()
        return {'response': response,
                'start_time': start_time,
                'end_time': end_time}

    def blocking_call(client):
        start_time = time.time()
        response = client.post("/blocking_probability", json={})
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

