"""
DisplayPage
"""

from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np

# TODO: DisplayPage Class file
# The video part of the GUI
# Used for reading in and displaying the animation sent directly from simulink
HEIGHT, WIDTH = 600, 600
class DisplayPage(ttk.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(**kwargs)
		self.currentVideoFrame = None
		self.image = None
		self.imageLabel = None	

	# Loads the initial state of the display page, using a given placeholder image
	def load(self, filename, main, frameSize):
		placeholder = Image.open(filename)
		self.image = ImageTk.PhotoImage(placeholder)
		if self.imageLabel == None:
			self.imageLabel = ttk.Label(self, image=self.image)
			self.imageLabel.grid(column=1,row=0)
			print ('reloading fully')
		else:
			self.imageLabel.configure(image = self.image)
		self.after(30, self.loadImage, main, frameSize)
	
	# Loads an image from the video queue
	# This function will schedule itself to run, so it should ONLY BE CALLED ONCE
	# Once it is called, it will continue to call itself and attempt to load images from the video queue
	# Hence why it begins by checking whether or not the video queue has enough data to load an image
	def loadImage(self, main, frameSize):
		if main.currentVideoFrameSize >= frameSize:
			img = bytearray()
			pulledSize = 0
			imageLoaded = False
			while not main.videoEmpty and not imageLoaded:
				vidData = main.getVideoData()
				if pulledSize + len(vidData) >= frameSize:
					#split vidData to size
					tempArr = bytearray(vidData)
					sizeToPull = frameSize - pulledSize
					img.extend(tempArr[:sizeToPull])
					del tempArr[:sizeToPull]
					#put excess back into queue
					main.addVideoData(tempArr)
					#actually load image
					#the following numpy code exists because simulink sends video data as RGB, interleaved by row of pixels
					#why simulink does this I don't know, wish it didn't, but it is what it is
					h,w = 600,600
					bpc = h*w
					# Make a Numpy array for each channel's pixels
					R = np.frombuffer(img, dtype=np.uint8, count=bpc).reshape((h,w))  
					G = np.frombuffer(img, dtype=np.uint8, count=bpc, offset=bpc).reshape((h,w))  
					B = np.frombuffer(img, dtype=np.uint8, count=bpc, offset=2*bpc).reshape((h,w))

					# Interleave the pixels from RRRRRRGGGGGGBBBBBB to RGBRGBRGBRGBRGB
					RGB = np.dstack((R,G,B))

					# Make PIL Image from Numpy array
					self.currentVideoFrame = Image.fromarray(RGB)
					self.image = ImageTk.PhotoImage(self.currentVideoFrame)
					# Load the PIL image into the image display label
					if self.imageLabel == None:
						self.imageLabel = ttk.Label(self, image=self.image)
						self.imageLabel.grid(column=1,row=0)
						print ('reloading fully')
					else:
						self.imageLabel.configure(image = self.image)
					imageLoaded = True
					main.calculateVideoFrameSize()
				else:
					img.extend(bytearray(vidData))
					pulledSize += len(vidData)
		# Schedules itself to run again, with the same input data
		# The first argument is the amount of milliseconds to wait before calling itself again
		# TODO:
		# - Tweak the first argument to strike a balance between not calling itself too often and maximizing framerate
		# - If needed, create a test or something in order to be able to stop this function from running instead of closing python
		self.after(10, self.loadImage, main, frameSize)

#		img = bytearray()
#		while not main.videoEmpty and main.currentVideoFrameSize < frameSize:
#			img.append(bytearray(main.getVideoData()))
#		if not img == None and main.currentVideoFrameSize >= frameSize:
#			print("Final frame is of size ", len(img))
#			self.currentVideoFrame = Image.frombytes("RGB",[600,600],bytes(img))
#			self.image = ImageTk.PhotoImage(self.currentVideoFrame)

	# Loading the image the manual/hard way, only intended for debugging
	def loadImageManually(self, data):
		self.currentVideoFrame = Image.frombytes("RGB",[600,600],data)
		self.image = ImageTk.PhotoImage(self.currentVideoFrame)
		if self.imageLabel == None:
			self.imageLabel = ttk.Label(self, image=self.image)
			self.imageLabel.grid(column=0,row=0)
			print ('reloading fully')
		else:
			self.imageLabel.configure(image = self.image)
