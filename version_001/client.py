import socket
import threading

import mss
import pyautogui


class Client:

	def __init__(self, host, port):
		self.sock = socket.socket()
		self.sock.connect((host, port))

	def screen_share(self):
		sct = mss.mss()

		while True:
			sct.shot(output="test.png")
			with open("test.png", "rb") as file:
				img = file.read()
				self.sock.send(img)

	def command_line(self):
		while True:
			cmd = self.sock.recv(1024).decode()

			if cmd == "screen":
				threading.Thread(target=self.screen_share()).start()
			elif cmd == "recv_message":
				message_data = self.sock.recv(2048)
				pyautogui.alert(message_data, "~")


if __name__ == '__main__':
	client = Client("localhost", 8888)
	client.command_line()