import os
import pytest
from app.main import app
from pypdf import PdfReader


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_fix_pdf_preserves_text(client):
    test_file_path = "./tools/test.pdf"
    assert os.path.exists(test_file_path), "test.pdf file is missing"

    with open(test_file_path, "rb") as f:
        data = {"file": (f, "test.pdf")}
        response = client.post(
            "/fix-pdf", data=data, content_type="multipart/form-data"
        )

    assert response.status_code == 200
    assert response.mimetype == "application/pdf"

    # Save the returned PDF temporarily
    fixed_path = "fixed_test.pdf"
    with open(fixed_path, "wb") as out_file:
        out_file.write(response.data)

    # Read the PDF and check for the string
    reader = PdfReader(fixed_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() or ""

    os.remove(fixed_path)

    assert "123ghostscript321" in full_text
