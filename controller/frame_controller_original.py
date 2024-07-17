import time
import os
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from threading import Thread
import queue
import RPi.GPIO as GPIO
import subprocess
import socket

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
wireless_dir = os.path.join(parent_dir,'wireless')
bluetooth_script = os.path.join(wireless_dir,'bluetoothsocket.py')
next_file_path = os.path.join(current_dir,'displayed_photo','next.jpg')
current_file_path = os.path.join(current_dir,'displayed_photo','current.jpg')
init_file_path = os.path.join(current_dir,'logo.jpg')
hostname_file_path = os.path.join(current_dir,'hostname_display.jpg')

BUTTON_PIN = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def get_hostname():
    
    try:
        return socket.gethostname()
    except Exception as e:
        print(f"Error getting hostname: {e}")
        return None    

def create_hostname_display():
    
    hostname = get_hostname()
    if hostname:
        message = hostname
    else:
        message = "Not Available"
    font_path = "/user/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font_size = 40
    hostname_image = Image.new('RGB', (1024,600), color='black')
    width, height = hostname_image.size
    hostname_draw = ImageDraw.Draw(hostname_image)
    font = ImageFont.truetype(font_path,font_size)
    text_bbox = hostname_draw.textbbox((0,0),message,font=font)
    #text_width = text_bbox[2] - text_bbox[0]
    #text_height = text_bbox[3] - text_bbox[1]
    #text_x = (width - text_width) // 2
    #text_y = (height - text_height) // 2
    hostname_draw.text((10,10), message, font = font, fill='white')
    hostname_image.save(hostname_file_path)

def run_command(command):
    result = subprocess.run(command,shell=True,capture_output=True,text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}\n{result.stderr}")
    else:
        print(f"Command successful: {command}\n{result.stdout}")


def enter_bluetooth_discovery_mode():
    
    run_command("sudo hciconfig hci0 piscan")
    run_command(f"sudo python3 {bluetooth_script}")
    run_command("sudo hciconfig hci0 noscan")

   
def frame_control(q):
    
    previous_state = GPIO.HIGH
    time.sleep(5)
           
    while True:
        current_state = GPIO.input(BUTTON_PIN)
        if previous_state == GPIO.HIGH and current_state == GPIO.LOW:
            q.put(hostname_file_path)
            enter_bluetooth_discovery_mode()
            q.put(init_file_path)		
        if os.path.exists(next_file_path):            
            try:
                if os.path.exists(current_file_path):
                    os.remove(current_file_path)
                os.rename(next_file_path,current_file_path)
                q.put(current_file_path)
            except Exception as e:
                print(f"An error occurred: {e}")

        previous_state = current_state
        time.sleep(1)
    
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
    
    create_hostname_display()
    
    #init_display_environment(root)
    
    image_label = tk.Label(root)
    image_label.pack(fill=tk.BOTH, expand=True)
    
    q = queue.Queue(maxsize=1)
    q.put(init_file_path)
        
    update_thread = Thread(target=frame_control,args=(q,),daemon=True)
    update_thread.start()
        
    update_display(image_label, q)
    
    root.mainloop()

def init_display_environment(root=None):
    root.attributes("-fullscreen",True)
    root.config(cursor="none")
    root.bind("<Escape>",lambda event: revert_display_environment(event,root))

def revert_display_environment(event=None,root=None):
    root.attributes("-fullscreen",False)
    root.config(cursor="")

if __name__ == "__main__":
    start_frame_controller()
    

    
    
