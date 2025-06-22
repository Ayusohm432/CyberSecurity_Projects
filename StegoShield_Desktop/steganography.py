from PIL import Image
import os
from base64 import b64encode, b64decode

def encode_message(image_path, message, output_path):
    img = Image.open(image_path).convert("RGB")
    encoded_message = b64encode(message.encode()).decode()
    binary_message = ''.join(format(ord(c), '08b') for c in encoded_message) + '1111111111111110'
    data = iter(img.getdata())

    new_data = []
    for i in range(0, len(binary_message), 3):
        pixels = list(next(data))
        for j in range(3):
            if i + j < len(binary_message):
                pixels[j] = pixels[j] & ~1 | int(binary_message[i + j])
        new_data.append(tuple(pixels))

    new_data.extend(data)
    img.putdata(new_data)
    img.save(output_path, format="PNG")

def decode_message(image_path):
    img = Image.open(image_path).convert("RGB")
    binary_data = ''
    for pixel in img.getdata():
        for color in pixel[:3]:
            binary_data += str(color & 1)
            if binary_data[-16:] == '1111111111111110':
                raw_chars = [chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data) - 16, 8)]
                decoded_base64 = ''.join(raw_chars)
                try:
                    return b64decode(decoded_base64.encode()).decode()
                except Exception:
                    return '[Message decoding failed: Invalid encoding]'
    return '[No hidden message found]'

def encode_image(carrier_path, secret_path, output_path):
    carrier = Image.open(carrier_path).convert("RGB")
    secret = Image.open(secret_path).convert("RGB")

    carrier_data = list(carrier.getdata())
    secret_data = list(secret.getdata())

    if len(secret_data) * 3 > len(carrier_data):
        raise ValueError("Secret image is too large to hide in carrier image")

    binary_secret = ''.join(f'{r:08b}{g:08b}{b:08b}' for (r, g, b) in secret_data) + '1111111111111110'

    new_data = []
    data_iter = iter(carrier_data)
    for i in range(0, len(binary_secret), 3):
        pixel = list(next(data_iter))
        for j in range(3):
            if i + j < len(binary_secret):
                pixel[j] = pixel[j] & ~1 | int(binary_secret[i + j])
        new_data.append(tuple(pixel))

    new_data.extend(data_iter)
    carrier.putdata(new_data)
    carrier.save(output_path, format="PNG")

def decode_image(encoded_path, size):
    img = Image.open(encoded_path).convert("RGB")
    binary_data = ''
    for pixel in img.getdata():
        for color in pixel[:3]:
            binary_data += str(color & 1)
            if binary_data[-16:] == '1111111111111110':
                break

    binary_data = binary_data[:-16]
    pixels = []
    for i in range(0, len(binary_data), 24):
        r = int(binary_data[i:i+8], 2)
        g = int(binary_data[i+8:i+16], 2)
        b = int(binary_data[i+16:i+24], 2)
        pixels.append((r, g, b))

    secret_img = Image.new("RGB", size)
    secret_img.putdata(pixels[:size[0]*size[1]])
    return secret_img
