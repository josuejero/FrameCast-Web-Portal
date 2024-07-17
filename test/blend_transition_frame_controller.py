import time
import os
import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread
import queue

#current_photo = None
#next_photo = None
#update = False
#alpha = 0.0

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
next_file_path = os.path.join(current_dir,'displayed_photo','next.jpg')
current_file_path = os.path.join(current_dir,'displayed_photo','current.jpg')
init_file_path = os.path.join(current_dir,'logo.jpg')
   
def frame_control(q):
    
    #global current_photo
    #global next_photo
    #global update
        
    time.sleep(5)
           
    while True:
 
        if os.path.exists(next_file_path):
            #next_photo = Image.open(next_file_path)
            #if current_photo is None:
                #current_photo = next_photo
            #update = True
            
            try:
                if os.path.exists(current_file_path):
                    os.remove(current_file_path)
                os.rename(next_file_path,current_file_path)
                q.put(current_file_path)
            except Exception as e:
                print(f"An error occurred: {e}")

        time.sleep(1)
    
'''def update_display(image_label):
    
    global current_photo
    global next_photo
    global update
    global alpha
    
    if update and next_photo is not None and current_photo is not None:
        photo = Image.blend(current_photo, next_photo, alpha)
        alpha += 0.05
        if alpha >= 1.0:
            alpha = 0.0
            current_photo = next_photo
            display = ImageTk.PhotoImage(current_photo)
            image_label.config(image=display)
            image_label.image = display
            update = False
        else:
            image_label.after(50, update_display, image_label)
            display = ImageTk.PhotoImage(photo)
            image_label.config(image=display)
            image_label.image = display
            return
    
    image_label.after(1000, update_display, image_label)'''
    
def update_display(image_label, q):
    
    try:
        image_path = q.get_nowait()
        if os.path.exists(image_path):
            image = Image.open(image_path)
            display = ImageTk.PhotoImage(image)
            image_label.config(image=display)
            image_label.image = display
    except queue.Empty:
        pass
    
    image_label.after(1000, update_display, image_label, q)
  
def start_frame_controller():
           
    root = tk.Tk()
    root.geometry("1024x600")
    
    image_label = tk.Label(root)
    image_label.pack(fill=tk.BOTH, expand=True)
    
    q = queue.Queue(maxsize=1)
    q.put(init_file_path)
        
    update_thread = Thread(target=frame_control,args=(q,),daemon=True)
    update_thread.start()
        
    update_display(image_label, q)
    
    root.mainloop()

    

    
    
