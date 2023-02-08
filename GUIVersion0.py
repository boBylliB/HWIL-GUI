from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from PIL import Image, ImageTk
from queue import Queue
from array import *
import numpy as np
import datetime
import threading
import socket
import csv

# class for the GUI itself
# holds each section of the GUI within itself, and acts to bridge the gap and hold utility functions
class MainPage(ttk.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(**kwargs)
		self.ctrl = None
		self.diag = None
		self.disp = None
		self.requestImageLoad = False
		self.queue = Queue()
		self.sendQueue = Queue()
		self.videoQueue = Queue()
		self.currentVideoFrameSize = 0
		self.empty = True
		self.videoEmpty = True
		self.sendEmpty = True
#	def changeState(self,text):
#		self.state_lbl['text'] = text


	# Adding data to the queue, for any received numeric data
	def addData(self,data):
		self.queue.put(data)
		self.empty = self.queue.empty()

	# Adding data to video queue, solely used for receiving video frames from the simulink animation
	def addVideoData(self,data):
		self.videoQueue.put(data)
		self.videoEmpty = self.videoQueue.empty()
		self.currentVideoFrameSize += len(data)


	# Calculating how large the current video queue would be if read as a single frame
	# Used to compare to the desired video frame size
	def calculateVideoFrameSize(self):
		self.currentVideoFrameSize = 0
		# Loops through each entry in the video queue, and sums up the total video data size
		for idx in range(self.videoQueue.qsize()):
			data = self.getVideoData()
			self.currentVideoFrameSize += len(data)
			self.addData(data)


	# Retrieve video data from queue
	def getVideoData(self):
		# Making sure that the video queue is not empty
		if not self.videoQueue.empty():
			# Pops the current item from the queue
			data = self.videoQueue.get()
			# Removes the size of the data from the frame size
			self.currentVideoFrameSize -= len(data)
			return data

		self.videoEmpty = self.videoQueue.empty()

	# Loading frames within frames, essentially the video screen and the other parts
	# Used for initializing anything required for the subframes to function
	def loadSubFrames(self,ctrl,diag,disp):
		self.disp = disp
		self.disp.grid(row=0, column=1)
		self.ctrl = ctrl
		ctrl.grid(row=0, column=0)
		self.diag = diag
		diag.grid(row=1, column=0, columnspan=2)
		ctrl.load(self)
		disp.load("forklift600.jpg", self, READSIZE)

	# Updates the image within the subframe for video
	# This is what changes the forklift picture to something else
	def updateImage(self, loadedImage):
		if self.imageLabel == None:
			self.imageLabel = ttk.Label(self, image=loadedImage).grid(column=1,row=0)
			print ('reloading fully')
		else:
			self.imageLabel.configure(image = loadedImage)
	
	# Get numeric data from the queue of received data
	def getData(self):
		if not self.queue.empty():
			return self.queue.get()
		self.empty = self.queue.empty()

	# Checks if the received data queue is empty
	def checkEmpty(self):
		return self.queue.empty()

	def updateMatlab(self, *args):
		# Build dataset in the same format as the received dataset
		dataString = str(self.ctrl.EccentricityEntry.get()) + "," + str(self.ctrl.SemiMajorAxisEntry.get()) + "," + str(self.ctrl.InclinationEntry.get()) + "," + str(self.ctrl.LongitudeAscendingEntry.get()) + "," + str(self.ctrl.ArgumentPeriapsisEntry.get()) + "," + str(self.ctrl.TrueAnomalyEntry.get()) + "," + str(self.ctrl.attitudeXEntry.get()) + "," + str(self.ctrl.attitudeYEntry.get()) + "," + str(self.ctrl.attitudeZEntry.get())
		# Convert to bytes and queue it
		data = bytes(dataString,'utf-8')
		self.queueData(data)

	# Adds received data to the queue
	def queueData(self, data):
		self.sendQueue.put(data)
		self.sendEmpty = self.sendQueue.empty()

	# Used for sending data back to simulink, if the send queue isn't empty it'll return the next item of data to send
	def sendData(self):
		if not self.sendQueue.empty():
			return self.sendQueue.get()
		self.sendEmpty = self.sendQueue.empty()

# The control part of the GUI
# Used for entering initial values and controlling the simulation from the GUI
class ControlPage(ttk.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(**kwargs)
		# Orbital Parameters
		self.Eccentricity = StringVar()
		self.SemiMajorAxis = StringVar()
		self.Inclination = StringVar()
		self.LongitudeAscending = StringVar()
		self.ArgumentPeriapsis = StringVar()
		self.TrueAnomaly = StringVar()
		# Orbital Parameter Entries
		self.EccentricityEntry = StringVar()
		self.SemiMajorAxisEntry = StringVar()
		self.InclinationEntry = StringVar()
		self.LongitudeAscendingEntry = StringVar()
		self.ArgumentPeriapsisEntry = StringVar()
		self.TrueAnomalyEntry = StringVar()
		# Attitude
		self.attitudeX = StringVar()
		self.attitudeY = StringVar()
		self.attitudeZ = StringVar()
		# Attitude Entries
		self.attitudeXEntry = StringVar()
		self.attitudeYEntry = StringVar()
		self.attitudeZEntry = StringVar()
		# Simulation Time
		self.time = 0
		self.displayTime = None
		self.units = None
		self.timeLabel = None
		# Flag for when a stringvar is changed by a set function instead of the user
		self.selfChanges = 0
	
	# Control Page save functionality	
	def Control_csv(self):
		# Column headers for csv file
		Control_fields = ['Eccentricity', 'Semi Major Axis', 'Inclination', 'Longitude Ascending', 'Argument Periapsis', 'True Anomaly']
		# Data Definition
		Control_rows = [self.Eccentricity.get(), self.SemiMajorAxis.get(), self.Inclination.get(), self.LongitudeAscending.get(), 
		self.ArgumentPeriapsis.get(), self.TrueAnomaly.get()]
		# name of CSV file
		Control_filename = 'ControlPage.csv'
		# writing csv file
		with open(Control_filename, 'w') as csvfile:
			csvwriter = csv.writer(csvfile)
			# writing the fields (column)
			csvwriter.writerow(Control_fields)
			# writing the data rows
			csvwriter.writerow(Control_rows)
	
	# Attitude save functionality
	def Attitude_csv(self):
		# Column headers for csv file
		Attitude_fields = ['Attitude X', 'Attitude Y', 'Attitude Z']
		# Data Definition
		Attitude_rows = [self.attitudeX.get(), self.attitudeY.get(), self.attitudeZ.get()]
		# name of CSV file
		Attitude_filename = 'ControlPage.csv'
		# writing csv file
		with open(Attitude_filename, 'w') as csvfile:
			csvwriter = csv.writer(csvfile)
			# writing the fields (column)
			csvwriter.writerow(Attitude_fields)
			# writing the data rows
			csvwriter.writerow(Attitude_rows)				
	
	# Placeholder save function, is this correct?
	def save(self):
		Control_csv()
		Attitude_csv()

	def start(self):
		print ('start simulation')

	def stop(self):
		print ('stop simulation')

	# Sets time, then autoscales to an easy-to-read unit based on the size
	def setTime(self, time):
		self.time = time
		if time < 300:
			self.units = ' seconds'
			self.displayTime = str(self.time)
		elif time < 7200:
			self.units = ' minutes'
			self.displayTime = str(self.time / 60)
		else:
			self.units = ' hours'
			self.displayTime = str(self.time / 3600)
		if not self.timeLabel == None:
			self.selfChanges += 1 # Ignore 1 StringVar change
			self.timeLabel['text'] = 'Runtime: ' + self.displayTime + self.units

	# Sets params for orbital stuff directly, just passes in all the variables
	def setOrbitalParameters(self, Eccentricity, SemiMajorAxis, Inclination, LongitudeAscending, ArgumentPeriapsis, TrueAnomaly):
		self.Eccentricity.set(Eccentricity)
		self.SemiMajorAxis.set(SemiMajorAxis)
		self.Inclination.set(Inclination)
		self.LongitudeAscending.set(LongitudeAscending)
		self.ArgumentPeriapsis.set(ArgumentPeriapsis)
		self.TrueAnomaly.set(TrueAnomaly)

	# Sets the stored attitude of the satellite to given values
	def setAttitude(self, attx, atty, attz):
		self.attitudeX.set(attx)
		self.attitudeY.set(atty)
		self.attitudeZ.set(attz)

	# Sets the labels to the current StringVar values
	def updateLabels(self):
		self.EccentricityLabel['text'] = 'Eccentricity = ' + self.Eccentricity.get()
		self.SemiMajorAxisLabel['text'] = 'Semi-Major Axis = ' + self.SemiMajorAxis.get()
		self.InclinationLabel['text'] = 'Inclination = ' + self.Inclination.get()
		self.LongitudeAscendingLabel['text'] = 'Longitude of Ascending Node = ' + self.LongitudeAscending.get()
		self.ArgumentPeriapsisLabel['text'] = 'Argument of Periapsis = ' + self.ArgumentPeriapsis.get()
		self.TrueAnomalyLabel['text'] = 'True Anomaly = ' + self.TrueAnomaly.get()
		self.attitudeXLabel['text'] = 'X = ' + self.attitudeX.get()
		self.attitudeYLabel['text'] = 'Y = ' + self.attitudeY.get()
		self.attitudeZLabel['text'] = 'Z = ' + self.attitudeZ.get()

	# Initializes the control page of the GUI, building all of the buttons, labels, and entry fields
	def load(self, main):
		# Left Buttons
		ttk.Button(self, text="Save", command=self.save).grid(column=0, row=0, sticky=W)
		ttk.Button(self, text="Start", command=self.start).grid(column=1, row=0, sticky=E)
		ttk.Button(self, text="Stop", command=self.stop).grid(column=2, row=0, sticky=E)
		ttk.Label(self, text="").grid(column=0, row=1) # Spacer
		# Orbital Parameters
		ttk.Label(self, text="Orbital Parameters").grid(column=0, row=2, columnspan=3)
		self.EccentricityLabel = ttk.Label(self, text="Eccentricity = N/A").grid(column=0, row=3, columnspan=2, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.EccentricityEntry).grid(column=2, row=3, sticky=W)
		self.SemiMajorAxisLabel = ttk.Label(self, text="Semi-Major Axis = N/A").grid(column=0, row=4, columnspan=2, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.SemiMajorAxisEntry).grid(column=2, row=4, sticky=W)
		self.InclinationLabel = ttk.Label(self, text="Inclination = N/A").grid(column=0, row=5, columnspan=2, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.InclinationEntry).grid(column=2, row=5, sticky=W)
		self.LongitudeAscendingLabel = ttk.Label(self, text="Longitude of Ascending Node = N/A").grid(column=0, row=6, columnspan=2, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.LongitudeAscendingEntry).grid(column=2, row=6, sticky=W)
		self.ArgumentPeriapsisLabel = ttk.Label(self, text="Argument of Periapsis = N/A").grid(column=0, row=7, columnspan=2, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.ArgumentPeriapsisEntry).grid(column=2, row=7, sticky=W)
		self.TrueAnomalyLabel = ttk.Label(self, text="True Anomaly = N/A").grid(column=0, row=8, columnspan=2, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.TrueAnomalyEntry).grid(column=2, row=8, sticky=W)
		ttk.Label(self, text="").grid(column=0, row=9) # Spacer
		# Attitude
		ttk.Label(self, text="Attitude").grid(column=0, row=10, columnspan=3)
		self.attitudeXLabel = ttk.Label(self, text="X = N/A").grid(column=1, row=11, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.attitudeXEntry).grid(column=2, row=11, sticky=W)
		self.attitudeYLabel = ttk.Label(self, text="Y = N/A").grid(column=1, row=12, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.attitudeYEntry).grid(column=2, row=12, sticky=W)
		self.attitudeZLabel = ttk.Label(self, text="Z = N/A").grid(column=1, row=13, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.attitudeZEntry).grid(column=2, row=13, sticky=W)
		ttk.Label(self, text="").grid(column=0, row=14) # Spacer
		# Update button
		ttk.Button(self, text="Update Matlab", command=main.updateMatlab).grid(column=1, row=15, columnspan=2)
		ttk.Label(self, text="").grid(column=0, row=16) # Spacer
		self.timeLabel = ttk.Label(self, text="Runtime: 0 seconds").grid(column=0, row=17, columnspan=3)


# The diagnostics part of the GUI
# Used for viewing relevant data and statistics while the simulation is running
class DiagnosticsPage(ttk.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(**kwargs)
		# StringVars for displaying
		self.mode = StringVar(self, "Mode: Not Running")
		self.sunExposure = StringVar(self, "Sun Exposure = ?")
		self.powerGeneration = StringVar(self, "Power Generation = ?")
		self.powerDraw = StringVar(self, "Power Draw = ?")
		self.voltage = StringVar(self, "Battery Voltage = ?")
		self.chargePercent = StringVar(self, "Estimated Charge = ?")
		# Displayed Readouts
		ttk.Label(self, textvariable=self.mode).grid(column=0, row=0, sticky=W)
		ttk.Label(self, textvariable=self.sunExposure).grid(column=1, row=0)
		ttk.Label(self, textvariable=self.powerGeneration).grid(column=0, row=1, sticky=E)
		ttk.Label(self, textvariable=self.powerDraw).grid(column=1, row=1, sticky=W)
		ttk.Label(self, textvariable=self.voltage).grid(column=2, row=1)
		ttk.Label(self, textvariable=self.chargePercent).grid(column=2, row=0, sticky=E)
	
	# Diagnostics save functionality
	def Diagnostics_csv(self):
		# Column headers for csv file
		Diagnostics_fields = ['Mode', 'Sun Exposure', 'Power Generation', 'Power Draw', 'Voltage', 'Charge Percent']
		# Data Definition
		Diagnostics_rows = [self.mode.get(), self.sunExposure.get(), self.powerGeneration.get(), self.powerDraw.get(), self.voltage.get(),
		self.chargePercent.get()]
		# name of CSV file
		Diagnostics_filename = 'ControlPage.csv'
		# writing csv file
		with open(Diagnostics_filename, 'w') as csvfile:
			csvwriter = csv.writer(csvfile)
			# writing the fields (column)
			csvwriter.writerow(Diagnostics_fields)
			# writing the data rows
			csvwriter.writerow(Diagnostics_rows)		

	# Setter functions for all Diagnostics

	def setMode(self, mode):
		self.mode = "Mode: " + str(mode)

	def setSunExposure(self, sunExposure):
		self.sunExposure = 'Sun Exposure = ' + str(sunExposure) + ' %'

	def setPowerGeneration(self, powerGeneration):
		self.powerGeneration = 'Power Generation = ' + str(powerGeneration) + ' W'

	def setPowerDraw(self, powerDraw):
		self.powerDraw = 'Power Draw = ' + str(powerDraw) + ' W'

	def setVoltage(self, voltage):
		self.voltage = 'Battery Voltage = ' + str(voltage) + ' V'

	def setChargePercent(self, chargePercent):
		self.chargePercent = 'Estimated Charge = ' + str(chargePercent) + ' %'

	# TODO: Add functionality
	def save(self):
		print ('save file')
		ctrl.Control_csv()
		ctrl.Attitude_csv()
		self.Diagnostics_csv()
	
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
			self.imageLabel = ttk.Label(self, image=self.image).grid(column=1,row=0)
			print ('reloading fully')
		else:
			self.imageLabel.configure(image = self.image)
		disp.after(30, self.loadImage, main, frameSize)
	
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
						self.imageLabel = ttk.Label(self, image=self.image).grid(column=1,row=0)
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
		disp.after(10, self.loadImage, main, frameSize)

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
			self.imageLabel = ttk.Label(self, image=self.image).grid(column=0,row=0)
			print ('reloading fully')
		else:
			self.imageLabel.configure(image = self.image)

#Listener pulls in data from MATLAB
# 'localhost' should be changed to whatever address that needs to be accessed, has the port 50007
HOST, DATAPORT = 'localhost', 50007
def listener(main):
	# Setting up socket, binding to address, listening for one connection
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, DATAPORT))
	s.listen(1)
	# Accept connection
	conn, addr = s.accept()
	# Prints connecting address
	print ('Connected by ', addr, ' for receiving data')
	while 1:
		data = conn.recv(256)
		if not data: break
		# If this returns anything other than 256, bad things happen
		# Can potentially change the size of data received, but 256 is relatively standard and should be enough for now
		#print ('Received data of size ', len(data))
		# Adds in data received from connection to the received data queue
		main.addData(data)
	conn.close()

#Sender sends data to MATLAB
#It is important to keep in mind that if MATLAB expects to receive data and doesn't receive it, it will crash and stop the simulation
#Therefore it is of upmost importance that this sends data fast and sends correctly formatted zero if there's no data, so that MATLAB won't bottleneck on receive
SENDPORT = 50008
def sender(main):
	# Setting up socket, binding to address, listening for one connection
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, SENDPORT))
	s.listen(1)
	# Accept connection
	conn, addr = s.accept()
	# Prints connecting address
	print ('Connected by ', addr, ' for sending data')
	endChar = bytes('|','utf-8')
	while 1:
		# Sends all data in sendData queue
		# If simulink expects to receive data, you NEED to send data, hence why there's a default message in case the send queue is empty
		sentData = False
		while not main.sendEmpty:
			sendData = main.sendData()
			if not sendData == None:
				conn.sendall(bytes(sendData))
				conn.sendall(endChar)
				print ('sending ', sendData)
				sentData = True
		if not sentData:
			conn.sendall(bytes('No Change','utf-8'))
			conn.sendall(endChar)
	conn.close()

