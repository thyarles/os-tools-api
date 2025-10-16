import subprocess
import tempfile
import os
from flask import request, jsonify
from app.common.decoder import decode_text

def odt2txt():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    filename = getattr(file, 'filename', '') or ''

    if filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not filename.lower().endswith('.odt'):
        return jsonify({'error': 'Only .odt files are supported'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".odt") as temp_file:
        file.save(temp_file.name)

    try:
        result = subprocess.run(['odt2txt', temp_file.name],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                check=True,
                                text=False)

        stdout_data = decode_text(result.stdout)
        stderr_data = decode_text(result.stderr)

        if result.returncode != 0:
            return jsonify({'error': 'Failed to extract text', 'details': stderr_data}), 500

        lines = [line.strip() for line in stdout_data.splitlines() if line.strip()]
        text = '\n'.join(lines)

        return jsonify({'text': text})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to extract text', 'details': e.stderr}), 500
    finally:
        os.remove(temp_file.name)
