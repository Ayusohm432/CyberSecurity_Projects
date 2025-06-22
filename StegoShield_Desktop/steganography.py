from PIL import Image
from base64 import b64encode, b64decode

def _str_to_binary(s):
    """Converts a string to its binary representation."""
    return ''.join(format(ord(c), '08b') for c in s)

def _embed_data(image, data_to_embed):
    """Embeds a stream of binary data into an image's LSBs."""
    if len(data_to_embed) > len(image.getdata()) * 3:
        raise ValueError("Data is too large to hide in the carrier image.")

    data_iter = iter(data_to_embed)
    new_data = []
    for pixel in image.getdata():
        new_pixel = list(pixel)
        try:
            for i in range(3):  # For R, G, B channels
                bit = next(data_iter)
                new_pixel[i] = new_pixel[i] & ~1 | int(bit)
        except StopIteration:
            # No more data to hide
            new_data.append(tuple(new_pixel))
            break
        new_data.append(tuple(new_pixel))

    # Append the rest of the original pixels
    new_data.extend(image.getdata())
    # Truncate to the original image size
    new_data = new_data[:len(image.getdata())]

    image.putdata(new_data)
    return image

def _extract_bits(image, num_bits):
    """Extracts a specific number of bits from an image's LSBs."""
    bits = ""
    for pixel in image.getdata():
        for color_val in pixel[:3]:
            bits += str(color_val & 1)
            if len(bits) == num_bits:
                return bits
    return bits

def encode_message(image_path, message):
    """Encodes a text message into an image using length prefixing."""
    img = Image.open(image_path).convert("RGB")
    
    # Payload format: [Type Bit '0'] + [Message Content]
    payload_str = b64encode(message.encode()).decode()
    binary_payload = "0" + _str_to_binary(payload_str)

    # Prefix the payload with its 32-bit length
    binary_length = f'{len(binary_payload):032b}'
    data_to_embed = binary_length + binary_payload
    
    return _embed_data(img, data_to_embed)

def decode_message(image_path):
    """Decodes a text message from an image using length prefixing."""
    img = Image.open(image_path).convert("RGB")
    
    # 1. Extract the 32-bit length prefix
    binary_length_str = _extract_bits(img, 32)
    if len(binary_length_str) < 32:
        raise ValueError("Cannot extract message: Invalid or not an encoded image.")
    payload_length = int(binary_length_str, 2)

    # 2. Extract the full payload
    data_to_extract = 32 + payload_length
    binary_data = _extract_bits(img, data_to_extract)

    # 3. Get the payload part and validate
    binary_payload = binary_data[32:]
    if len(binary_payload) < payload_length:
        raise ValueError("Message data is corrupt or incomplete.")

    # 4. Check type bit and decode
    if not binary_payload.startswith("0"):
        raise ValueError("Encoded data is not a text message.")
    
    binary_payload_str_only = binary_payload[1:]
    byte_data = [binary_payload_str_only[i:i+8] for i in range(0, len(binary_payload_str_only), 8)]
    raw_chars = ''.join(chr(int(byte, 2)) for byte in byte_data)

    return b64decode(raw_chars.encode()).decode()

def encode_image(carrier_path, secret_path):
    """Encodes an image into another image using length prefixing."""
    carrier_img = Image.open(carrier_path).convert("RGB")
    secret_img = Image.open(secret_path).convert("RGB")
    w, h = secret_img.size

    # Payload format: [Type '1'] + [Header Len (16b)] + [Header] + [Pixel Data]
    header_str = f"{w}x{h}"
    binary_header = _str_to_binary(header_str)
    binary_header_len = f'{len(binary_header):016b}'
    binary_pixels = ''.join(f'{r:08b}{g:08b}{b:08b}' for r, g, b in secret_img.getdata())
    
    binary_payload = "1" + binary_header_len + binary_header + binary_pixels
    
    # Prefix the payload with its 32-bit length
    binary_length = f'{len(binary_payload):032b}'
    data_to_embed = binary_length + binary_payload

    return _embed_data(carrier_img, data_to_embed)

def decode_image(encoded_path):
    """Decodes an image from another image using length prefixing."""
    img = Image.open(encoded_path).convert("RGB")
    
    # 1. Extract the 32-bit length prefix for the whole payload
    binary_length_str = _extract_bits(img, 32)
    if len(binary_length_str) < 32:
        raise ValueError("Cannot extract image: Invalid or not an encoded image.")
    payload_length = int(binary_length_str, 2)

    # 2. Extract the full payload
    data_to_extract = 32 + payload_length
    binary_data = _extract_bits(img, data_to_extract)

    # 3. Get the payload part and validate
    binary_payload = binary_data[32:]
    if len(binary_payload) < payload_length:
        raise ValueError("Image data is corrupt or incomplete.")

    # 4. Check type bit
    if not binary_payload.startswith("1"):
        raise ValueError("Encoded data is not an image.")

    # 5. Parse the payload: [Type '1'] + [Header Len (16b)] + [Header] + [Pixel Data]
    try:
        header_len_str = binary_payload[1:17]
        header_len = int(header_len_str, 2)
        
        header_end_index = 17 + header_len
        binary_header = binary_payload[17:header_end_index]
        binary_pixels = binary_payload[header_end_index:]

        # Decode header to get dimensions
        raw_header = ''.join(chr(int(binary_header[i:i+8], 2)) for i in range(0, len(binary_header), 8))
        w_str, h_str = raw_header.split('x')
        w, h = int(w_str), int(h_str)

    except (ValueError, IndexError):
        raise ValueError("Image header data is corrupt.")

    # 6. Reconstruct the image from the pixel data
    pixels = []
    expected_pixel_bits = w * h * 24
    if len(binary_pixels) < expected_pixel_bits:
        raise ValueError(f"Image pixel data is incomplete. Expected {expected_pixel_bits} bits, found {len(binary_pixels)}.")

    for i in range(0, expected_pixel_bits, 24):
        pixel_binary = binary_pixels[i:i+24]
        r = int(pixel_binary[0:8], 2)
        g = int(pixel_binary[8:16], 2)
        b = int(pixel_binary[16:24], 2)
        pixels.append((r, g, b))
        
    secret_img = Image.new("RGB", (w, h))
    secret_img.putdata(pixels)
    return secret_img