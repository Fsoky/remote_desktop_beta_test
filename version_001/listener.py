import io

from tkinter import Tk, Canvas, Menu

import socket
import threading

from PIL import ImageTk, Image
import pyautogui


class Listener:

	def __init__(self, host, port):
		self.sock = socket.socket()
		self.sock.bind((host, port))
		self.sock.listen()

		self.client, self.addr = self.sock.accept()
		print(f"client connected: {self.addr[0]} {self.addr[1]}")

	def recv_data(self):
		data = self.client.recv(300000)
		return data

	def send_data(self, data):
		self.client.send(data.encode())

	def command_line(self):
		while True:
			cmd = input("> ")

			if cmd == "screen":
				self.send_data(cmd)
				threading.Thread(target=Visual.get_client_screen(self)).start()


class Visual(Listener):

	def get_client_screen(self):
		window = Tk()
		window.title("screen")
		window.geometry("1280x720")

		canvas = Canvas(window, width=1920, height=1080)
		canvas.grid(row=0, column=0)

		def mouse_event(event):
			x, y = event.x, event.y
			act = event.num

			if act == 1:
				pyautogui.moveTo(x=x, y=y)
				pyautogui.click(button="left")
			elif act == 3:
				pyautogui.moveTo(x=y, y=x)
				pyautogui.click(button="right")

		window.bind_all("<Button-1>", mouse_event)
		window.bind_all("<Button-3>", mouse_event)

		def update():
			while True:
				img_data = self.recv_data()
				
				try:
					img = ImageTk.PhotoImage(Image.open(io.BytesIO(img_data)).resize((1280, 720)))
					canvas.create_image(0, 0, image=img, anchor="nw")
				except OSError:
					continue
				except AttributeError:
					continue

		threading.Thread(target=update).start()
		window.mainloop()


if __name__ == '__main__':
	listener = Listener("localhost", 8888)
	listener.command_line()