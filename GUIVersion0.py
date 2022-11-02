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

#   BELLO
#	def changeState(self,text):
#		self.state_lbl['text'] = text

	def addData(self,data):
		self.queue.put(data)
		self.empty = self.queue.empty()

	def addVideoData(self,data):
		self.videoQueue.put(data)
		self.videoEmpty = self.videoQueue.empty()
		self.currentVideoFrameSize += len(data)

	def calculateVideoFrameSize(self):
		self.currentVideoFrameSize = 0
		for idx in range(self.videoQueue.qsize()):
			data = self.getVideoData()
			self.currentVideoFrameSize += len(data)
			self.addData(data)

	def getVideoData(self):
		if not self.videoQueue.empty():
			data = self.videoQueue.get()
			self.currentVideoFrameSize -= len(data)
			return data

		self.videoEmpty = self.videoQueue.empty()

	def loadSubFrames(self,ctrl,diag,disp):
		self.disp = disp
		self.disp.grid(row=0, column=1)
		self.ctrl = ctrl
		ctrl.grid(row=0, column=0)
		self.diag = diag
		diag.grid(row=1, column=0, columnspan=2)
		ctrl.load()
		disp.load("forklift600.jpg", self, READSIZE)

	def updateImage(self, loadedImage):
		if self.imageLabel == None:
			self.imageLabel = ttk.Label(self, image=loadedImage).grid(column=1,row=0)
			print ('reloading fully')
		else:
			self.imageLabel.configure(image = loadedImage)

	def getData(self):
		if not self.queue.empty():
			return self.queue.get()
		self.empty = self.queue.empty()

	def checkEmpty(self):
		return self.queue.empty()

	def queueData(self, data):
		self.sendQueue.put(data)
		self.sendEmpty = self.sendQueue.empty()

	def sendData(self):
		if not self.sendQueue.empty():
			return self.sendQueue.get()
		self.sendEmpty = self.sendQueue.empty()

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
		# Attitude and Simulation Time
		self.attitudeX = StringVar()
		self.attitudeY = StringVar()
		self.attitudeZ = StringVar()
		self.time = 0
		self.displayTime = None
		self.units = None
		self.timeLabel = None

	def save(self):
		print ('save file')

	def start(self):
		print ('start simulation')

	def stop(self):
		print ('stop simulation')

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
			self.timeLabel['text'] = 'Runtime: ' + self.displayTime + self.units

	def setOrbitalParameters(self, Eccentricity, SemiMajorAxis, Inclination, LongitudeAscending, ArgumentPeriapsis, TrueAnomaly):
		self.Eccentricity.set(Eccentricity)
		self.SemiMajorAxis.set(SemiMajorAxis)
		self.Inclination.set(Inclination)
		self.LongitudeAscending.set(LongitudeAscending)
		self.ArgumentPeriapsis.set(ArgumentPeriapsis)
		self.TrueAnomaly.set(TrueAnomaly)

	def setAttitude(self, attx, atty, attz):
		self.attitudeX.set(attx)
		self.attitudeY.set(atty)
		self.attitudeZ.set(attz)

	def load(self):
		# Left Buttons
		ttk.Button(self, text="Save", command=self.save).grid(column=0, row=0, sticky=W)
		ttk.Button(self, text="Start", command=self.start).grid(column=1, row=0, sticky=E)
		ttk.Button(self, text="Stop", command=self.stop).grid(column=2, row=0, sticky=E)
		ttk.Label(self, text="").grid(column=0, row=1) # Spacer
		# Orbital Parameters
		ttk.Label(self, text="Orbital Parameters").grid(column=0, row=2, columnspan=3)
		ttk.Label(self, text="Eccentricity = ").grid(column=0, row=3, columnspan=2, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.Eccentricity).grid(column=2, row=3, sticky=W)
		ttk.Label(self, text="Semi-Major Axis = ").grid(column=0, row=4, columnspan=2, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.SemiMajorAxis).grid(column=2, row=4, sticky=W)
		ttk.Label(self, text="Inclination = ").grid(column=0, row=5, columnspan=2, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.Inclination).grid(column=2, row=5, sticky=W)
		ttk.Label(self, text="Longitude of Ascending Node = ").grid(column=0, row=6, columnspan=2, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.LongitudeAscending).grid(column=2, row=6, sticky=W)
		ttk.Label(self, text="Argument of Periapsis = ").grid(column=0, row=7, columnspan=2, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.ArgumentPeriapsis).grid(column=2, row=7, sticky=W)
		ttk.Label(self, text="True Anomaly = ").grid(column=0, row=8, columnspan=2, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.TrueAnomaly).grid(column=2, row=8, sticky=W)
		ttk.Label(self, text="").grid(column=0, row=9) # Spacer
		# Attitude and Simulation Time
		ttk.Label(self, text="Attitude").grid(column=0, row=10, columnspan=3)
		ttk.Label(self, text="X = ").grid(column=1, row=11, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.attitudeX).grid(column=2, row=11, sticky=W)
		ttk.Label(self, text="Y = ").grid(column=1, row=12, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.attitudeY).grid(column=2, row=12, sticky=W)
		ttk.Label(self, text="Z = ").grid(column=1, row=13, sticky=E)
		ttk.Entry(self, width=10, textvariable=self.attitudeZ).grid(column=2, row=13, sticky=W)
		ttk.Label(self, text="").grid(column=0, row=14) # Spacer
		self.timeLabel = ttk.Label(self, text="Runtime: 0 seconds").grid(column=0, row=15, columnspan=3)

