import socket


# Multiplayer and server creation utilities

def create_server(host, port):
	"""
	Creates and binds a TCP socket server.

	Args:
		host (str): Local IP address to bind.
		port (int): Port number to listen on.

	Returns:
		socket.socket: The bound server socket.
	"""
	try:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind((host, int(port)))
		return server
	except Exception as e:
		print(f"Error creating server: {e}")
		raise


def create_client(host, port):
	"""
	Creates a TCP socket client and connects to a server.

	Args:
		host (str): IP address of the server.
		port (int): Port number to connect to.

	Returns:
		socket.socket: The connected client socket.
	"""
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((host, int(port)))
		return client
	except Exception as e:
		print(f"Error connecting to server: {e}")
		raise
