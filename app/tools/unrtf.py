import subprocess
import tempfile
import os
from flask import request, jsonify


def unrtf():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.lower().endswith(".rtf"):
        return jsonify({"error": "Only .rtf files are supported"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".rtf") as temp_file:
        file.save(temp_file.name)

    try:
        result = subprocess.run(
            ["unrtf", "--text", "--nopict", temp_file.name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=False,
        )

        stdout_data = result.stdout.decode("latin1", errors="ignore")
        stderr_data = result.stderr.decode("latin1", errors="ignore")

        if result.returncode != 0:
            return (
                jsonify({"error": "Failed to extract text", "details": stderr_data}),
                500,
            )

        # Split lines and find the separator
        lines = stdout_data.splitlines()
        try:
            separator_index = lines.index("-----------------")
            content_lines = lines[separator_index + 1 :]
        except ValueError:
            # If separator not found, use all lines
            content_lines = lines

        # Clean up the lines
        cleaned_lines = [line.strip() for line in content_lines if line.strip()]
        text = "\n".join(cleaned_lines)

        return jsonify({"text": text})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to extract text", "details": e.stderr}), 500
    finally:
        os.remove(temp_file.name)
