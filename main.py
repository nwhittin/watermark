import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import PIL
from PIL import Image, ImageDraw

MAIN_WINDOW_WIDTH = 500
MAIN_WINDOW_HEIGHT = 450
IMG_EXTS = ".bmp .ico .jpeg .jpg .png"

temp_font_color = "#000000"


class Img:

    def __init__(self):
        # Placeholders to be filled by browse_images function
        self.filename = None
        self.file_ext = None
        self.image = None

    def open_image(self):
        try:
            self.image = Image.open(self.filename)
        except AttributeError:
            messagebox.showerror(title="File Error", message="Please select an image file.")


class Wmark:

    def __init__(self):
        self.text = "test"
        self.coords = (0, 0)
        self.font_color = temp_font_color


def browse_images():
    # Opens filedialog window allowing user to select an image file
    try:
        filename = filedialog.askopenfilename(
            initialdir="/",
            title="Select a file",
            filetypes=(("Image Files", IMG_EXTS), ("All Files", "*.*"))
        )
        display_filename = "".join(filename.split("/")[-1].split(".")[0:-1])
        image.file_ext = filename.split(".")[-1]
        new_filename = display_filename + "_edit"
        image.filename = filename
        image.open_image()

        # Display filename, allow editing of new filename field, and use of buttons
        current_label.config(state="normal")
        current_entry.config(state="normal")
        current_entry.delete(0, tk.END)
        current_entry.insert(0, display_filename)
        current_entry.config(state="disabled")
        new_label.config(state="normal")
        new_entry.config(state="normal")
        new_entry.delete(0, tk.END)
        new_entry.insert(0, new_filename)
        watermark_label.config(state="normal")
        watermark_entry.config(state="normal")
        watermark_entry.delete(0, tk.END)
        watermark_entry.insert(0, watermark.text)
        color_button.config(state="normal")
        preview_button.config(state="normal")
        reset_button.config(state="normal")
    except PIL.UnidentifiedImageError:
        # Catches non-image file selected by user
        messagebox.showerror(title="File Type Error", message="Please select an image file.")
    except PermissionError:
        # Catches system file or elevated-access file selected by user
        messagebox.showerror(
            title="There Was a Problem",
            message="There was a problem opening the file. Please try again.",
        )


def choose_font_color():
    global temp_font_color
    temp_font_color = colorchooser.askcolor(title="Choose Font Color")[-1]
    watermark.font_color = temp_font_color


def preview_image():
    image.open_image()
    # Watermarks the image with the selected font and text options and opens a preview window
    watermark.text = watermark_entry.get()
    draw = ImageDraw.Draw(image.image)
    draw.text(watermark.coords, watermark.text, fill=watermark.font_color)
    image.image.show()
    # Allows use of save button
    save_button.config(state="normal")


def reset_watermark():
    # Resets the watermark by re-opening the original image
    reset = messagebox.askquestion(title="Reset Progress?", message="This will reset the watermark. Are you sure?")
    if reset == "yes":
        image.open_image()


def save_image():
    # Prompts the user to select where the image will be saved and saves the watermarked image
    directory = filedialog.askdirectory(initialdir="/", title="Select save location")
    new_filename = f"{directory}/{new_entry.get()}.{image.file_ext}"
    if new_filename == image.filename:
        overwrite = messagebox.askquestion(
            title="Overwrite Existing File?",
            message='Do you wish to overwrite the original image file?\n'
                    'Click "Yes" to proceed or click "No" and change the "Save as Filename" field '
                    'or select a different folder.')
        if overwrite == "yes":
            image.image.save(new_filename)
    else:
        image.image.save(new_filename)


# Create Img and Wmark objects
image = Img()
watermark = Wmark()

# Main window setup
window = tk.Tk()
window.title("Watermark")
window.config(padx=50, pady=50)

# Get screen dimensions
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate x and y coordinates for main window
x = int((screen_width / 2) - (MAIN_WINDOW_WIDTH / 2))
y = int((screen_height / 2) - (MAIN_WINDOW_HEIGHT / 2))

# Set main window dimensions and location (centered on screen)
window.geometry(f"{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}+{x}+{y}")

# Set main window as non-resizable
window.resizable(False, False)

# Button/entry/label setup
browse_button = tk.Button(
    width=30,
    height=3,
    text="Browse for Images",
    font=("TkDefaultFont", 16, "bold"),
    command=browse_images,
)
browse_button.grid(row=0, column=0, columnspan=3, pady=10)
current_label = tk.Label(text="Selected image:", width=15, state="disabled")
current_label.grid(row=1, column=0, pady=10)
current_entry = tk.Entry(width=25, state="disabled")
current_entry.grid(row=1, column=1, columnspan=2)
new_label = tk.Label(text="Save as filename:", width=15, state="disabled")
new_label.grid(row=2, column=0, pady=10)
new_entry = tk.Entry(width=25, state="disabled")
new_entry.grid(row=2, column=1, columnspan=2)
watermark_label = tk.Label(text="Watermark text:", width=15, state="disabled")
watermark_label.grid(row=3, column=0, pady=10)
watermark_entry = tk.Entry(width=25, state="disabled")
watermark_entry.grid(row=3, column=1, columnspan=2)
color_button = tk.Button(width=15, text="Font Color", state="disabled", command=choose_font_color)
color_button.grid(row=4, column=0)
preview_button = tk.Button(width=15, text="Preview Image", state="disabled", command=preview_image)
preview_button.grid(row=4, column=1)
reset_button = tk.Button(width=15, text="Reset Watermark", state="disabled", command=reset_watermark)
reset_button.grid(row=4, column=2)
save_button = tk.Button(
    width=20,
    height=2,
    text="Save Image",
    font=("TkDefaultFont", 14, "bold"),
    state="disabled",
    command=save_image,
)
save_button.grid(row=5, column=0, columnspan=3, pady=10)

window.mainloop()
