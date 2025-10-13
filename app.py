from flask import Flask, request, jsonify
from flasgger import Swagger
import subprocess
import tempfile
import os

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/extract-text', methods=['POST'])
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
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.lower().endswith('.doc'):
        return jsonify({'error': 'Only .doc files are supported'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".doc") as temp_file:
        file.save(temp_file.name)

    try:
        result = subprocess.run(['antiword', temp_file.name],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                check=True,
                                text=True)

	# Normal output
	# text = result.stdout.strip()

        # Optional: beautify
        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        text = '\n\n'.join(lines)

        return jsonify({'text': text})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to extract text', 'details': e.stderr}), 500
    finally:
        os.remove(temp_file.name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

