from tkinter import *
from PIL import Image, ImageTk
import socket
import threading
import pyautogui
import base64
import mss

window = Tk()
window.geometry("1280x720")

canvas = Canvas(window, width=1920, height=1080)
canvas.grid(row=0, column=0)

# host = "localhost"
# port = 8080

# server = socket.socket()
# server.bind((host, port))
# server.listen()

# client, address = server.accept()


def mouse_event(event):
	mouse_x, mouse_y = event.x, event.y
	action = event.num

	if action == 1:
		pyautogui.moveTo(x=mouse_x, y=mouse_y)
		pyautogui.click(button="left")
	elif action == 3:
		pyautogui.moveTo(x=mouse_x, y=mouse_y)
		pyautogui.click(button="right")


def update():		
	while True:
		sct = mss.mss()
		img = ImageTk.PhotoImage(file=sct.shot())
		canvas.create_image(0, 0, image=img, anchor="nw")

threading.Thread(target=update).start()

window.bind_all("<Button-1>", mouse_event)
window.bind_all("<Button-3>", mouse_event)

window.mainloop()