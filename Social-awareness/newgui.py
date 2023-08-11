#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import tkinter as tk
from PIL import Image, ImageTk

from sensor_msgs.msg import Image as ROSImage
from cv_bridge import CvBridge
import cv2

class ImageGUI:
    def __init__(self, root):
        print("im running the image GUI")
        self.root = root
        self.root.title("Image GUI")

        self.transparency = 20
        self.icon_size = 300
        self.space_between_images = 20  # Adjust as needed
        
        # Initialize images
        self.image_list = [
            [Image.open("images/shape-0.png"), 
             Image.open("images/shape-1.png"),
             Image.open("images/shape-2.png")],

             [Image.open("images/status-single.png"), 
             Image.open("images/status-married.png"),
             Image.open("images/status-group3.png")],

             [Image.open("images/speed-slow.png"),
             Image.open("images/speed-fast.png")],

             [Image.open("images/hat.png"), 
             Image.open("images/hat-no.png")],
        ]

        self.labels = []
        for i in range(len(self.image_list)):
            row_labels = []
            for j in range(len(self.image_list[i])):
                label = tk.Label(root)
                label.grid(row=(i*2), column=j, padx=0, pady=self.space_between_images)
                row_labels.append(label)
            self.labels.append(row_labels)

        self.create_buttons()
        self.show_images()

        self.subscriber = rospy.Subscriber("string_topic", String, self.string_callback)

    def create_buttons(self):
        for i in range(len(self.image_list)):
            for j in range(len(self.image_list[i])):
                button = tk.Button(self.root, command=lambda cat=i, itm=j: self.on_button_click(cat, itm))
                button.grid(row=(i*2)+1, column=j, padx=0, pady=1)

    def on_button_click(self, category, item):
        self.update_images(category, item)
    
    def string_callback(self, msg):
        if msg.data == "A":
            self.update_images(0,0)
        elif msg.data == "B":
            self.update_images(1,1)
        elif msg.data == "C":
            self.update_images(2,1)
        else:
            self.update_images(0,0)

    def show_images(self):
        for i in range(len(self.image_list)):
            self.update_images(i, -1)

    def update_images(self, category, item):
        for j in range(len(self.image_list[category])):
            img = self.image_list[category][j].copy()
            img = img.resize((self.icon_size, self.icon_size), Image.LANCZOS)

            if j != item:
                img.putalpha(self.transparency)

            photo = ImageTk.PhotoImage(img)

            self.labels[category][j].configure(image=photo)
            self.labels[category][j].image = photo

class ImageReceiverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Receiver")

        self.bridge = CvBridge()

        self.image_label = tk.Label(root)
        self.image_label.grid(row=0, column=4, rowspan=1, padx=10, pady=10)  # Adjust row, column, rowspan, padx, and pady

        self.subscriber = rospy.Subscriber("image_topic", ROSImage, self.image_callback)
    
    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            resized_image = self.resize_cv_image(cv_image, 300, 300)  # Adjust new_width and new_height
            self.update_image(resized_image)
        except Exception as e:
            print("Error processing image:", e)

    def resize_cv_image(self, cv_image, width, height):
        return cv2.resize(cv_image, (width, height))

    def update_image(self, cv_image):
        image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image)
        tk_image = ImageTk.PhotoImage(pil_image)
        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image

def main():
    rospy.init_node("combined_gui_receiver_node")

    root = tk.Tk()

    gui = ImageGUI(root)
    receiver = ImageReceiverGUI(root)

    root.mainloop()

if __name__ == "__main__":
    main()
