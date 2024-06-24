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
from class_customers_page import *
from class_clock import *
from class_week_page import *
from class_weekwidget2 import *
from class_daywidget2 import *
from class_timeslotwidget2 import *
from class_modalappointmentsettings import *
#from class_remindappointment_page import *
from class_appointments_search_page import *
from class_about_page import *
import time
import re
import os
import sys
from class_rightpath import *


#############################################
# Main Application
#############################################
class App(tk.Tk):
    """
    Class that holds the main app
    """
   
    def __init__(self, *args, **kwargs):
        
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Appointments Management for a Small Business")
        # Calculate dimensions to center the window on screen
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Specify window width and height
        window_width = 1400
        window_height = 850
        # Calculate position coordinates
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        
        # Icon. Like Favicon but for the window.
        # Instatanate an rp object with the name of the icon.
        rp = Right_path("./business_construction_avatar_engineer_man_employee_person_worker_icon_262353.ico")
        # Call rp.resource_path() to form the right path for the icon resource.
        self.iconbitmap(rp.resource_path())

        ############################################
        # Create Styles
        style_timeslot_label = ttk.Style()
        style_timeslot_label.configure('Timeslot.TLabel', foreground='black', borderwidth=1, relief="solid", width=27)
        
        style_timeslot_booked_label = ttk.Style()
        style_timeslot_booked_label.configure('TimeslotBooked.TLabel', foreground='white', background="green", borderwidth=1, relief="solid", width=27)

        style_daynamedata_label = ttk.Style()
        style_daynamedata_label.configure('DayNameData.TLabel', foreground='black', background='antiquewhite1')

        style_day_frame = ttk.Style()
        style_day_frame.configure('Day.TFrame', borderwidth=0, relief="solid", background='antiquewhite1')

        style_week_frame = ttk.Style()
        style_week_frame.configure('Week.TFrame', borderwidth=0, relief="solid", background='antiquewhite3')

        style_header_label = ttk.Style()
        style_header_label.configure('Header.TLabel', foreground='antiquewhite4', font=("Montserrat", 20, "bold italic"))

        style_clock_label = ttk.Style()
        style_clock_label.configure('Clock.TLabel', foreground='white', background='black', font=("Arial", 12, "bold"))


        # creating a container
        container = tk.Frame(self)  
        # container.pack(side = "top", fill = "both", expand = True)
        container.grid(row=0, column=0)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # initializing frames to an empty dictionary
        self.frames = {}

        # initializing windows to an empty dictionary
        self.windows = {}


        # iterating through a tuple consisting
        # of the different page layouts
        for frame_class in (WeekPage, AppointmentsSearch, CustomersPage01, AboutPage01):
  
            frame = frame_class(container, self)
  
            # initializing frame of that object from
            # StartPage, WeekPage, Page3 respectively with 
            # for loop
            self.frames[frame_class] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")

        # Create Menu Bar START ###########################################
        main_menubar = Menu(self)
        self.config(menu=main_menubar)

        # create the Appointments Menu
        appointments_menu = Menu(
            main_menubar,
            tearoff=0
        )             

        # add menu items to the Appointments Menu
        appointments_menu.add_command(label='Calendar (weekly)', command=lambda : self.show_frame(WeekPage))
        appointments_menu.add_command(label='Appointments Search', command=lambda : self.show_frame(AppointmentsSearch))
        #appointments_menu.add_command(label='Start Page', command=lambda : self.show_frame(StartPage))
        appointments_menu.add_separator()
        # add Exit menu item
        appointments_menu.add_command(
            label='Exit', command=self.destroy
        )

        main_menubar.add_cascade(
            label="Appointments",
            menu=appointments_menu,
            underline=0
        )

        # create the Customers Menu
        customers_menu = Menu(
            main_menubar,
            tearoff=0
        )             

        # add menu items to Customers Menu
        customers_menu.add_command(label='Customers Management', command=lambda : self.show_frame(CustomersPage01))
        #customers_menu.add_command(label='Υπενθύμιση Ραντεβού', command=lambda : self.show_frame(RemindAppointment))

        main_menubar.add_cascade(
            label="Customers",
            menu=customers_menu,
            underline=0
        )

        main_menubar.add_command(
            label="About",
            command = lambda : self.show_frame(AboutPage01)
        )

        # Create Menu Bar END ###########################################

        # On start, display this Page
        self.show_frame(WeekPage)


    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
    