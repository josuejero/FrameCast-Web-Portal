import time
import os
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from threading import Thread
import queue
import RPi.GPIO as GPIO
import subprocess
import socket
import pyautogui
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
wireless_dir = os.path.join(parent_dir,'wireless')
bluetooth_script = os.path.join(wireless_dir,'bluetooth_connection.py')
wireless_script = os.path.join(wireless_dir,'wifi_connection.py')
next_file_path = os.path.join(current_dir,'displayed_photo','next.jpg')
current_file_path = os.path.join(current_dir,'displayed_photo','current.jpg')
init_file_path = os.path.join(current_dir,'logo.jpg')
hostname_file_path = os.path.join(current_dir,'hostname_display.jpg')


line = "WIFI: Dan’s 13 ProMax 12345679"
match = re.match(r"WIFI: (.+) (\S+)$", line)
if match:
	ssid = match.group(1)
	psk = match.group(2)
	print(f"SSID: {ssid}")
	print(f"PSK: {psk}")
	
result = subprocess.run(['sudo','python3',wireless_script,ssid,psk],capture_output=True,text=True)
if result.returncode != 0:
	print(f"Error running wireless script:\n{result.stderr}")
else:
	print(f"Wireless script successful:\n{result.stdout}")
