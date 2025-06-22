import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
from steganography import encode_message, decode_message, encode_image, decode_image
import os
from PIL import Image, ImageTk

# --- UI Logic Functions ---
def browse_image():
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp"), ("All Files", "*.*")])
    if path:
        image_path.set(path)

def browse_secret_image():
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp"), ("All Files", "*.*")])
    if path:
        secret_image_path.set(path)

def generate_output_path(input_path, prefix):
    base_dir = os.path.dirname(input_path)
    original_name = os.path.splitext(os.path.basename(input_path))[0]
    filename = f"{prefix}_{original_name}.png"
    counter = 1
    while os.path.exists(os.path.join(base_dir, filename)):
        filename = f"{prefix}_{original_name}_{counter}.png"
        counter += 1
    return os.path.join(base_dir, filename)

def show_image_dialog(images, titles):
    dialog = tk.Toplevel()
    dialog.title("Preview")
    dialog.geometry("800x400")

    frame = ttk.Frame(dialog, padding=10)
    frame.pack(fill="both", expand=True)

    for idx, (img, title) in enumerate(zip(images, titles)):
        tk.Label(frame, text=title).grid(row=0, column=idx)
        img_resized = img.resize((350, 350), Image.LANCZO)
        tk_img = ImageTk.PhotoImage(img_resized)
        label = tk.Label(frame, image=tk_img)
        label.image = tk_img
        label.grid(row=1, column=idx, padx=10)

    def save():
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if path:
            images[-1].save(path)
            dialog.destroy()

    ttk.Button(dialog, text="Save", command=save).pack(side="left", padx=20, pady=10)
    ttk.Button(dialog, text="Exit", command=dialog.destroy).pack(side="right", padx=20, pady=10)

def perform_hide(operation):
    try:
        if not image_path.get():
            raise ValueError("Carrier image must be selected")

        output_file = ""
        if operation == "text":
            if not message.get():
                raise ValueError("Message field cannot be empty")
            output_file = generate_output_path(image_path.get(), "encoded")
            encode_message(image_path.get(), message.get(), output_file)
        elif operation == "image":
            if not secret_image_path.get():
                raise ValueError("Secret image must be selected")
            output_file = generate_output_path(image_path.get(), "encodedimg")
            encode_image(image_path.get(), secret_image_path.get(), output_file)

        original = Image.open(image_path.get())
        encoded = Image.open(output_file)
        show_image_dialog([original, encoded], ["Original", "Encoded"])
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

def extract_image():
    try:
        if not image_path.get():
            raise ValueError("Please select an encoded image")

        img = Image.open(image_path.get())
        width, height = img.size
        secret = decode_image(image_path.get(), (width, height))
        show_image_dialog([img, secret], ["Encoded", "Extracted"])
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- UI Setup ---
root = tk.Tk()
root.title("StegoShield Desktop")

frame = ttk.Frame(root, padding=20)
frame.grid()

ttk.Label(frame, text="StegoShield", font=("Segoe UI", 16, "bold")).grid(column=0, row=0, columnspan=3, pady=10)

image_path = tk.StringVar()
message = tk.StringVar()
secret_image_path = tk.StringVar()
mode = tk.StringVar(value="")

# Buttons to toggle mode
ttk.Button(frame, text="Hide Text", command=lambda: switch_mode("text")).grid(column=0, row=1, pady=5)
ttk.Button(frame, text="Hide Image", command=lambda: switch_mode("image")).grid(column=1, row=1, pady=5)

# Text mode widgets
text_widgets = []
text_widgets.append(ttk.Label(frame, text="Carrier Image:"))
text_widgets.append(ttk.Entry(frame, textvariable=image_path, width=40))
text_widgets.append(ttk.Button(frame, text="Browse", command=browse_image))
text_widgets.append(ttk.Label(frame, text="Secret Message:"))
text_widgets.append(ttk.Entry(frame, textvariable=message, width=40))
text_widgets.append(ttk.Button(frame, text="Hide Message", command=lambda: perform_hide("text")))
text_widgets.append(ttk.Button(frame, text="Extract Message", command=extract_message))

# Image mode widgets
image_widgets = []
image_widgets.append(ttk.Label(frame, text="Carrier Image:"))
image_widgets.append(ttk.Entry(frame, textvariable=image_path, width=40))
image_widgets.append(ttk.Button(frame, text="Browse", command=browse_image))
image_widgets.append(ttk.Label(frame, text="Secret Image:"))
image_widgets.append(ttk.Entry(frame, textvariable=secret_image_path, width=40))
image_widgets.append(ttk.Button(frame, text="Browse", command=browse_secret_image))
image_widgets.append(ttk.Button(frame, text="Hide Image", command=lambda: perform_hide("image")))
image_widgets.append(ttk.Button(frame, text="Extract Image", command=extract_image))

def switch_mode(selected_mode):
    for widget in text_widgets + image_widgets:
        widget.grid_remove()

    if selected_mode == "text":
        for i, widget in enumerate(text_widgets):
            widget.grid(column=i % 3, row=2 + i // 3, padx=2, pady=2, sticky='w')
    elif selected_mode == "image":
        for i, widget in enumerate(image_widgets):
            widget.grid(column=i % 3, row=2 + i // 3, padx=2, pady=2, sticky='w')

    mode.set(selected_mode)

root.mainloop()