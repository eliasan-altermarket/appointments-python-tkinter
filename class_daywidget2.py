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
from class_timeslotwidget2 import *
import time
import re

class DayWidget2(ttk.Frame):
    """
    Creates a frame for the day. Inside this frame, there are the time slots.
    param: day_obj, a Day object
    ### param: day_info, Info about the day (eg day name)
    ### param: timeslots_data, the data for all timeslots (a list of tuples)
    param: r, row
    param: c, column
    param: day_style, the style to use to draw the this day frame
    param: timeslot_style, the style to use to draw the timeslot labels
    """
    # def __init__(self, parent, day_info, timeslots_data, r, c, day_style, timeslot_style):
    def __init__(self, parent, day_obj, r, c, day_style, timeslot_style):
        super().__init__(master=parent, style=day_style)

        self.day_obj = day_obj
        # A list of all timeslots for the day
        self.timeslots = []

        # This places the DayWidget instance in the grid of its parent
        self.grid(row=r, column=c)

        # Create a new frame inside this DayWidget instance
        self.day_frame = ttk.Frame(self, style=day_style)
        self.day_frame.grid()

        # Get the Name of the Day (Monday ... Sunday) as astring
        dayName = ttk.Label(self.day_frame, text=self.day_obj.get_weekday_name(), style='DayNameData.TLabel')
        dayName.grid(row=0, column=0)
        # Get the Date of the Day (18-05-2024) as astring
        dayDate = ttk.Label(self.day_frame, text=self.day_obj.get_weekday_date(), style='DayNameData.TLabel')
        dayDate.grid(row=1, column=0)

        # Get the timeslot data from the Day Object
        timeslots_data = self.day_obj.timeslots
        list_len = len(timeslots_data)
        for i in range(0, list_len):
            self.timeslots.append( TimeSlotWidget2(self.day_frame, timeslots_data[i], i+2, 0, timeslot_style) )


if __name__ == "__main__":
    pass