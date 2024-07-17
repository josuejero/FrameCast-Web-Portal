import time
import threading
from principal.agent_manager import run_agent_manager
from controller.frame_controller import start_frame_controller
from web.web_server import start_web_server

def main():

	agent_manager_thread = threading.Thread(target=run_agent_manager)
	agent_manager_thread.daemon = True
	agent_manager_thread.start()
	
	web_server_thread = threading.Thread(target=start_web_server)
	web_server_thread.daemon = True
	web_server_thread.start()
	
	start_frame_controller()
	
	
	'''try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		print("Main application is shutting down...")'''


if __name__ == '__main__':
	main()
