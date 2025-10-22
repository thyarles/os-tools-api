import os
import pytest
from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_odt2txt_success(client):
    test_file_path = "./tools/test.odt"
    assert os.path.exists(test_file_path), "test.odt file is missing"

    with open(test_file_path, "rb") as f:
        data = {"file": (f, "test.odt")}
        response = client.post(
            "/odt", data=data, content_type="multipart/form-data"
        )

    assert response.status_code == 200
    json_data = response.get_json()
    assert "text" in json_data
    assert "123odt321" in json_data["text"]
