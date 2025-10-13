# Antiword API

A lightweight Flask-based API that accepts `.doc` (Word 97-2003) files, extracts the text using `antiword`, and returns it in a clean JSON format.

Includes Swagger UI documentation for ease of testing and integration.

---

## Features

- Upload `.doc` file via POST request
- Extracts and beautifies plain text from the document
- Returns structured JSON
- Swagger UI (`/apidocs`) for testing and documentation
- Fully containerized with Docker
- Easy to extend for HTML/Markdown output or other formats

---

## Technologies & Libraries Used

| Tech           | Purpose                                      |
|----------------|----------------------------------------------|
| **Python 3.11** | Backend language                             |
| **Flask**      | Web framework                                |
| **Flasgger**   | Swagger/OpenAPI documentation for Flask      |
| **antiword**   | CLI tool to extract text from `.doc` files   |
| **Docker**     | Containerization                             |

---

## Installation

### Prerequisites

- [Docker](https://www.docker.com/get-started)

---

## Run with Docker

Clone the repository and build the image:

```bash
git clone https://github.com/your-org/doc-text-api.git
cd doc-text-api

docker build -t doc-text-api .
docker run -p 5000:5000 doc-text-api
````

Now the API is available at: [http://localhost:5000](http://localhost:5000)

---

## API Usage

### Endpoint: `POST /extract-text`

**Form Field**: `file` — must be a `.doc` file (old Word format)

#### cURL Example

```bash
curl -X POST http://localhost:5000/extract-text \
  -F "file=@/path/to/your/file.doc"
```

#### Sample Response

```json
{
  "text": "This is the extracted text from the document."
}
```

---

## Swagger UI (API Docs)

Once running, go to:

> [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)

You’ll see an interactive Swagger interface to test and explore the API.

---

## For Developers

### Project Structure

```
doc-text-api/
│
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container setup
└── README.md            # You're here!
```

### Local Development (without Docker)

1. Install `antiword`:

   ```bash
   sudo apt install antiword  # Debian/Ubuntu
   ```

2. Set up a Python virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python app.py
   ```

### Modify Swagger Configuration

Swagger uses in-code Python docstrings via `flasgger`. If you want to customize the Swagger UI or add global info:

In `app.py`:

```python
swagger = Swagger(app, template={
    "info": {
        "title": "DOC Text Extractor API",
        "description": "API to extract text from .doc (Word 97-2003) files using antiword.",
        "version": "1.0.0"
    }
})
```

---

## Security Notes

* Only accepts `.doc` files — does **not** process `.docx`.
* No authentication is enabled by default.
* Consider wrapping this API behind a gateway or firewall in production environments.

---

## License

MIT License — free for personal and commercial use.

---

## Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to change or add.

---

## FAQ

### Why only `.doc` files?

This tool uses `antiword`, which only supports old Word binary formats (`.doc`). For `.docx`, consider `python-docx` or `pandoc`.

### Can it return HTML or Markdown?

Right now, it returns clean plain text. Let us know if you want to support formatting or downloadable outputs!

