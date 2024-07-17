#import tkinter as tk
import os
import sys
from PIL import Image, ImageTk, ExifTags

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
import_dir = os.path.join(parent_dir,'principal')
sys.path.append(import_dir)

from framecast_classes import DigitalPhoto, PhotoViewWindow

import os
import io
     
def format_for_display(digital_photo, src_file_path, dest_file_path):

    photo = Image.open(src_file_path)
    photo = suppress_auto_rotate(photo)
    
    scaling = digital_photo.scaling
    if scaling != 100:
        w, h = photo.size
        w, h = (int)(w*scaling/100), (int)(h*scaling/100)
        photo = photo.resize((w,h),resample=Image.NEAREST)
    
    left = digital_photo.window.x
    top = digital_photo.window.y
    right = left+1024
    bottom = top+600
    
    photo = photo.crop((left,top,right,bottom))
    photo.save(dest_file_path)
    
def suppress_auto_rotate(photo):
    
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
    
    return photo
        
def format_photo_for_edit_window(filepath, scaleValue):
    
    actualScaleValue = (int)(scaleValue)/100 * 0.5
    
    photo = Image.open(filepath)
    photo = suppress_auto_rotate(photo)
    photo = photo.resize(((int)(photo.width * actualScaleValue),(int)(photo.height * actualScaleValue)), Image.ANTIALIAS)

    photo_io = io.BytesIO()
    photo.save(photo_io, 'JPEG')
    photo_io.seek(0)
    
    return photo_io

def format_photo_for_preview(filepath):
    
    photo = Image.open(filepath)
    photo = suppress_auto_rotate(photo)
    
    w = photo.width
    h = photo.height
    
    scaleValue = 1;
    
    if w >= h:
        scaleValue = w/300
    else:
        scaleValue = h/300
    
    print(photo.width)
    print(photo.height)
      
    photo = photo.resize(((int)(photo.width / scaleValue),(int)(photo.height / scaleValue)), Image.ANTIALIAS)
    print(photo.width)
    print(photo.height)
    photo_io = io.BytesIO()
    photo.save(photo_io, 'JPEG')
    photo_io.seek(0)
    
    return photo_io
        
        
        