#VideoListener pulls in video data specifically from MATLAB
#host address should be the same, but the port will be different
#readsize might change, but should be: height * width * 3
VIDEOPORT = 50080
READSIZE = 1080000

# Listening for video data
def videoListener(main):
	# Setting up socket, binding, listening for 1 connection
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, VIDEOPORT))
	s.listen(1)
	# Accept connection
	conn, addr = s.accept()
	# Prints connecting address
	print ('Connected by ', addr, ' for video')
	totalSize = 0;
	# Reads and queues video data
	while 1:
		data = conn.recv(READSIZE)
		if not data: break
		#print ('Received video data of size ', len(data))
		main.addVideoData(data)
	conn.close()

#DataDecoder takes the data read from MATLAB and converts it into usable values
#This could also potentially schedule helper functions, if you receive data that needs math done
#However math should be scheduled or limited in scope to make this function run as fast as possible so as to limit bottlenecks
def dataDecoder(main):
	while 1:
		if not main.empty:
			data = main.getData()
			if not data == None and len(data)==256:
				#print('Decoding data: ', data)
				time, ecc, smaxis, inc, longasc, argper, tanom, attx, atty, attz, mode, sunex, powgen, powdraw, batv, batc, world, excess = str(data).split(',')
				main.ctrl.setTime(float(time.replace('b','').replace('\'','')))
				main.ctrl.setOrbitalParameters(float(ecc), float(smaxis), float(inc), float(longasc), float(argper), float(tanom))
				main.ctrl.setAttitude(float(attx), float(atty), float(attz))
				main.diag.setMode(mode)
				main.diag.setSunExposure(float(sunex))
				main.diag.setPowerGeneration(float(powgen))
				main.diag.setPowerDraw(float(powdraw))
				main.diag.setVoltage(float(batv))
				main.diag.setChargePercent(float(batc))
			
# Pretty standard GUI setup, similar to most other tkinter GUIs
root = Tk()
root.title("EagleSat Simulation Interface") # Set the window title

# Create a MainPage class and set it to reference the root frame
main = MainPage(root)
main.grid() # The organization function I'm using is grid, this initializes it
root.wm_geometry("1000x800") # Set the initial window size

# Create the subframes of the main frame
ctrl = ControlPage(main)
diag = DiagnosticsPage(main)
disp = DisplayPage(main)

main.loadSubFrames(ctrl,diag,disp)

# Starting the communication threads
dataThread = threading.Thread(target=listener, args=(main, ))
dataThread.daemon = True
dataThread.start()

sendThread = threading.Thread(target=sender, args=(main, ))
sendThread.daemon = True
sendThread.start()

decodingThread = threading.Thread(target=dataDecoder, args=(main, ))
decodingThread.daemon = True
decodingThread.start()

videoThread = threading.Thread(target=videoListener, args=(main, ))
videoThread.daemon = True
videoThread.start()

# Begin the tkinter loop, which simply activates the GUI functionality
root.mainloop()
