import subprocess
import tempfile
import os
from flask import request, jsonify, send_file

DEFAULT_GS_OPTIONS = {
    '-dSAFER': None,
    '-dBATCH': None,
    '-dNOPAUSE': None,
    '-sDEVICE': 'pdfwrite',
    '-dPreserveAnnots': 'false',
    '-dCompatibilityLevel': '1.4',
    '-dPDFSETTINGS': '/screen',
    '-dDownsampleColorImages': 'true',
    '-dDownsampleGrayImages': 'true',
    '-dDownsampleMonoImages': 'true',
    '-dColorImageResolution': '72',
    '-dGrayImageResolution': '72',
    '-dMonoImageResolution': '72',
    '-dEmbedAllFonts': 'false'
}

def build_gs_command(input_path, output_path, custom_options=None):
    options = DEFAULT_GS_OPTIONS.copy()
    if custom_options:
        options.update(custom_options)

    command = ['gs']
    for key, value in options.items():
        if value is None:
            command.append(key)
        else:
            command.append(f"{key}={value}")
    command.extend(['-o', output_path, input_path])
    return command

def ghostscript():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only .pdf files are supported'}), 400

    # Optional custom Ghostscript options from JSON string
    custom_options = request.form.get('gs_options')
    try:
        custom_options = eval(custom_options) if custom_options else None
        if custom_options and not isinstance(custom_options, dict):
            raise ValueError("gs_options must be a JSON object")
    except Exception as e:
        return jsonify({'error': 'Invalid gs_options format', 'details': str(e)}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        file.save(temp_file.name)

    try:
        output_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        output_pdf.close()

        gs_command = build_gs_command(temp_file.name, output_pdf.name, custom_options)

        try:
            result = subprocess.run(
                gs_command,
                # stdout=subprocess.PIPE,
                # stderr=subprocess.PIPE,
                check=True,
                text=True
            )

        except subprocess.CalledProcessError as e:
            # This block runs if the command fails (returns a non-zero exit code)
            return jsonify({'error': 'Failed to process PDF', 'details': e.stderr}), 500

        except FileNotFoundError:
            # This block runs if the command itself is not found
            return jsonify({'error': 'File not found!'}), 500

        return send_file(output_pdf.name, as_attachment=True, mimetype='application/pdf', download_name='fixed_output.pdf')
    
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Ghostscript command failed', 'details': e.stderr}), 500
    finally:
        os.remove(temp_file.name)
        os.remove(output_pdf.name)