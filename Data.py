from queue import Queue

# Important constants
# Host and dataport for reciving from matlab
HOST, DATAPORT = 'localhost', 50007
# Sending port and delay for matlab
SENDPORT = 50008
SENDDELAY = 0.15 # This is the minimum, cannot go lower


class Data():

    # Throw all the initial stuff in here, might needs some predefined stuff
    # Who knows
    def __init__(self):
        pass

    #########################
    ### DATA MANIPULATION ###
    #########################

    # Adds data to the data queue, used for numeric data
    def addData(self, data):
        pass

    # Add data to video queue, used to receive frames to be displayed
    def addVideoData(self, data):
        pass

    # Calculates how big the
    def calculateVideoFrameSize(self):
        pass

    # Adding data to the queue
    # Old function also updates the sendEmpty variable, but that is
    # redundant with the checkEmpty() function
    def queueData(self, data):
        pass


    ####################
    ### GETTING DATA ###
    ####################

    def getVideoData(self):
        pass

    def checkEmpty(self):
        pass


    def sendData(self):
        pass
