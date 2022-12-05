import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw

WATERMARK = "test"
image = None


def browse_files():
    global image
    filename = filedialog.askopenfilename(
        initialdir="/",
        title="Select a file",
        filetypes=(("JPEG", ".jpg"), ("all files", "*.*"))
    )
    image = Img(filename)


class Img:

    def __init__(self, filename):
        self.filename = filename
        self.filename_display = filename.split("/")[-1]
        self.new_filename = f"{''.join(self.filename_display.split('.')[0:-1])}_edit.jpg"
        self.update_entry()
        self.image = Image.open(self.filename)
        self.watermark_image()

    def watermark_image(self):
        draw = ImageDraw.Draw(self.image)
        draw.text((0, 0), WATERMARK)

    def preview_image(self):
        self.image.show()

    def update_entry(self):
        browse_entry.config(state="normal")
        browse_entry.insert(0, self.filename_display)
        browse_entry.config(state="disabled")
        new_entry.insert(0, self.new_filename)

    def save_image(self):
        self.image.save(self.new_filename)
        browse_entry.config(state="normal")
        browse_entry.delete(0, tk.END)
        browse_entry.config(state="disabled")
        new_entry.delete(0, tk.END)


def preview_image():
    image.preview_image()


def save_image():
    image.save_image()


window = tk.Tk()
window.title("Watermark")
window.config(padx=50, pady=50)

browse_label = tk.Label(text="Select an image")
browse_label.grid(row=0, column=0, padx=2)
browse_entry = tk.Entry(width=20, state="disabled")
browse_entry.grid(row=0, column=1)
browse_button = tk.Button(width=20, text="Browse", command=browse_files)
browse_button.grid(row=0, column=2)
new_label = tk.Label(text="New filename")
new_label.grid(row=1, column=0)
new_entry = tk.Entry(width=20)
new_entry.grid(row=1, column=1)
preview_button = tk.Button(width=20, text="Preview", command=preview_image)
preview_button.grid(row=1, column=2)
save_button = tk.Button(width=20, text="Save", command=save_image)
save_button.grid(row=2, column=1)

window.mainloop()
