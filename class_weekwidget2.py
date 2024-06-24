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
from class_daywidget2 import *
import time
import re

class WeekWidget2(ttk.Frame):
    """
    Creates a frame for the week. Inside this frame, there are the day frames.
    param: monthObj, the current month object
    param: frame_style, the style to use to draw the frame
    param: day_style, the style to use to draw the day
    param: timeslot_style, the style to use to draw the timeslot labels (defined in App)
    """
    def __init__(self, parent, monthObj, week_style, day_style, timeslot_style, week_index=-1):
        super().__init__(master=parent, style=week_style)

        self.monthObj = monthObj
        self.week_index = week_index
        
        # To implement later
        # self.week_index = self.monthObj.get_week_index_for_day()
        
        if self.week_index == -1:
            # Returns a list with the Day objects that belong to current date.
            self.week_days_list = self.monthObj.get_todays_week_days()
        if self.week_index >= 0 and self.week_index <= 4:
            # Returns a list with the Day objects that belong to a week of the month.
            self.week_days_list = self.monthObj.get_week_days(self.week_index)
        # A list of all days of the week
        self.days = []

        # This places the WeekWidget instance in the grid of its parent
        self.grid(row=1, column=0)

        # Create a new frame inside this WeekWidget2 instance
        week_frame = ttk.Frame(self, style=week_style)
        week_frame.grid(padx=10, pady=10)   

        list_len = len(self.week_days_list)
        for i in range(0, list_len):
            self.days.append( DayWidget2(week_frame, self.week_days_list[i], 1, i, day_style, timeslot_style))


if __name__ == "__main__":
    pass