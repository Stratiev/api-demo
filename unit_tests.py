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
