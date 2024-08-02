import tkinter as tk
from PIL import Image, ImageTk
import os

class ImageSliderApp:
    def __init__(self, root, image1, image2, image3, hold=5000):
        self.root = root
        self.image1 = image1
        self.image2 = image2
        self.image3 = image3
        self.hold = hold
        self.interval = 10
        self.alpha = 0.0
        self.current_image = image1
        self.next_image = image2
        self.is_image1 = True
        self.counter = 1
        
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', self.exit_fullscreen)
        
        self.image_label = tk.Label(root)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        self.show_current_image()
        
        self.root.after(self.hold, self.transition)
        
    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)
        
    def show_current_image(self):
        self.photo = ImageTk.PhotoImage(self.current_image)
        self.image_label.config(image=self.photo)
        
    def blend_images(self):
        blended_image = Image.blend(self.current_image, self.next_image, self.alpha)
        self.photo = ImageTk.PhotoImage(blended_image)
        self.image_label.config(image=self.photo)
    
    def transition(self):
 
        self.alpha += 0.05
        if self.alpha >= 1.0:
            self.alpha = 0.0
            if self.counter == 1:
                self.current_image = self.image2
                self.next_image = self.image3
                self.counter = 2;
            elif self.counter == 2:
                self.current_image = self.image3
                self.next_image = self.image1
                self.counter = 3;
            else:
                self.current_image = self.image1
                self.next_image = self.image2
                self.counter = 1;
            
            
            '''temp = self.current_image
            self.current_image = self.next_image
            self.next_image = temp'''
            
            self.show_current_image()
            self.root.after(5000, self.transition)
        else:
            self.blend_images()
            self.root.after(self.interval, self.transition)
        
if __name__ == "__main__":
    
    root = tk.Tk()
    
    pic = Image.open("picture.jpg")
    w, h = pic.size
    neww = (int)(w/2)
    newh = (int)(h/2)
    resize_pic = pic.resize((neww,newh),resample=Image.NEAREST)
    w, h = resize_pic.size
    centerX = w/2
    centerY = h/2-50
    left = centerX - 512
    right = centerX + 512
    top = centerY - 300
    bottom = centerY + 300
    crop_pic = resize_pic.crop((left,top,right,bottom))

    pic2 = Image.open("picture2.jpg")
    pic2 = pic2.transpose(Image.ROTATE_270)
    w2, h2 = pic2.size
    ratio2 = w2/1024
    neww2 = (int)(1024)
    newh2 = (int)(h2/ratio2)
    resize_pic2 = pic2.resize((neww2,newh2),resample=Image.NEAREST)
    w2, h2 = resize_pic.size
    centerX2 = w2/2
    centerY2 = h2/2+200
    left2 = centerX2 - 512
    right2 = centerX2 + 512
    top2 = centerY2 - 300
    bottom2 = centerY2 + 300
    crop_pic2 = resize_pic2.crop((left2,top2,right2,bottom2))
    
    pic3 = Image.open("picture3.jpg")
    pic3 = pic3.transpose(Image.ROTATE_270)
    w3, h3 = pic3.size
    ratio3 = w3/1024
    neww3 = (int)(1024)
    newh3 = (int)(h3/ratio3)
    resize_pic3 = pic3.resize((neww3,newh3),resample=Image.NEAREST)
    w3, h3 = resize_pic3.size
    centerX3 = w3/2
    centerY3 = h3/2
    left3 = centerX3 - 512
    right3 = centerX3 + 512
    top3 = centerY3 - 300
    bottom3 = centerY3 + 300
    crop_pic3 = resize_pic3.crop((left3,top3,right3,bottom3))
    
    app = ImageSliderApp(root, crop_pic, crop_pic2, crop_pic3)
    root.mainloop()
        
        
        
        
        
        
