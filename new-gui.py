import rospy
from std_msgs.msg import String
import tkinter as tk
from PIL import Image, ImageTk

class ImageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image GUI")

        self.transparency = 20
        self.icon_size = 200
        self.space_between_images = 20  # Adjust as needed
        
        # Initialize images
        self.image_list = [
            [Image.open("Social-awareness/images/shape-0.png"), 
             Image.open("Social-awareness/images/shape-1.png"),
             Image.open("Social-awareness/images/shape-2.png")],

             [Image.open("Social-awareness/images/status-single.png"), 
             Image.open("Social-awareness/images/status-married.png"),
             Image.open("Social-awareness/images/status-group3.png")],

             [Image.open("Social-awareness/images/speed-slow.png"),
             Image.open("Social-awareness/images/speed-fast.png")],

             [Image.open("Social-awareness/images/hat.png"), 
             Image.open("Social-awareness/images/hat-no.png")],
        ]

        

        # Create labels for images
        self.labels = []
        for i in range(len(self.image_list)):
            row_labels = []
            for j in range(len(self.image_list[i])):
                label = tk.Label(root)
                label.grid(row=(i*2), column=j, padx=0, pady=self.space_between_images)  # Add spacing here
                # label.grid(row=i, column=j)
                row_labels.append(label)
            self.labels.append(row_labels)
        
        # self.show_images()
        self.create_buttons()
        self.show_images()

        self.subscriber = rospy.Subscriber("string_topic", String, self.string_callback)


    def create_buttons(self):
        for i in range(len(self.image_list)):
            for j in range(len(self.image_list[i])):
                button = tk.Button(self.root, command=lambda cat=i, itm=j: self.on_button_click(cat, itm))
                # button.grid(row=i, column=j)
                # button.grid(row=len(self.image_list), column=j, padx=10, pady=10)  # Adjust padx and pady as needed
                button.grid(row=(i*2)+1, column=j, padx=0, pady=1)

                # img = self.image_list[i][j].resize((self.icon_size, self.icon_size), Image.LANCZOS)
                # img.putalpha(self.transparency)
                # photo = ImageTk.PhotoImage(img)
                # button.config(image=photo)
                # button.image = photo

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
        # for i in range(len(self.image_list)):
        for j in range(len(self.image_list[category])):
            img = self.image_list[category][j].copy()

            img = img.resize((self.icon_size, self.icon_size), Image.LANCZOS)

            if j != item:
                # img = Image.new("RGBA", img.size, (255, 255, 255, 0))  # Create a white background
                # img.paste(img, (0, 0), img)  # Paste the original image with transparency onto the white background
                # img.putalpha(int(255 * self.transparency))  # Set the overall transparency level
                img.putalpha(self.transparency)
                # img.putdata([(r, g, b, int(255 * self.transparency)) for r, g, b, _ in img.getdata()])

            photo = ImageTk.PhotoImage(img)

            self.labels[category][j].configure(image=photo)
            self.labels[category][j].image = photo

    def updateTransparency(self, image_index, transparency):
        if 0 <= image_index < len(self.image_list):
            self.image_list[image_index] = self.apply_transparency(self.image_list[image_index], transparency)
            self.update_images()

    def apply_transparency(self, image, transparency):
        if self.ros_message != "A":
            new_image = image.copy()
            new_image.putdata([(r, g, b, int(255 * transparency)) for r, g, b, _ in new_image.getdata()])
            return new_image
        else:
            return image

if __name__ == "__main__":
    root = tk.Tk()
    




def main():
    rospy.init_node("image_selector_node")
    app = ImageGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
