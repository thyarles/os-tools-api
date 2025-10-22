from flask import Flask
from flasgger import Swagger
from app.tools.antiword import antiword
from app.tools.ghostscript import ghostscript
from app.tools.lynx import lynx
from app.tools.unrtf import unrtf
from app.tools.odt2txt import odt2txt
from app.tools.docx2txt import docx2txt

app = Flask(__name__)
swagger_template = {
    "info": {
        "title": "OS Tools API",
        "description": "API documentation",
        "version": "1.0.1",
    }
}
swagger = Swagger(app, template=swagger_template)


@app.route("/ping", methods=["GET"])
def ping():
    """
    Test the liveness of the API
    ---
    responses:
      200:
        description: Server is up and running
    """
    return "Pong", 200


@app.route("/doc", methods=["POST"])
def extract_text():
    """
    Extract text from a .doc (Word 97-2003) file
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The .doc file to upload
    responses:
      200:
        description: Extracted text
        schema:
          type: object
          properties:
            text:
              type: string
              description: Extracted plain text
      400:
        description: Bad request (e.g., missing file or wrong file type)
      500:
        description: Internal error during text extraction
    """
    return antiword()


@app.route("/pdf", methods=["POST"])
def fix_pdf():
    """
    Fix a PDF using Ghostscript with optional custom parameters
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The PDF file to upload
      - name: gs_options
        in: formData
        type: string
        required: false
        description: Optional Ghostscript options as a JSON object (e.g., {"-dPDFSETTINGS":"/ebook","-dEmbedAllFonts":"true"})
    responses:
      200:
        description: Fixed PDF file
        content:
          application/pdf:
            schema:
              type: string
              format: binary
      400:
        description: Bad request (e.g., missing file, wrong file type, or invalid options)
      500:
        description: Internal error during PDF processing
    """
    return ghostscript()


@app.route("/html", methods=["POST"])
@app.route("/htm", methods=["POST"])
def extract_lynx():
    """
    Extract text from an HTML file using Lynx
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The .html file to upload
    responses:
      200:
        description: Extracted text
        schema:
          type: object
          properties:
            text:
              type: string
              description: Extracted plain text
      400:
        description: Bad request (e.g., missing file, wrong file type)
      500:
        description: Internal error during text extraction
    """
    return lynx()


@app.route("/rtf", methods=["POST"])
def extract_unrtf():
    """
    Extract text from an RTF file using unrtf
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The .rtf file to upload
    responses:
      200:
        description: Extracted text
        schema:
          type: object
          properties:
            text:
              type: string
              description: Extracted plain text
      400:
        description: Bad request (e.g., missing file, wrong file type)
      500:
        description: Internal error during text extraction
    """
    return unrtf()


@app.route("/odt", methods=["POST"])
def extract_odt2txt():
    """
    Extract text from an ODT file using odt2txt
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The .odt file to upload
    responses:
      200:
        description: Extracted text
        schema:
          type: object
          properties:
            text:
              type: string
              description: Extracted plain text
      400:
        description: Bad request (e.g., missing file, wrong file type)
      500:
        description: Internal error during text extraction
    """
    return odt2txt()


@app.route("/docx", methods=["POST"])
def extract_docx2txt():
    """
    Extract text from a DOCX file using docx2txt
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The .docx file to upload
    responses:
      200:
        description: Extracted text
        schema:
          type: object
          properties:
            text:
              type: string
              description: Extracted plain text
      400:
        description: Bad request (e.g., missing file, wrong file type)
      500:
        description: Internal error during text extraction
    """
    return docx2txt()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
