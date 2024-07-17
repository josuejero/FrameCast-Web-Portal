import time
import threading
from controller.frame_controller import start_frame_controller
from web.web_server import start_web_server
import pyautogui

def main():
	
	web_server_thread = threading.Thread(target=start_web_server)
	web_server_thread.daemon = True
	web_server_thread.start()
	
	start_frame_controller()
	
	'''try:
		while True:
			time.sleep(1)
			pyautogui.click(1000,500)
	except KeyboardInterrupt:
		print("Application closing...")'''
		
if __name__ == '__main__':
	main()


	
