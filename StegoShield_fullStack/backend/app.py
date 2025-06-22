from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import os
import uuid

# Import the core steganography functions and help text
from steganography import encode_message, decode_message, encode_image, decode_image
import help as help_text

app = Flask(__name__)
# Enable CORS to allow requests from the React frontend
CORS(app)

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'webp', 'gif', 'svg', }

def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file_storage):
    """Saves an uploaded file with a unique name to prevent conflicts."""
    if file_storage and allowed_file(file_storage.filename):
        # Generate a unique filename to avoid overwriting files
        filename = f"{uuid.uuid4()}_{file_storage.filename}"
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_storage.save(path)
        return path
    return None

# --- API Endpoints ---

@app.route('/api/encode-text', methods=['POST'])
def handle_encode_text():
    """API endpoint to hide a text message in an image."""
    if 'carrier' not in request.files or 'message' not in request.form:
        return jsonify({"error": "Carrier image and message are required."}), 400

    carrier_file = request.files['carrier']
    message = request.form['message']

    if carrier_file.filename == '' or not message:
        return jsonify({"error": "Please provide both a carrier image and a message."}), 400

    carrier_path = save_file(carrier_file)
    if not carrier_path:
        return jsonify({"error": "Invalid file type. Please use PNG, JPG, or BMP."}), 400

    try:
        encoded_image_obj = encode_message(carrier_path, message)
        output_filename = f"encoded_text_{uuid.uuid4()}.png"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        encoded_image_obj.save(output_path, "PNG")
        
        # Send the processed image back to the client for download
        return send_file(output_path, as_attachment=True, download_name=output_filename)
    except Exception as e:
        return jsonify({"error": f"An error occurred during encoding: {e}"}), 500

@app.route('/api/decode-text', methods=['POST'])
def handle_decode_text():
    """API endpoint to extract a text message from an image."""
    if 'encoded' not in request.files:
        return jsonify({"error": "Please select an image to decode."}), 400

    encoded_file = request.files['encoded']
    if encoded_file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    encoded_path = save_file(encoded_file)
    if not encoded_path:
        return jsonify({"error": "Invalid file type."}), 400

    try:
        secret_message = decode_message(encoded_path)
        return jsonify({"message": secret_message})
    except Exception as e:
        return jsonify({"error": f"Failed to decode message: {e}"}), 500

@app.route('/api/encode-image', methods=['POST'])
def handle_encode_image():
    """API endpoint to hide an image within another image."""
    if 'carrier' not in request.files or 'secret' not in request.files:
        return jsonify({"error": "Both carrier and secret images are required."}), 400

    carrier_file = request.files['carrier']
    secret_file = request.files['secret']

    if carrier_file.filename == '' or secret_file.filename == '':
        return jsonify({"error": "Please select both a carrier and a secret image."}), 400

    carrier_path = save_file(carrier_file)
    secret_path = save_file(secret_file)

    if not carrier_path or not secret_path:
        return jsonify({"error": "Invalid file type for one or both images."}), 400

    try:
        encoded_image_obj = encode_image(carrier_path, secret_path)
        output_filename = f"encoded_image_{uuid.uuid4()}.png"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        encoded_image_obj.save(output_path, "PNG")
        
        return send_file(output_path, as_attachment=True, download_name=output_filename)
    except ValueError as e:
        # Catch specific value errors (e.g., secret image too large)
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred during image encoding: {e}"}), 500

@app.route('/api/decode-image', methods=['POST'])
def handle_decode_image():
    """API endpoint to extract a hidden image from a carrier."""
    if 'encoded' not in request.files:
        return jsonify({"error": "Please select an image to decode."}), 400

    encoded_file = request.files['encoded']
    if encoded_file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    encoded_path = save_file(encoded_file)
    if not encoded_path:
        return jsonify({"error": "Invalid file type."}), 400

    try:
        secret_image_obj = decode_image(encoded_path)
        output_filename = f"extracted_image_{uuid.uuid4()}.png"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        secret_image_obj.save(output_path, "PNG")
        
        return send_file(output_path, as_attachment=True, download_name=output_filename)
    except Exception as e:
        return jsonify({"error": f"Failed to decode image: {e}"}), 500

@app.route('/api/help', methods=['GET'])
def get_help_text():
    """API endpoint to provide the help text content to the frontend."""
    return jsonify({
        "title_what_it_does": help_text.title_what_it_does,
        "text_what_it_does": help_text.text_what_it_does,
        "title_how_to_use": help_text.title_how_to_use,
        "text_how_to_use": help_text.text_how_to_use,
        "title_rules_restrictions": help_text.title_rules_restrictions,
        "text_rules_restrictions": help_text.text_rules_restrictions,
    })


if __name__ == '__main__':
    app.run(port=5000, debug=True)

