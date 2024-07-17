import tkinter as tk
from PIL import Image, ImageTk, ExifTags
import os
        
if __name__ == "__main__":
           
    photo = Image.open("Photo_8.jpg")
    
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = photo._getexif()
        if exif is not None:
            orientation = exif.get(orientation,1)
            if orientation == 3:
                photo = photo.rotate(180, expand=True)
            elif orientation == 6:
                photo = photo.rotate(270, expand=True)
            elif orientation == 8:
                photo = photo.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    
    scaling = 75
    if scaling != 100:
        w, h = photo.size
        w, h = (int)(w*scaling/100), (int)(h*scaling/100)
        photo = photo.resize((w,h),resample=Image.NEAREST)
    
    left = 55
    top = 350
    right = left+1024
    bottom = top+600
    
    photo = photo.crop((left,top,right,bottom))
    photo.save("photo_test.jpg")
    
def suppress_auto_rotate(photo):
    
    try:
        for orientation in ExifTags.TAGS.keys():
            print(ExifTags.TAGS[orientation])
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = photo._getexif()
        print(exif)
        if exif is not None:
            orientation = exif.get(orientation,1)
            if orientation == 3:
                photo = photo.rotate(180, expand=True)
            elif orientation == 6:
                photo = photo.rotate(270, expand=True)
            elif orientation == 8:
                photo = photo.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    
    return photo
    
        
        
        
        
        
        

