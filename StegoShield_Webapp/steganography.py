from PIL import Image

def encode_message(image_path, message, output_path):
    img = Image.open(image_path)
    binary_message = ''.join(format(ord(c), '08b') for c in message) + '1111111111111110'
    data = iter(img.getdata())

    new_data = []
    for i in range(0, len(binary_message), 3):
        pixels = list(next(data))
        for j in range(3):
            if i + j < len(binary_message):
                pixels[j] = pixels[j] & ~1 | int(binary_message[i + j])
        new_data.append(tuple(pixels))
    img.putdata(new_data + list(data))
    img.save(output_path)

def decode_message(image_path):
    img = Image.open(image_path)
    binary_data = ''
    for pixel in img.getdata():
        for color in pixel[:3]:
            binary_data += str(color & 1)
            if binary_data[-16:] == '1111111111111110':
                return ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data) - 16, 8))
    return ''
