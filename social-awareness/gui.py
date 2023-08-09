#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import tkinter as tk
from PIL import Image, ImageTk

class ImageSelectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Awareness")

        self.current_transparency = [255, 255, 255]  # Initial transparency (white)

        self.grid_size = (5, 3)  # Number of rows and columns in the grid
        self.cell_width = 300
        self.cell_height = 300

        # Load your images here
        self.image_head_shape_0 = Image.open("social-awareness/images/shape-0.png").convert("RGBA")
        self.image_head_shape_1 = Image.open("social-awareness/images/shape-1.png").convert("RGBA")
        self.image_head_shape_2 = Image.open("social-awareness/images/shape-2.png").convert("RGBA")

        self.images = [
            self.image_head_shape_0,
            self.image_head_shape_1,
            self.image_head_shape_2,
        ]

        self.images = [self.resize_image(image) for image in self.images]

        self.image_frames = [[None] * self.grid_size[1] for _ in range(self.grid_size[0])]

        self.create_grid()

        self.image_labels = [[None] * self.grid_size[1] for _ in range(self.grid_size[0])]
        self.load_images()

        self.subscriber = rospy.Subscriber("string_topic", String, self.string_callback)

    def string_callback(self, msg):
        if msg.data == "A":
            self.update_transparency(transparency=[255, 255, 255])  # No transparency
        elif msg.data == "B":
            self.update_transparency(transparency=[255, 128, 128])  # Partial transparency
        else:
            self.update_transparency(transparency=[128, 255, 128])  # Different partial transparency

    def update_transparency(self, transparency):
        self.current_transparency = transparency
        for row in self.image_frames:
            for image_frame in row:
                label = image_frame.winfo_children()[0]
                image = label.image
                r, g, b, _ = image.split()
                new_alpha_channel = Image.new("L", image.size, self.current_transparency[0])
                new_image = Image.merge("RGBA", (r, g, b, new_alpha_channel))
                photo = ImageTk.PhotoImage(new_image)
                label.config(image=photo)
                label.photo = photo

    def resize_image(self, image):
        return image.resize((self.cell_width, self.cell_height), Image.LANCZOS)

    def create_grid(self):
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                image_frame = tk.Frame(self.root, width=self.cell_width, height=self.cell_height)
                image_frame.grid(row=row, column=col)

                label = tk.Label(image_frame)
                label.pack()

                self.image_frames[row][col] = image_frame

    def close_gui(self):
        self.root.destroy()

    def load_images(self):
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                image_frame = tk.Frame(self.root, width=self.cell_width, height=self.cell_height)
                image_frame.grid(row=row, column=col)

                label = tk.Label(image_frame)
                label.pack()

                self.image_labels[row][col] = label

        self.update_images()

    def update_images(self):
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                img = self.images[row % len(self.images)].copy()
                if self.ros_message != "A":
                    img.putdata([(r, g, b, int(255 * self.transparency)) for r, g, b, _ in img.getdata()])
                photo = ImageTk.PhotoImage(img)
                self.image_labels[row][col].config(image=photo)
                self.image_labels[row][col].photo = photo

def main():
    rospy.init_node("image_selector_node")

    root = tk.Tk()
    gui = ImageSelectorGUI(root)

    root.mainloop()

if __name__ == "__main__":
    main()
