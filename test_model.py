import torch
import sys
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from skimage import io

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

class GDataset(torch.utils.data.Dataset):
	""" Generic Dataset Class """
	def __init__(self, train=True):
		self.metadata = []
		self.train = train
		if(train):
			metadata_file = "./data/train/metadata.txt"
		else:
			metadata_file = "./data/test/metadata.txt"
		f = open(metadata_file, "r")
		for line in f:
			elem = line.split()
			elem[1] = int(elem[1])
			self.metadata.append(elem)
	
	def __len__(self):
		return len(self.metadata)

	def __getitem__(self, idx):
		if(self.train):
			image_name = "./data/train/" + self.metadata[idx][0]
		else:
			image_name = "./data/test/" + self.metadata[idx][0]
		image = io.imread(image_name)
		label = self.metadata[idx][1]

		transform = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
		image = transform(image)

		data_tuple = (image, label)
		return data_tuple

# Make sure number of classes is passed in
if(len(sys.argv) != 2):
	sys.exit()

# Load the neural net
net = torch.load("model.pt")

# Test the neural net
num_correct = 0
testset = GDataset(train=False)
testloader = torch.utils.data.DataLoader(testset, batch_size=1, shuffle=True, num_workers=2)
for data in testloader:
	X, y_real = data
	y_real = y_real.detach().numpy()[0]
	y_guess = np.argmax(net(X).detach().numpy())
	if(y_real == y_guess):
		num_correct += 1
print("Test data percentage correct: " + str(num_correct/len(testloader)*100) + "%")