class DiagnosticsPage(ttk.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(**kwargs)
		# Numerical Readouts
		self.mode = ttk.Label(self, text="Mode: Not Running").grid(column=0, row=0, sticky=W)
		self.sunExposure = ttk.Label(self, text="Sun Exposure = 0 %").grid(column=1, row=0)
		self.powerGeneration = ttk.Label(self, text="Power Generation = 0 W").grid(column=0, row=1, sticky=E)
		self.powerDraw = ttk.Label(self, text="Power Draw = 0 W").grid(column=1, row=1, sticky=W)
		self.voltage = ttk.Label(self, text="Battery Voltage = 0 V").grid(column=2, row=1)
		self.chargePercent = ttk.Label(self, text="Estimated Charge = 0 %").grid(column=2, row=0, sticky=E)

	def setMode(self, mode):
		if not self.mode == None:
			self.mode['text'] = 'Mode: ' + str(mode)

	def setSunExposure(self, sunExposure):
		if not self.sunExposure == None:
			self.sunExposure['text'] = 'Sun Exposure = ' + str(sunExposure) + ' %'

	def setPowerGeneration(self, powerGeneration):
		if not self.powerGeneration == None:
			self.powerGeneration['text'] = 'Power Generation = ' + str(powerGeneration) + ' W'

	def setPowerDraw(self, powerDraw):
		if not self.powerDraw == None:
			self.powerDraw['text'] = 'Power Draw = ' + str(powerDraw) + ' W'

	def setVoltage(self, voltage):
		if not self.voltage == None:
			self.voltage['text'] = 'Battery Voltage = ' + str(voltage) + ' V'

	def setChargePercent(self, chargePercent):
		if not self.chargePercent == None:
			self.chargePercent['text'] = 'Estimated Charge = ' + str(chargePercent) + ' %'

HEIGHT, WIDTH = 600, 600
class DisplayPage(ttk.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(**kwargs)
		self.currentVideoFrame = None
		self.image = None
		self.imageLabel = None

	def load(self, filename, main, frameSize):
		placeholder = Image.open(filename)
		self.image = ImageTk.PhotoImage(placeholder)
		if self.imageLabel == None:
			self.imageLabel = ttk.Label(self, image=self.image).grid(column=1,row=0)
			print ('reloading fully')
		else:
			self.imageLabel.configure(image = self.image)
		disp.after(30, self.loadImage, main, frameSize)

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
					#print("Final frame is of size ", len(img))
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
		disp.after(30, self.loadImage, main, frameSize)


#		img = bytearray()
#		while not main.videoEmpty and main.currentVideoFrameSize < frameSize:
#			img.append(bytearray(main.getVideoData()))
#		if not img == None and main.currentVideoFrameSize >= frameSize:
#			print("Final frame is of size ", len(img))
#			self.currentVideoFrame = Image.frombytes("RGB",[600,600],bytes(img))
#			self.image = ImageTk.PhotoImage(self.currentVideoFrame)

	def loadImageManually(self, data):
		self.currentVideoFrame = Image.frombytes("RGB",[600,600],data)
		self.image = ImageTk.PhotoImage(self.currentVideoFrame)
		if self.imageLabel == None:
			self.imageLabel = ttk.Label(self, image=self.image).grid(column=0,row=0)
			print ('reloading fully')
		else:
			self.imageLabel.configure(image = self.image)

#Listener pulls in data from MATLAB
HOST, DATAPORT = 'localhost', 50007
def listener(main):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, DATAPORT))
	s.listen(1)
	conn, addr = s.accept()
	print ('Connected by ', addr)
	while 1:
		data = conn.recv(256)
		if not data: break
		print ('Received data of size ', len(data))
		main.addData(data)
		main.queueData(data)
		while not main.sendEmpty:
			sendData = main.sendData()
			if not sendData == None:
				conn.sendall(bytes(sendData))
			else:
				conn.sendall(b'0')
	conn.close()

#VideoListener pulls in video data specifically from MATLAB
VIDEOPORT = 50008
READSIZE = 1080000
def videoListener(main):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, VIDEOPORT))
	s.listen(1)
	conn, addr = s.accept()
	print ('Connected by ', addr, ' for video')
	totalSize = 0;
	while 1:
		data = conn.recv(READSIZE)
		if not data: break
		print ('Received video data of size ', len(data))
		main.addVideoData(data)
	conn.close()

#DataDecoder takes the data read from MATLAB and converts it into usable values
def dataDecoder(main):
	while 1:
		if not main.empty:
			data = main.getData()
			if not data == None:
				print('Decoding data: ', data)
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

root = Tk()
root.title("EagleSat Simulation Interface")

main = MainPage(root)
main.grid()
root.wm_geometry("1000x800")

ctrl = ControlPage(main)
diag = DiagnosticsPage(main)
disp = DisplayPage(main)

main.loadSubFrames(ctrl,diag,disp)

dataThread = threading.Thread(target=listener, args=(main, ))
dataThread.daemon = True
dataThread.start()

decodingThread = threading.Thread(target=dataDecoder, args=(main, ))
decodingThread.daemon = True
decodingThread.start()

videoThread = threading.Thread(target=videoListener, args=(main, ))
videoThread.daemon = True
videoThread.start()

root.mainloop()