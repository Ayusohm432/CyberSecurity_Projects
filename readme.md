# 🛡️ StegoShield: A Steganography Suite

Welcome to StegoShield, a comprehensive steganography tool designed to hide data in plain sight. This project provides three distinct applications, all powered by the same core Python steganography engine.

Steganography is the art of concealing a message, image, or file within another message, image, or file. StegoShield implements this by subtly altering the pixel data of a carrier image to embed your secret data, making it visually imperceptible.

## ✨ Core Features

-   **Encode Text in Image**: Hide a secret text message within a standard image file.
-   **Decode Text from Image**: Extract a hidden text message from a StegoShield-encoded image.
-   **Encode Image in Image**: Conceal a smaller secret image inside a larger carrier image.
-   **Decode Image from Image**: Recover a hidden image from its carrier.
-   **Lossless Output**: All encoded images are saved in the PNG format to ensure the integrity of the hidden data.

---

## 🖥️ 1. StegoShield Desktop

A user-friendly graphical application built with Python and Tkinter for a native desktop experience.

### Desktop Features

-   **Intuitive Tabbed UI**: Easy-to-navigate interface separating each function.
-   **Side-by-Side Previews**: Compare original and processed images before saving the final result.
-   **Integrated Help Guide**: A built-in help tab explains the application's functionality and rules.

### Setup & Run (Desktop)

1.  **Navigate to the Directory**: `cd path/to/StegoShield_Desktop`
2.  **Create Virtual Environment & Activate**:
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install Dependencies**: `pip install Pillow`
4.  **Run Application**: `python main.py`

---

## 🌐 2. StegoShield WebApp

A traditional web version built with Python and Flask, where the server renders HTML templates.

### WebApp Features

-   **Server-Side Rendering**: A classic web application model using Flask and Jinja2 templates.
-   **Modern Web Interface**: Clean, responsive, and accessible from any modern web browser.
-   **Result Previews**: Displays original and processed images on a results page.

### Setup & Run (WebApp)

1.  **Navigate to the Directory**: `cd path/to/StegoShield_WebApp`
2.  **Create Virtual Environment & Activate**
3.  **Install Dependencies**: `pip install Flask Pillow markupsafe`
4.  **Run Application**: `python app.py`
5.  **Access**: Open your browser to `http://127.0.0.1:5000`.

---

## 🚀 3. StegoShield Full-Stack (React + Flask)

A modern single-page application (SPA) featuring a React frontend that communicates with a Flask backend API.

### Full-Stack Features

-   **Decoupled Architecture**: A separate React frontend for a dynamic user experience and a Flask backend acting as a pure API.
-   **Client-Side Rendering**: Fast and responsive UI managed by React.
-   **API-Driven**: All operations are handled through API calls between the client and server.

### Setup & Run (Full-Stack)

Setting up the full-stack version requires running the backend and frontend servers simultaneously in **two separate terminals**.

#### **A. Run the Backend (The Kitchen)**

1.  **Navigate to the Backend Directory**:
    ```bash
    cd path/to/stegoshield_fullstack/backend
    ```
2.  **Create and Activate Virtual Environment**.
3.  **Install Python Dependencies**:
    ```bash
    pip install Flask Flask-Cors Pillow
    ```
4.  **Run the Flask Server**:
    ```bash
    python app.py
    ```
    ✅ The backend is now running on `http://localhost:5000`. **Leave this terminal open.**

#### **B. Run the Frontend (The Menu)**

1.  **Open a New Terminal**.
2.  **Navigate to the Frontend Directory**:
    ```bash
    cd path/to/stegoshield_fullstack/frontend
    ```
3.  **Install JavaScript Dependencies**:
    ```bash
    npm install
    ```
4.  **Run the React Client**:
    ```bash
    npm start
    ```
    ✅ The frontend will open automatically in your browser at `http://localhost:3000`.

---

## 📖 How Steganography Works in StegoShield

The core `steganography.py` script uses the **Least Significant Bit (LSB)** technique. Here's a simplified overview:

1.  **Data Conversion**: The secret message or image is first converted into a binary string (a sequence of 1s and 0s).
2.  **Payload Creation**: To ensure data can be correctly decoded, a payload is constructed containing a type bit (0 for text, 1 for image), header data (like length or dimensions), and the actual binary data.
3.  **Embedding**: The application iterates through the pixels of the carrier image, modifying the least significant bit of each color channel (Red, Green, and Blue) to store one bit from the payload.
4.  **Extraction**: The decoding process reverses this by reading the LSBs to reconstruct the payload and interpret the hidden data.
