# help.py

# This file contains the text content for the Help tab in the StegoShield application.

title_what_it_does = "What StegoShield Does"

text_what_it_does = (
    "StegoShield is a steganography tool that allows you to hide secret data within a standard image file. "
    "Steganography is the art of concealed communication; unlike cryptography, which scrambles a message, "
    "steganography hides the very existence of the message.\n\n"
    "This application embeds your secret (text or another image) into the pixel data of a 'carrier' image. "
    "The changes made to the carrier are so subtle that they are generally invisible to the naked eye, allowing "
    "you to store or transmit information secretly."
)

title_how_to_use = "How to Use This Application"

text_how_to_use = (
    "The application is organized into tabs for each function. Here is a guide for each one:\n\n"
    "1. Encode Text: This tab is for hiding a written message inside an image.\n"
    "   • Carrier Image: Click 'Browse...' to select the main image that will hide your secret. "
    "Larger images with more detail work best.\n"
    "   • Secret Message: Type or paste the text you wish to hide in this field.\n"
    "   • Preview & Hide Message: Click this button. A new window will show the original carrier and the new, "
    "encoded image side-by-side. If you are satisfied, click 'Save Image...' to save the result.\n\n"
    
    "2. Decode Text: Use this tab if you have received an image that you believe contains a hidden text message.\n"
    "   • Encoded Image: Click 'Browse...' and select the image you want to decode.\n"
    "   • Extract Message: Click this button. If a valid message encoded by StegoShield is found, it will be "
    "displayed in a pop-up window.\n\n"

    "3. Encode Image: This tab allows you to hide an entire image inside another one.\n"
    "   • Carrier Image: Select the main, visible image.\n"
    "   • Secret Image: Select the image you want to hide. Note the size restrictions below.\n"
    "   • Preview & Hide Image: This will show you the carrier and the final encoded image. Click 'Save Image...' "
    "to save the result. The secret image will not be visible.\n\n"

    "4. Decode Image: Use this to extract a hidden image from an encoded carrier.\n"
    "   • Encoded Image: Select the image you want to decode.\n"
    "   • Extract Image: Click this. A preview window will appear, showing the encoded image and the extracted "
    "secret image side-by-side."
)

title_rules_restrictions = "Important Rules & Restrictions"

text_rules_restrictions = (
    "Please read these points carefully to ensure the application works correctly.\n\n"
    "• Output File Format: All encoded images are saved in the PNG (.png) format. This is mandatory "
    "because steganography requires a lossless format. Saving an encoded image as a JPEG or other lossy "
    "formats will corrupt and destroy the hidden data.\n\n"
    
    "• Carrier Image Size (Capacity): The amount of data you can hide is directly limited by the size of the "
    "carrier image. A larger carrier image (with more pixels) has a higher capacity for storing secret data.\n\n"

    "• Secret Image Size Restriction: This is the most important rule. The secret image must be "
    "significantly smaller than the carrier image.\n"
    "   - Rule of Thumb: You need at least 8 pixels in the carrier image to hide just 1 pixel "
    "of the secret image.\n"
    "   - If you choose a secret image that is too large for the carrier, the application will show an "
    "error message.\n\n"
    
    "• Decoding Failures: If you attempt to decode an image and receive an error like 'Invalid or no "
    "hidden image data found,' it usually means one of the following:\n"
    "   1. The image was never encoded with StegoShield.\n"
    "   2. The image was encoded but was later saved as a JPEG or compressed in a way that corrupted the hidden data.\n"
    "   3. The file itself is corrupted."
)