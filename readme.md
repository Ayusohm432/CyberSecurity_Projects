🛡️ StegoShield: A Steganography Suite

Welcome to StegoShield, a comprehensive steganography tool designed to hide data in plain sight. This project provides two distinct applications—a native Desktop GUI and a browser-based WebApp—both powered by the same core steganography engine.

Steganography is the art of concealing a message, image, or file within another message, image, or file. StegoShield implements this by subtly altering the pixel data of a carrier image to embed your secret data, making it visually imperceptible.

✨ Core Features (Both Applications)
Encode Text in Image: Hide a secret text message within a standard image file.

Decode Text from Image: Extract a hidden text message from a StegoShield-encoded image.

Encode Image in Image: Conceal a smaller secret image inside a larger carrier image.

Decode Image from Image: Recover a hidden image from its carrier.

Lossless Output: All encoded images are saved in the PNG format to ensure the integrity of the hidden data.

🖥️ StegoShield Desktop
A user-friendly graphical application built with Python and Tkinter for a native desktop experience.

Desktop Features
Intuitive Tabbed UI: Easy-to-navigate interface separating each function.

Side-by-Side Previews: Compare original and processed images before saving the final result.

Integrated Help Guide: A built-in help tab explains the application's functionality and rules.

File Dialogs: Simple browsing for local file selection and saving.

Setup & Run (Desktop)
1. Prerequisites:

Ensure you have Python 3 installed.

2. Navigate to the Desktop Directory:

cd path/to/StegoShield_Desktop

3. Create a Virtual Environment (Recommended):

# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

4. Install Dependencies:
The only external library required is Pillow.

pip install Pillow

5. Run the Application:

python main.py

🌐 StegoShield WebApp
A web-based version built with Python and Flask, bringing the power of StegoShield to your browser.

WebApp Features
Modern Web Interface: Clean, responsive, and accessible from any modern web browser.

Server-Side Processing: All steganography operations are handled securely on the server.

Result Previews: Displays original and processed images on a results page.

Direct Downloads: Download your newly encoded images directly from the browser.

Setup & Run (WebApp)
1. Prerequisites:

Ensure you have Python 3 installed.

2. Navigate to the WebApp Directory:

cd path/to/StegoShield_WebApp

3. Create a Virtual Environment (Recommended):

# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

4. Install Dependencies:
Install all required packages using pip.

pip install Flask Pillow markupsafe

5. Run the Application:

python app.py

The application will be accessible in your web browser at: http://127.0.0.1:5000

📖 How Steganography Works in StegoShield
The core steganography.py script uses the Least Significant Bit (LSB) technique. Here's a simplified overview:

Data Conversion: The secret message or image is first converted into a binary string (a sequence of 1s and 0s).

Payload Creation: To ensure data can be correctly decoded, a payload is constructed containing:

A type bit (0 for text, 1 for image).

Header data (e.g., the length of the message or dimensions of the secret image).

The actual binary data of the secret.

Embedding: The application