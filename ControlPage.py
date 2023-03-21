from tkinter import *
from tkinter import ttk

import csv

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
            # self.timeLabel['text'] = 'Runtime: ' + self.displayTime + self.units # TODO: Make this work

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
    # TODO: CURRENTLY UNUSED WILL NEED TO BE FIXED
    # def updateLabels(self):
    #     self.EccentricityLabel['text'] = 'Eccentricity = ' + self.Eccentricity.get()
    #     self.SemiMajorAxisLabel['text'] = 'Semi-Major Axis = ' + self.SemiMajorAxis.get()
    #     self.InclinationLabel['text'] = 'Inclination = ' + self.Inclination.get()
    #     self.LongitudeAscendingLabel['text'] = 'Longitude of Ascending Node = ' + self.LongitudeAscending.get()
    #     self.ArgumentPeriapsisLabel['text'] = 'Argument of Periapsis = ' + self.ArgumentPeriapsis.get()
    #     self.TrueAnomalyLabel['text'] = 'True Anomaly = ' + self.TrueAnomaly.get()
    #     self.attitudeXLabel['text'] = 'X = ' + self.attitudeX.get()
    #     self.attitudeYLabel['text'] = 'Y = ' + self.attitudeY.get()
    #     self.attitudeZLabel['text'] = 'Z = ' + self.attitudeZ.get()

    # Initializes the control page of the GUI, building all of the buttons, labels, and entry fields
    def load(self, main):
        # Left Buttons
        ttk.Button(self, text="Save").grid(column=0, row=0, sticky=W) # command=self.save 
        ttk.Button(self, text="Start", command=self.start).grid(column=1, row=0, sticky=E)
        ttk.Button(self, text="Stop", command=self.stop).grid(column=2, row=0, sticky=E)
        ttk.Label(self, text="").grid(column=0, row=1) # Spacer
        # Orbital Parameters
        ttk.Label(self, text="Orbital Parameters").grid(column=0, row=2, columnspan=3)
        self.EccentricityLabel = ttk.Label(self, text="Eccentricity = N/A")
        self.EccentricityLabel.grid(column=0, row=3, columnspan=2, sticky=E)
        ttk.Entry(self, width=10, textvariable=self.EccentricityEntry).grid(column=2, row=3, sticky=W)
        self.SemiMajorAxisLabel = ttk.Label(self, text="Semi-Major Axis = N/A")
        self.SemiMajorAxisLabel.grid(column=0, row=4, columnspan=2, sticky=E)
        ttk.Entry(self, width=10, textvariable=self.SemiMajorAxisEntry).grid(column=2, row=4, sticky=W)
        self.InclinationLabel = ttk.Label(self, text="Inclination = N/A")
        self.InclinationLabel.grid(column=0, row=5, columnspan=2, sticky=E)
        ttk.Entry(self, width=10, textvariable=self.InclinationEntry).grid(column=2, row=5, sticky=W)
        self.LongitudeAscendingLabel = ttk.Label(self, text="Longitude of Ascending Node = N/A")
        self.LongitudeAscendingLabel.grid(column=0, row=6, columnspan=2, sticky=E)
        ttk.Entry(self, width=10, textvariable=self.LongitudeAscendingEntry).grid(column=2, row=6, sticky=W)
        self.ArgumentPeriapsisLabel = ttk.Label(self, text="Argument of Periapsis = N/A")
        self.ArgumentPeriapsisLabel.grid(column=0, row=7, columnspan=2, sticky=E)
        ttk.Entry(self, width=10, textvariable=self.ArgumentPeriapsisEntry).grid(column=2, row=7, sticky=W)
        self.TrueAnomalyLabel = ttk.Label(self, text="True Anomaly = N/A")
        self.TrueAnomalyLabel.grid(column=0, row=8, columnspan=2, sticky=E)
        ttk.Entry(self, width=10, textvariable=self.TrueAnomalyEntry).grid(column=2, row=8, sticky=W)
        ttk.Label(self, text="").grid(column=0, row=9) # Spacer
        # Attitude
        ttk.Label(self, text="Attitude").grid(column=0, row=10, columnspan=3)
        self.attitudeXLabel = ttk.Label(self, text="X = N/A")
        self.attitudeXLabel.grid(column=1, row=11, sticky=E)
        ttk.Entry(self, width=10, textvariable=self.attitudeXEntry).grid(column=2, row=11, sticky=W)
        self.attitudeYLabel = ttk.Label(self, text="Y = N/A")
        self.attitudeYLabel.grid(column=1, row=12, sticky=E)
        ttk.Entry(self, width=10, textvariable=self.attitudeYEntry).grid(column=2, row=12, sticky=W)
        self.attitudeZLabel = ttk.Label(self, text="Z = N/A")
        self.attitudeZLabel.grid(column=1, row=13, sticky=E)
        ttk.Entry(self, width=10, textvariable=self.attitudeZEntry).grid(column=2, row=13, sticky=W)
        ttk.Label(self, text="").grid(column=0, row=14) # Spacer
        # Update button
        ttk.Button(self, text="Update Matlab", command=main.updateMatlab).grid(column=1, row=15, columnspan=2)
        ttk.Label(self, text="").grid(column=0, row=16) # Spacer
        self.timeLabel = ttk.Label(self, text="Runtime: 0 seconds")
        self.timeLabel.grid(column=0, row=17, columnspan=3)