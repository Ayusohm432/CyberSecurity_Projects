import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from steganography import encode_message, decode_message, encode_image, decode_image
import help as help_text

class StegoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("StegoShield Desktop")
        self.geometry("600x450")

        # --- Style Configuration ---
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TButton", padding=6, relief="flat", font=("Segoe UI", 10))
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("SubHeader.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=[10, 5])

        # --- Main Layout ---
        header_frame = ttk.Frame(self, padding=10)
        header_frame.pack(fill="x")
        ttk.Label(header_frame, text="StegoShield", style="Header.TLabel").pack()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # --- Create Tabs ---
        self.create_encode_text_tab()
        self.create_decode_text_tab()
        self.create_encode_image_tab()
        self.create_decode_image_tab()
        self.create_help_tab()
        self.create_exit_tab()
        self.protocol("WM_DELETE_WINDOW", self.confirm_exit)

    def create_tab_frame(self, tab_name):
        frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(frame, text=tab_name)
        return frame

    # --- TAB 1: ENCODE TEXT ---
    def create_encode_text_tab(self):
        frame = self.create_tab_frame("Encode Text")
        carrier_path = tk.StringVar()
        message = tk.StringVar()

        ttk.Label(frame, text="Select an image to hide your message in.").grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")
        ttk.Label(frame, text="Carrier Image:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=carrier_path, width=50).grid(row=1, column=1, sticky="ew")
        ttk.Button(frame, text="Browse...", command=lambda: self.browse_file(carrier_path)).grid(row=1, column=2, padx=5)

        ttk.Label(frame, text="Secret Message:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=message, width=50).grid(row=2, column=1, sticky="ew")

        ttk.Button(frame, text="Preview & Hide Message", command=lambda: self.perform_encode_text(carrier_path.get(), message.get())).grid(row=3, column=1, pady=20)
        frame.columnconfigure(1, weight=1)

    # --- TAB 2: DECODE TEXT ---
    def create_decode_text_tab(self):
        frame = self.create_tab_frame("Decode Text")
        encoded_path = tk.StringVar()

        ttk.Label(frame, text="Select an image to extract a hidden message from.").grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")
        ttk.Label(frame, text="Encoded Image:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=encoded_path, width=50).grid(row=1, column=1, sticky="ew")
        ttk.Button(frame, text="Browse...", command=lambda: self.browse_file(encoded_path)).grid(row=1, column=2, padx=5)

        ttk.Button(frame, text="Extract Message", command=lambda: self.perform_decode_text(encoded_path.get())).grid(row=2, column=1, pady=20)
        frame.columnconfigure(1, weight=1)

    # --- TAB 3: ENCODE IMAGE ---
    def create_encode_image_tab(self):
        frame = self.create_tab_frame("Encode Image")
        carrier_path = tk.StringVar()
        secret_path = tk.StringVar()

        ttk.Label(frame, text="Hide one image inside another.").grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")
        
        ttk.Label(frame, text="Carrier Image:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=carrier_path, width=50).grid(row=1, column=1, sticky="ew")
        ttk.Button(frame, text="Browse...", command=lambda: self.browse_file(carrier_path)).grid(row=1, column=2, padx=5)

        ttk.Label(frame, text="Secret Image:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=secret_path, width=50).grid(row=2, column=1, sticky="ew")
        ttk.Button(frame, text="Browse...", command=lambda: self.browse_file(secret_path)).grid(row=2, column=2, padx=5)

        ttk.Button(frame, text="Preview & Hide Image", command=lambda: self.perform_encode_image(carrier_path.get(), secret_path.get())).grid(row=3, column=1, pady=20)
        frame.columnconfigure(1, weight=1)

    # --- TAB 4: DECODE IMAGE ---
    def create_decode_image_tab(self):
        frame = self.create_tab_frame("Decode Image")
        encoded_path = tk.StringVar()

        ttk.Label(frame, text="Select an image to extract a hidden image from.").grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")
        ttk.Label(frame, text="Encoded Image:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=encoded_path, width=50).grid(row=1, column=1, sticky="ew")
        ttk.Button(frame, text="Browse...", command=lambda: self.browse_file(encoded_path)).grid(row=1, column=2, padx=5)

        ttk.Button(frame, text="Extract Image", command=lambda: self.perform_decode_image(encoded_path.get())).grid(row=2, column=1, pady=20)
        frame.columnconfigure(1, weight=1)
        
    # --- TAB 5: HELP ---
    def create_help_tab(self):
        tab_frame = self.create_tab_frame("Help")
        tab_frame.grid_rowconfigure(0, weight=1)
        tab_frame.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(tab_frame)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding=20)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # --- Add Content from help_text module ---
        ttk.Label(scrollable_frame, text=help_text.title_what_it_does, style="SubHeader.TLabel").pack(anchor="w", pady=(0, 5))
        ttk.Label(scrollable_frame, text=help_text.text_what_it_does, wraplength=480, justify="left").pack(anchor="w", pady=(0, 20), fill='x')

        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=5)

        ttk.Label(scrollable_frame, text=help_text.title_how_to_use, style="SubHeader.TLabel").pack(anchor="w", pady=(5, 5))
        ttk.Label(scrollable_frame, text=help_text.text_how_to_use, wraplength=480, justify="left").pack(anchor="w", pady=(0, 20), fill='x')
        
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=5)

        ttk.Label(scrollable_frame, text=help_text.title_rules_restrictions, style="SubHeader.TLabel").pack(anchor="w", pady=(5, 5))
        ttk.Label(scrollable_frame, text=help_text.text_rules_restrictions, wraplength=480, justify="left").pack(anchor="w", fill='x')


    # --- TAB 6: EXIT ---
    def create_exit_tab(self):
        frame = self.create_tab_frame("Exit")
        
        # Center the button in the frame
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        exit_button = ttk.Button(frame, text="Exit Application", command=self.confirm_exit, style="TButton")
        exit_button.grid(row=0, column=0)

    def confirm_exit(self):
        """Shows a confirmation dialog and exits the app if confirmed."""
        if messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit StegoShield?"):
            self.destroy()

    # --- Core Logic Functions ---
    def browse_file(self, path_var):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp"), ("All Files", "*.*")])
        if path:
            path_var.set(path)
    
    def generate_output_path(self, input_path, prefix):
        base_dir = os.path.dirname(input_path)
        original_name = os.path.splitext(os.path.basename(input_path))[0]
        filename = f"{prefix}_{original_name}.png"
        counter = 1
        # Check for existence to suggest a unique name
        while os.path.exists(os.path.join(base_dir, filename)):
            filename = f"{prefix}_{original_name}_{counter}.png"
            counter += 1
        return os.path.join(base_dir, filename)

    def perform_encode_text(self, carrier_path, message):
        if not carrier_path or not message:
            messagebox.showerror("Error", "Carrier image and message must be provided.")
            return
        try:
            # Generate the default output path with the "encoded" prefix
            suggested_path = self.generate_output_path(carrier_path, "encoded")
            
            original_image = Image.open(carrier_path)
            encoded_image = encode_message(carrier_path, message)

            self.show_preview_dialog(
                original_image, 
                encoded_image, 
                "Preview: Encoded Text",
                initial_path=suggested_path
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encode message: {e}")

    def perform_decode_text(self, encoded_path):
        if not encoded_path:
            messagebox.showerror("Error", "Please select an encoded image file.")
            return
        try:
            result = decode_message(encoded_path)
            messagebox.showinfo("Decoded Message", result)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decode message: {e}")

    def perform_encode_image(self, carrier_path, secret_path):
        if not carrier_path or not secret_path:
            messagebox.showerror("Error", "Both carrier and secret images must be selected.")
            return
        try:
            # Generate the default output path with the "encoded" prefix
            suggested_path = self.generate_output_path(carrier_path, "encoded")
            
            original_image = Image.open(carrier_path)
            encoded_image = encode_image(carrier_path, secret_path)

            self.show_preview_dialog(
                original_image, 
                encoded_image, 
                "Preview: Encoded Image",
                initial_path=suggested_path
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encode image: {e}")
    
    def perform_decode_image(self, encoded_path):
        if not encoded_path:
            messagebox.showerror("Error", "Please select an encoded image file.")
            return
        try:
            encoded_img = Image.open(encoded_path)
            secret_img = decode_image(encoded_path)
            self.show_preview_dialog(encoded_img, secret_img, "Preview: Extracted Image", allow_save=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decode image: {e}")

    def show_preview_dialog(self, img1, img2, title, allow_save=True, initial_path=""):
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("800x475")
        dialog.transient(self)
        dialog.grab_set()

        titles = ["Original Image", "Processed Image"]
        if "Extracted" in title:
            titles = ["Encoded Image", "Extracted Secret Image"]

        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill="both", expand=True)

        for idx, (img, t) in enumerate(zip([img1, img2], titles)):
            col_frame = ttk.Frame(frame)
            col_frame.grid(row=0, column=idx, padx=10, pady=5, sticky="n")
            
            ttk.Label(col_frame, text=t, font=("Segoe UI", 12, "bold")).pack(pady=(0, 10))
            
            img_resized = img.resize((350, 350), Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(img_resized)
            
            label = ttk.Label(col_frame, image=tk_img)
            label.image = tk_img
            label.pack()

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        
        button_frame = ttk.Frame(dialog, padding=(0, 10, 0, 0))
        button_frame.pack(fill="x", side="bottom")

        def save_action():
            # Use the generated path to set the initial directory and filename
            initial_dir = os.path.dirname(initial_path)
            initial_file = os.path.basename(initial_path)

            path = filedialog.asksaveasfilename(
                title="Save Encoded Image",
                initialdir=initial_dir,
                initialfile=initial_file,
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All Files", "*.*")]
            )
            if path:
                try:
                    img2.save(path, "PNG")
                    messagebox.showinfo("Success", f"Image saved successfully to:\n{path}", parent=dialog)
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Save Error", f"Failed to save image: {e}", parent=dialog)

        if allow_save:
            ttk.Button(button_frame, text="Save Image...", command=save_action).pack(side="left", padx=20)
            ttk.Button(button_frame, text="Exit", command=dialog.destroy).pack(side="right", padx=20)
        else:
            ttk.Button(button_frame, text="Close", command=dialog.destroy).pack()

        button_frame.pack_propagate(False)
        button_frame.configure(height=50)


if __name__ == "__main__":
    app = StegoApp()
    app.mainloop()