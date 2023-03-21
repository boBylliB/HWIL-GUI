from tkinter import ttk, StringVar, W, E
import csv

# The diagnostics part of the GUI
# Used for viewing relevant data and statistics while the simulation is running
class DiagnosticsPage(ttk.Frame):
	""" Diagnostics Page GUI

	This class holds all things related to diagnostics and saving to CSV

	Attributes
	----------
	mode : StringVar
		Displays current mode\n
	sunExposure : StringVar
		Displays current sun exposure\n
	powerGeneration : StringVar
		Displays current power generation\n
	powerDraw : StringVar
		Displays current power draw\n
	voltage : StringVar
		Displays current voltage\n
	chargePercent : StringVar
		Displays current charge percentage
	
	Methods
	-------
	Diagnostics_csv(): 
		Saves diagnostic data to a csv\n
	Setters:
		Sets all of the string vars according to name. Not writing all those out.\n
	"""
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
		#ctrl.Control_csv()
		#ctrl.Attitude_csv()
		self.Diagnostics_csv()
