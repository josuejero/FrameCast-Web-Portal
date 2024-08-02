import bluetooth

server_address = "B8:27:EB:81:31:84"

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((server_address,1))

message = "Hello, Raspberry Pi Zero W!"
sock.send(message)

print(f"Sent: {message}")

sock.close()
