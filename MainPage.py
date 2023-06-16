# from tkinter import *
from tkinter import ttk

from queue import Queue

# class for the GUI itself
# holds each section of the GUI within itself, and acts to bridge the gap and hold utility functions
class MainPage(ttk.Frame):
    """ Main page GUI

    This class holds the general functions for the main page.

    Attributes
    ----------
    ctrl : ControlPage
        Control Page GUI that will be shown in a subframe\n
    diag : DiagnosticsPage
        Diagnositc page GUI that will be shown in a subframe\n
    disp : DisplayPage
        Display Page GUI that will be shown in a subframe\n
    
    Methods
    -------
    loadSubFrames(ctrl, diag, disp): 
        Loads other pages to be displayed\n
    updateImage(loadedImage): 
        Loads and displays given image to screen\n
    """

    def __init__(self, *args, **kwargs):
        # TODO: Will need to go through this to find what we do and don't need
        super().__init__(**kwargs)
        self.ctrl = None
        self.diag = None
        self.disp = None
        self.requestImageLoad = False # Not sure if we need this
        self.queue = Queue() # Probably be moved to a data class
        self.sendQueue = Queue() # Same here
        self.videoQueue = Queue() # And here
        self.currentVideoFrameSize = 0 # Also here
        self.empty = True # Data stuff still
        self.videoEmpty = True # More Data stuff
        self.sendEmpty = True # Still more data stuff
#    def changeState(self,text):
#        self.state_lbl['text'] = text


    # Adding data to the queue, for any received numeric data
    # Probably don't need it here in the main page, will probably be better in a seperate class, not
    # specific to the gui
    def addData(self,data):
        self.queue.put(data)
        self.empty = self.queue.empty()

    # Adding data to video queue, solely used for receiving video frames from the simulink animation
    # Probably don't need it here in the main page, will probably be better in a seperate class, not
    # specific to the gui
    def addVideoData(self,data):
        self.videoQueue.put(data)
        self.videoEmpty = self.videoQueue.empty()
        self.currentVideoFrameSize += len(data)


    # Calculating how large the current video queue would be if read as a single frame
    # Used to compare to the desired video frame size
    # Probably don't need it here in the main page, will probably be better in a seperate class, not
    # specific to the gui
    def calculateVideoFrameSize(self):
        self.currentVideoFrameSize = 0
        # Loops through each entry in the video queue, and sums up the total video data size
        for idx in range(self.videoQueue.qsize()):
            data = self.getVideoData()
            self.currentVideoFrameSize += len(data)
            self.addData(data)


    # Retrieve video data from queue
    # Probably don't need it here in the main page, will probably be better in a seperate class, not
    # specific to the gui
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
        """Initializes subframe in main window to display images

        Parameters
        ----------
        ctrl : ControlPage
            The Control Page GUI to be put into a subframe\n
        daig : DiagnosticsPage
            The Diagnostics Page GUI to be put into a subframe\n
        disp : DisplayPage
            The Display Page GUI to be put into a subframe\n

        """
        self.disp = disp
        self.disp.grid(row=0, column=1)
        self.ctrl = ctrl
        ctrl.grid(row=0, column=0)
        self.diag = diag
        diag.grid(row=1, column=0, columnspan=2)
        ctrl.load(self)
        READSIZE = 1080000 # HACK: This should be changed later
        disp.load("forklift600.jpg", self, READSIZE) # TODO: MOVE TO DATA CLASS

    # Get numeric data from the queue of received data
    # Probably don't need it here in the main page, will probably be better in a seperate class, not
    # specific to the gui
    def getData(self):
        if not self.queue.empty():
            return self.queue.get()
        self.empty = self.queue.empty()

    # Checks if the received data queue is empty
    # Probably don't need it here in the main page, will probably be better in a seperate class, not
    # specific to the gui
    def checkEmpty(self):
        return self.queue.empty()

    # Probably don't need it here in the main page, will probably be better in a seperate class, not
    # specific to the gui
    def updateMatlab(self, *args):
        # Build dataset in the same format as the received dataset
        dataString = str(self.ctrl.EccentricityEntry.get()) + "," + str(self.ctrl.SemiMajorAxisEntry.get()) + "," + str(self.ctrl.InclinationEntry.get()) + "," + str(self.ctrl.LongitudeAscendingEntry.get()) + "," + str(self.ctrl.ArgumentPeriapsisEntry.get()) + "," + str(self.ctrl.TrueAnomalyEntry.get()) + "," + str(self.ctrl.attitudeXEntry.get()) + "," + str(self.ctrl.attitudeYEntry.get()) + "," + str(self.ctrl.attitudeZEntry.get())
        # Convert to bytes and queue it
        data = bytes(dataString,'utf-8')
        self.queueData(data)

    # Adds received data to the queue
    # Probably don't need it here in the main page, will probably be better in a seperate class, not
    # specific to the gui
    def queueData(self, data):
        self.sendQueue.put(data)
        self.sendEmpty = self.sendQueue.empty()

    # Used for sending data back to simulink, if the send queue isn't empty it'll return the next item of data to send
    # Probably don't need it here in the main page, will probably be better in a seperate class, not
    # specific to the gui
    def sendData(self):
        if not self.sendQueue.empty():
            return self.sendQueue.get()
        self.sendEmpty = self.sendQueue.empty()
