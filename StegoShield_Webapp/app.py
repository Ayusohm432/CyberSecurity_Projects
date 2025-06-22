import os
import uuid
from flask import Flask, render_template, request, send_from_directory, url_for, flash, redirect # type: ignore
from PIL import Image # type: ignore
from steganography import encode_message, decode_message, encode_image, decode_image
import help as help_text 
from markupsafe import Markup, escape

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages

# --- Configuration ---
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'webp', 'gif'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file_storage):
    """Saves a file with a unique name and returns its path."""
    if file_storage and allowed_file(file_storage.filename):
        filename = f"{uuid.uuid4()}_{file_storage.filename}"
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_storage.save(path)
        return path
    return None

# Custom filter to convert newlines to <br> tags
@app.template_filter('nl2br')
def nl2br(value):
    return Markup(value.replace('\n', '<br>\n'))

# --- Main Routes (Tabs) ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/decode-text')
def decode_text_page():
    return render_template('decode_text.html')

@app.route('/encode-image')
def encode_image_page():
    return render_template('encode_image.html')

@app.route('/decode-image')
def decode_image_page():
    return render_template('decode_image.html')

@app.route('/help')
def help_page():
    return render_template('help.html', help=help_text)


# --- Processing Logic ---
@app.route('/encode-text', methods=['POST'])
def handle_encode_text():
    if 'carrier' not in request.files or 'message' not in request.form:
        flash("Carrier image and message are required.", "error")
        return redirect(url_for('index'))

    carrier_file = request.files['carrier']
    message = request.form['message']

    if carrier_file.filename == '' or not message:
        flash("Please select a carrier image and enter a message.", "error")
        return redirect(url_for('index'))

    carrier_path = save_file(carrier_file)
    if not carrier_path:
        flash("Invalid file type. Please use PNG, JPG, JPEG, or BMP.", "error")
        return redirect(url_for('index'))

    try:
        encoded_image_obj = encode_message(carrier_path, message)
        output_filename = f"encoded_{uuid.uuid4()}.png"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        encoded_image_obj.save(output_path, "PNG")

        return render_template("result.html",
                               title="Text Encoded Successfully",
                               original_image=url_for('static', filename=os.path.relpath(carrier_path, 'static')),
                               processed_image=url_for('static', filename=os.path.relpath(output_path, 'static')),
                               original_title="Original Carrier Image",
                               processed_title="Image with Hidden Message (Stego Image)",
                               download_url=url_for('static', filename=os.path.relpath(output_path, 'static')))
    except Exception as e:
        flash(f"An error occurred during encoding: {e}", "error")
        return redirect(url_for('index'))

@app.route('/decode-text', methods=['POST'])
def handle_decode_text():
    if 'encoded' not in request.files:
        flash("Please select an image to decode.", "error")
        return redirect(url_for('decode_text_page'))

    encoded_file = request.files['encoded']
    if encoded_file.filename == '':
        flash("No file selected.", "error")
        return redirect(url_for('decode_text_page'))

    encoded_path = save_file(encoded_file)
    if not encoded_path:
        flash("Invalid file type.", "error")
        return redirect(url_for('decode_text_page'))

    try:
        secret_message = decode_message(encoded_path)
        return render_template("result.html",
                               title="Message Extracted Successfully",
                               secret_message=secret_message)
    except Exception as e:
        flash(f"Failed to decode message: {e}. The image may not contain a valid message or might be corrupted.", "error")
        return redirect(url_for('decode_text_page'))

@app.route('/encode-image', methods=['POST'])
def handle_encode_image():
    if 'carrier' not in request.files or 'secret' not in request.files:
        flash("Both carrier and secret images are required.", "error")
        return redirect(url_for('encode_image_page'))

    carrier_file = request.files['carrier']
    secret_file = request.files['secret']

    if carrier_file.filename == '' or secret_file.filename == '':
        flash("Please select both a carrier and a secret image.", "error")
        return redirect(url_for('encode_image_page'))

    carrier_path = save_file(carrier_file)
    secret_path = save_file(secret_file)

    if not carrier_path or not secret_path:
        flash("Invalid file type for one or both images.", "error")
        return redirect(url_for('encode_image_page'))

    try:
        encoded_image_obj = encode_image(carrier_path, secret_path)
        output_filename = f"encoded_image_{uuid.uuid4()}.png"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        encoded_image_obj.save(output_path, "PNG")

        return render_template("result.html",
                               title="Image Hidden Successfully",
                               original_image=url_for('static', filename=os.path.relpath(carrier_path, 'static')),
                               processed_image=url_for('static', filename=os.path.relpath(output_path, 'static')),
                               original_title="Original Carrier Image",
                               processed_title="Image with Hidden Image (Stego Image)",
                               download_url=url_for('static', filename=os.path.relpath(output_path, 'static')))
    except Exception as e:
        flash(f"An error occurred during image encoding: {e}", "error")
        return redirect(url_for('encode_image_page'))

@app.route('/decode-image', methods=['POST'])
def handle_decode_image():
    if 'encoded' not in request.files:
        flash("Please select an image to decode.", "error")
        return redirect(url_for('decode_image_page'))

    encoded_file = request.files['encoded']
    if encoded_file.filename == '':
        flash("No file selected.", "error")
        return redirect(url_for('decode_image_page'))

    encoded_path = save_file(encoded_file)
    if not encoded_path:
        flash("Invalid file type.", "error")
        return redirect(url_for('decode_image_page'))

    try:
        secret_image_obj = decode_image(encoded_path)
        output_filename = f"extracted_{uuid.uuid4()}.png"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        secret_image_obj.save(output_path, "PNG")

        return render_template("result.html",
                               title="Image Extracted Successfully",
                               original_image=url_for('static', filename=os.path.relpath(encoded_path, 'static')),
                               processed_image=url_for('static', filename=os.path.relpath(output_path, 'static')),
                               original_title="Encoded Carrier Image",
                               processed_title="Extracted Secret Image")
    except Exception as e:
        flash(f"Failed to decode image: {e}. The file may not be a valid StegoShield image or is corrupted.", "error")
        return redirect(url_for('decode_image_page'))

if __name__ == '__main__':
    app.run(debug=True)