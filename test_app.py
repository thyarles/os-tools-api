import os
import app
import pytest

@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    with app.app.test_client() as client:
        yield client

def test_no_file(client):
    response = client.post('/extract-text')
    assert response.status_code == 400
    assert b'No file part' in response.data

def test_empty_filename(client):
    from io import BytesIO
    data = {
        'file': (BytesIO(b'my file contents'), '')
    }
    response = client.post('/extract-text', content_type='multipart/form-data', data=data)
    assert response.status_code == 400
    assert b'No selected file' in response.data

def test_wrong_file_type(client):
    from io import BytesIO
    data = {
        'file': (BytesIO(b'Not a DOC file'), 'test.txt')
    }
    response = client.post('/extract-text', content_type='multipart/form-data', data=data)
    assert response.status_code == 400
    assert b'Only .doc files are supported' in response.data

def test_valid_doc_file(client):
    doc_path = os.path.join(os.path.dirname(__file__), 'test.doc')
    with open(doc_path, 'rb') as f:
        data = {
            'file': (f, 'test.doc')
        }
        response = client.post('/extract-text', content_type='multipart/form-data', data=data)

    assert response.status_code == 200
    json_data = response.get_json()

    assert 'text' in json_data
    assert isinstance(json_data['text'], str)
    
    # Validate extracted text content
    expected_text = "This is a doc file that has 123antiword321 on it."
    assert expected_text in json_data['text']

