import torch
import sys
import os
import time
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import cv2
import Tkinter as tk
from skimage import io
from PIL import ImageTk, Image

# Class Definitions
class Net(nn.Module):
	""" Generic Convolutional Neural Network """
	def __init__(self):
		super(Net, self).__init__()
		self.conv1 = nn.Conv2d(3, 6, 5)
		self.pool = nn.MaxPool2d(2, 2)
		self.conv2 = nn.Conv2d(6, 16, 5)
		self.fc1 = nn.Linear(16 * 5 * 5, 120)
		self.fc2 = nn.Linear(120, 84)
		self.fc3 = nn.Linear(84, int(sys.argv[1]))

	def forward(self, x):
		#print("Start: " + str(x.size()))
		x = F.relu(self.conv1(x))
		#print("after conv1: " + str(x.size()))
		x = self.pool(x)
		#print("after pool1: " + str(x.size()))
		x = F.relu(self.conv2(x))
		#print("after conv2: " + str(x.size()))
		x = self.pool(x)
		#print("after pool2: " + str(x.size()))
		x = x.view(-1, 16 * 5 * 5)
		x = F.relu(self.fc1(x))
		x = F.relu(self.fc2(x))
		x = self.fc3(x)
		return x

# Play a round
def play():
	s, image = cam.read()
	if(s):
		image = cv2.resize(image, (32, 32))
		transform = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
		image = transform(image).detach().numpy()
		X = np.zeros([1, 3, 32, 32])
		X[0] = image
		X = X.astype(np.float32)
		X = torch.from_numpy(X)
		y_guess = net(X).detach().numpy()[0]
		y_guess = np.exp(y_guess) / np.sum(np.exp(y_guess), axis=0)
		guess = "Guess: " + classes[np.argmax(y_guess)] + "\n\n"
		for i in range(len(classes)):
			guess += classes[i] + ": " + str(round(y_guess[i], 3)*100) + "%\n"
		panel.configure(text=guess)
		panel.text = guess
	window.after(10, play)

# Make sure number of classes is passed in
if(len(sys.argv) != 2):
	sys.exit()

# Set up neural net 
net = torch.load("model.pt")
classes = []
f = open("../key.txt", "r")
for line in f:
	classes.append(line.split()[0])
cam = cv2.VideoCapture(0)

# Set up GUI
window = tk.Tk()
window.title("CNN")
window.geometry("400x400")
panel = tk.Label(window, text="CNN")
panel.pack(side = "bottom", fill = "both", expand = "yes")
window.after(2000, play)
window.mainloop()
