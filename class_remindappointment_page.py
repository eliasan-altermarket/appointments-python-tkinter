"""
Author: Ilias Antonopoulos
eliasan@altermarket.com
www.altermarket.com, www.kalliergo.gr
Appointments Project, 2023-2024 Hellenic Open University
"""

import tkinter as tk
from tkinter import ttk, Menu, messagebox, Toplevel, Frame
# We have to install this to use normal images in Tkinter
from PIL import ImageTk, Image
from tkinter import messagebox
from librarycalendar07 import *
from database import *
from class_clock import *
import time
import re

# Define Remind Appointment Page
# Select date and send email to customers that have an appointment.
# You could also export the appointments data for that day.
# To be implemented by Kostas
class RemindAppointment(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
         
        # Contents
        label1 = ttk.Label(self, text ="Remind Appointments", font = ("Verdana", 35))
        # putting the grid in its place by using
        # grid
        label1.grid(row = 0, column = 0, padx = 10, pady = 10) 
  
        label2 = ttk.Label(self, text ="Select date and send email to customers that have an appointment.", font = ("Verdana", 15))
        label2.grid(row = 1, column = 0, padx = 10, pady = 10) 

        label3 = ttk.Label(self, text ="You could also export the appointments of that day.", font = ("Verdana", 15))
        label3.grid(row = 2, column = 0, padx = 10, pady = 10) 


if __name__ == "__main__":
    pass