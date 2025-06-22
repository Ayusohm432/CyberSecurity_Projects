import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from steganography import encode_message, decode_message
import os

def browse_image():
    path = filedialog.askopenfilename(filetypes=[
        ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp"),
        ("All Files", "*.*")
    ])
    if path:
        image_path.set(path)

def hide_message():
    try:
        if not image_path.get() or not message.get():
            raise ValueError("Image and message fields cannot be empty")
        base_dir = os.path.dirname(image_path.get())
        original_name = os.path.splitext(os.path.basename(image_path.get()))[0]
        filename = f"encoded_{original_name}.png"
        counter = 1
        while os.path.exists(os.path.join(base_dir, filename)):
            filename = f"encoded_{original_name}_{counter}.png"
            counter += 1
        output_file = os.path.join(base_dir, filename)
        encode_message(image_path.get(), message.get(), output_file)
        messagebox.showinfo("Success", f"Message hidden in:\n{output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def extract_message():
    try:
        if not image_path.get():
            raise ValueError("Please select an image file")
        result = decode_message(image_path.get())
        messagebox.showinfo("Decoded Message", result)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# UI Setup
root = tk.Tk()
root.title("StegoShield Desktop")

frame = ttk.Frame(root, padding=20)
frame.grid()

ttk.Label(frame, text="StegoShield: Hide Text in Image", font=("Segoe UI", 16, "bold")).grid(column=0, row=0, columnspan=3, pady=10)

image_path = tk.StringVar()
message = tk.StringVar()

ttk.Label(frame, text="Image Path:").grid(column=0, row=1, sticky='w')
ttk.Entry(frame, textvariable=image_path, width=40).grid(column=1, row=1)
ttk.Button(frame, text="Browse", command=browse_image).grid(column=2, row=1)

ttk.Label(frame, text="Secret Message:").grid(column=0, row=2, sticky='w')
ttk.Entry(frame, textvariable=message, width=40).grid(column=1, row=2, columnspan=2)

ttk.Button(frame, text="Hide Message", command=hide_message).grid(column=1, row=3, pady=10, sticky='w')
ttk.Button(frame, text="Extract Message", command=extract_message).grid(column=2, row=3, pady=10, sticky='e')

root.mainloop()
