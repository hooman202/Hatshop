import time
import tkinter as tk
from PIL import Image, ImageTk

def on_button_click(index):
    print(f"Button {index} clicked")

root = tk.Tk()

image_path = "social-awareness/images/shape-1.png"  # Replace with your image path
transparent_image = Image.open(image_path).convert("RGBA")

buttons = []

for i in range(5):
    button_label = tk.Label(root, image=ImageTk.PhotoImage(transparent_image))
    button_label.bind("<Button-1>", lambda event, idx=i: on_button_click(idx))
    button_label.grid(row=i, column=0)
    buttons.append(button_label)
    while(True):
        print("Text Merry")
        time.sleep(1)

root.mainloop()