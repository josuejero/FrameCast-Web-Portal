from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/heartbeat',methods=['GET'])
def heartbeat():
	return jsonify(status="success",message="Connection successful"), 200
	
def start_web_server():
	print("Starting web server...")
	app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
	start_web_server()
