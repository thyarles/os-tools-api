import subprocess
import tempfile
import os
from flask import request, jsonify

def lynx():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.lower().endswith('.html'):
        return jsonify({'error': 'Only .html files are supported'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
        file.save(temp_file.name)

    try:
        result = subprocess.run(['lynx', '-dump', '-nolist', temp_file.name],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                check=True,
                                text=True)

        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        text = '\n'.join(lines)

        return jsonify({'text': text})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to extract text', 'details': e.stderr}), 500
    finally:
        os.remove(temp_file.name)
