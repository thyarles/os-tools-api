import os
import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_antiword_success(client):
    test_file_path = './tools/test.doc'
    assert os.path.exists(test_file_path), "test.doc file is missing"

    with open(test_file_path, 'rb') as f:
        data = {'file': (f, 'test.doc')}
        response = client.post('/antiword', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    json_data = response.get_json()
    assert 'text' in json_data
    assert '123antiword321' in json_data['text']
