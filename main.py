"""
Main function for the HWIL GUI
"""
import Network
# Tkinter imports
from tkinter import Tk

# Other pages imports
from MainPage import MainPage
from ControlPage import ControlPage
from DiagnosticsPage import DiagnosticsPage
from DisplayPage import DisplayPage

root = Tk()

root.title("EagleSat Sim Interface")

main = MainPage(root)

main.grid()
root.wm_geometry("1000x800")

ctrl = ControlPage(main)
diag = DiagnosticsPage(main)
disp = DisplayPage(main)

main.loadSubFrames(ctrl, diag, disp)

root.mainloop()
