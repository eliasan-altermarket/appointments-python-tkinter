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
from class_weekwidget2 import *
import time
import re

# Week Page (actually it is a frame)
class WeekPage(ttk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        ttk.Frame.__init__(self, self.parent)

        # Set the minimum width of the row that will hold the
        # controls to 1400
        # That way, we prevent the flickering as we recreate
        # the week widget.
        self.grid_columnconfigure(0, weight=1, minsize=1400)
        self.grid_columnconfigure(2, weight=1)

        ############################################
        # Header START
        # Set the minimum width of the topHeader frame that will hold the controls to 700
        # That way, we prevent the flickering as we recreate
        # the week widget.
        topHeader = ttk.Frame(self, width=700, height=120)
        topHeader.grid(row=0, column=0)
        # Use the grid_propagate method to prevent the frame from resizing to fit its contents
        topHeader.grid_propagate(False)
        
        # Get today's date in a datetime object
        self.today = datetime.today()

        header = ttk.Label(topHeader, text="Appointments - Weekly Calendar", style='Header.TLabel')
        header.grid(row=0, column=0, columnspan=3)
        headerLabel01 = ttk.Label(topHeader, text=self.today.strftime('%Y-%m-%d'), style='Clock.TLabel')
        headerLabel01.grid(row=1, column=0)

        clock = Clock(topHeader, style='Clock.TLabel')
        clock.grid(row=1, column=2)

        # Combo boxes for Year and Month Selection
        # Create the frame that will hold them
        # Frame has as a parent the topHeader frame
        yearMonthSelect = ttk.Frame(topHeader)
        yearMonthSelect.grid(row=1, column=1)
        # Add to frame, 2 labels and 2 combo boxes
        labelYear = ttk.Label(yearMonthSelect, text="Year")
        labelYear.grid(row=0, column=0)
        self.comboYear = ttk.Combobox(yearMonthSelect, 
            state="readonly",
            values = list(range(2024,2061))

        )
        # Set year to current and add combo box to grid
        self.yearNumber = int(self.today.strftime('%Y'))
        self.comboYear.set(str(self.yearNumber))
        self.comboYear.grid(row=1, column=0)
        # Do something when the year changes
        # Update displayed dates (week), timeslots and appointments
        self.comboYear.bind('<<ComboboxSelected>>', self.on_month_year_selected)

        labelMonth = ttk.Label(yearMonthSelect, text="Month")
        labelMonth.grid(row=0, column=1)
        self.comboMonth = ttk.Combobox(yearMonthSelect, 
            state="readonly",
            values=list(range(1, 13))
        )
        # Set month to current and add combo box to grid
        self.monthNumber = int(self.today.strftime('%m'))
        self.comboMonth.set(str(self.monthNumber))
        self.comboMonth.grid(row=1, column=1)
        # Do something when the month changes
        self.comboMonth.bind('<<ComboboxSelected>>', self.on_month_year_selected)


        btPreviousWeek = ttk.Button(topHeader, text="<< Previous Week", command=self.previous_week)
        btPreviousWeek.grid(row=2, column=0, sticky="W")
        btNextWeek = ttk.Button(topHeader, text="Next Week >>", command=self.next_week)
        btNextWeek.grid(row=2, column=2, sticky="E")
        # Header END
        ############################################
        
        #self.display_week()
        self.thisMonth = Month(self.today)
        self.current_week_index = self.thisMonth.current_week_index
        self.week = WeekWidget2(self, self.thisMonth, 'Week.TFrame', 'Day.TFrame', 'Timeslot.TLabel')

    def display_week(self, ym_change=False, wi=-1):
        if ym_change == False:
            self.thisMonth = Month(self.today)
            # If there already a self.week destroy it
            # and recreate it. It flickers the screen
            # as all elements are recreated
            if self.week.winfo_exists():
                self.week.destroy()
            self.week = WeekWidget2(self, self.thisMonth, 'Week.TFrame', 'Day.TFrame', 'Timeslot.TLabel', self.current_week_index)
        else:
            # If there already a self.week destroy it
            # and recreate it. It flickers the screen
            # as all elements are recreated
            if self.week.winfo_exists():
                self.week.destroy()
            self.newdate = datetime(self.yearNumber, self.monthNumber, 1, 0, 0)
            self.thisMonth = Month( self.newdate )
            self.week = WeekWidget2(self, self.thisMonth, 'Week.TFrame', 'Day.TFrame', 'Timeslot.TLabel', self.current_week_index)
    
    
    def on_month_year_selected(self, event):
        self.monthNumber = int(self.comboMonth.get())
        self.yearNumber = int(self.comboYear.get())
        self.display_week(ym_change=True)

    def previous_week(self):
        self.current_week_index -= 1
        if self.current_week_index < 0:
            self.current_week_index = 0
        #print("After Previous self.current_week_index: " + str(self.current_week_index))
        self.display_week(True, self.current_week_index)

    def next_week(self):
        self.current_week_index += 1
        if self.current_week_index > 4:
            self.current_week_index = 4
        #print("After Next self.current_week_index: " + str(self.current_week_index))
        self.display_week(True, self.current_week_index)

if __name__ == "__main__":
    pass