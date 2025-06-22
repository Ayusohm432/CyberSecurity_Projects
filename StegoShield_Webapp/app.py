from flask import Flask, render_template, request, send_from_directory
import os
from steganography import encode_message, decode_message

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_PATH = 'static/output.png'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    image = request.files['image']
    message = request.form['message']
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)
    encode_message(image_path, message, OUTPUT_PATH)
    return render_template('index.html', download=True)

@app.route('/decode', methods=['POST'])
def decode():
    image = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)
    secret = decode_message(image_path)
    return render_template('index.html', secret=secret)

@app.route('/download')
def download():
    return send_from_directory('static', 'output.png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
