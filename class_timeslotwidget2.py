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
from class_modalappointmentsettings import *
import time
import re

class TimeSlotWidget2(ttk.Label):
    """
    Creates a label for the time slot.
    param: ts_object, an object of class TimeSlot
    param: r, the row to grid it
    param: c, the column to grid it
    param: timeslot_style, the style to use to draw the label (defined in App)
    """
    def __init__(self, parent, ts_object, r, c, timeslot_style):
        super().__init__(master=parent, 
                         text = ts_object.get_str_starttime()+"-"+ts_object.get_str_endtime(), 
                         style=timeslot_style)

        self.timeslot_obj = ts_object
        self.dbStartDate = ts_object.get_db_startdate()
        self.dbEndDate = ts_object.get_db_enddate()
        self.appointment = ts_object.get_appointment()

        # Change the style for the timeslot that has an appointment
        if self.appointment is not None:
            self.show_appointment_to_timeslot(ts_object.get_str_starttime(), ts_object.get_str_endtime(), self.appointment.customer_fn, self.appointment.customer_ln, self.appointment.customer_id)
            #print("Found an appointment! " + self.dbStartDate)

        # Test - Open Messagebox
        # self.bind('<Double-1>', self.dosomething01)
        
        # Open Modal Settings window for apointment manipulation
        self.bind('<Double-1>', self.open_modal_window)

        # Left mouse click to show the parent of the widget
        # self.bind('<Button-1>', self.on_left_mouse_click)

        # This places the TimeSlotWidget instance in the grid of its parent
        self.grid()
        self.grid(row=r, column=c, ipadx=2, ipady=2)    
    
    def show_appointment_to_timeslot(self, start_time, end_time, fname, lname, id):
        self.config(style='TimeslotBooked.TLabel')
        timeslotText = start_time + "-" + end_time
        self.config(text=timeslotText + " (" + lname + " " + fname + ")" + " (" + str(id) + ")")

    def empty_timeslot(self, start_time, end_time):
        self.config(style='Timeslot.TLabel')
        timeslotText = start_time + "-" + end_time
        self.config(text=timeslotText)


    def open_modal_window(self, event):
        # event.widget.winfo_id() # Get the ID of the widget
        
        # Use the event object to find the widget that triggered
        # the event
        the_timeslot = event.widget
        # Confirmation 1 that works.
        # Print the widget
        # print(f"The widget that triggered the event is: {the_timeslot}")
        #
        # Confirmation 2 that works.
        # Change timeslot's style
        # the_timeslot.config(style='TimeslotBooked.TLabel')        
        
        # To get the appointment associated with this
        # timeslot you can use two ways:
        # a) Call the method: the_timeslot.timeslot_obj.get_appointment()
        # b) Get the property: the_timeslot.appointment
        
        self.settingsWindow = ModalAppointmentSettings(self, the_timeslot)
        # Wait until the modal window is closed (destroyed)
        self.wait_window(self.settingsWindow)
        # self.bind('<Button-1>', self.play_sound)


if __name__ == "__main__":
    pass