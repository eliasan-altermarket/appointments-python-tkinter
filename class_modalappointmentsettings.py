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
import os
import sys
from class_rightpath import *

class ModalAppointmentSettings (tk.Toplevel):
    """
    Create a modal window
    param: parent, the parent tkinter object
    param: wdg_timeslot, the TimeSlotWidget object
    """
    def __init__(self, parent, wdg_timeslot):

        # __init__ function for class Tk
        super().__init__(parent)

        self.wdg_timeslot = wdg_timeslot
        self.transient(parent)
        # All events are focused to this modal window
        self.grab_set()
        self.focus_set()  # This line sets the focus to the modal window
        # Calculate dimensions to center the window on screen
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Specify window width and height
        window_width = 460
        window_height = 400 # (1: 1.875 ratio)
        # Calculate position coordinates
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        
        # Icon. Like Favicon but for the window.
        # Instatanate an rp object with the name of the icon.
        rp = Right_path("./business_construction_avatar_engineer_man_employee_person_worker_icon_262353.ico")
        # Call rp.resource_path() to form the right path for the icon resource.
        self.iconbitmap(rp.resource_path())
        # self.iconbitmap(os.path.join(sys.path[0], "./business_construction_avatar_engineer_man_employee_person_worker_icon_262353.ico"))

        self.style_dialog_header = ttk.Style()
        self.style_dialog_header.configure('DialogHeader.TLabel', foreground='antiquewhite4', font=("Arial", 20, "bold italic"))

        self.style_times = ttk.Style()
        self.style_times.configure('Times.TLabel', foreground='antiquewhite4', font=("Arial", 14, "bold"))
        self.style_data = ttk.Style()
        self.style_data.configure('Data.TLabel', foreground='black', font=("Arial", 12, "bold"))

        # creating a container
        container = ttk.Frame(self)  
        # container.pack(side = "top", fill = "both", expand = True)
        container.grid(row=0, column=0)
        if self.wdg_timeslot.appointment is not None:
            self.title("Delete Appointment")
            customer_data = self.get_customer_data(self.wdg_timeslot.appointment.customer_id)
            if customer_data is None:
                messagebox.showerror ("Error!", "I couldn't find customer's data!\nThis could be due to an error while communicatiing with the data base.")
                self.destroy()
            # Timeslot has an appointment
            lbl_header = ttk.Label(container, text="Appointment Data", style="DialogHeader.TLabel")
            lbl_header.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
            
            lbl_customer = ttk.Label(container, text="Customer")
            lbl_customer.grid(row=1, column=0, padx=5, pady=5, sticky="W")

            lbl_customer_fullname = ttk.Label(container, text=self.wdg_timeslot.appointment.customer_ln + " " + self.wdg_timeslot.appointment.customer_fn )
            lbl_customer_fullname.grid(row=1, column=1, padx=5, pady=5, sticky="W")

            lbl_customer = ttk.Label(container, text="Customer")
            lbl_customer.grid(row=1, column=0, padx=5, pady=5, sticky="W")

            lbl_customer_fullname = ttk.Label(container, text=self.wdg_timeslot.appointment.customer_ln + " " + self.wdg_timeslot.appointment.customer_fn, style="Data.TLabel")
            lbl_customer_fullname.grid(row=1, column=1, padx=5, pady=5, sticky="W")

            lbl_time1 = ttk.Label(container, text="Appointment Start Time")
            lbl_time1.grid(row=2, column=0, padx=5, pady=5, sticky="W")

            lbl_start_time = ttk.Label(container, text=self.wdg_timeslot.timeslot_obj.get_str_starttime(), style="Times.TLabel")
            lbl_start_time.grid(row=2, column=1, padx=5, pady=5, sticky="W")

            lbl_time2 = ttk.Label(container, text="Appointment End Time")
            lbl_time2.grid(row=3, column=0, padx=5, pady=5, sticky="W")

            lbl_end_time = ttk.Label(container, text=self.wdg_timeslot.timeslot_obj.get_str_endtime(), style="Times.TLabel")
            lbl_end_time.grid(row=3, column=1, padx=5, pady=5, sticky="W")

            lbl_email = ttk.Label(container, text="Email")
            lbl_email.grid(row=4, column=0, padx=5, pady=5, sticky="W")

            lbl_email_customer = ttk.Label(container, text=customer_data[4], style="Data.TLabel")
            lbl_email_customer.grid(row=4, column=1, padx=5, pady=5, sticky="W")

            lbl_phone = ttk.Label(container, text="Phone")
            lbl_phone.grid(row=5, column=0, padx=5, pady=5, sticky="W")

            lbl_phone_customer = ttk.Label(container, text=customer_data[3], style="Data.TLabel")
            lbl_phone_customer.grid(row=5, column=1, padx=5, pady=5, sticky="W")

            lbl_question = ttk.Label(container, text="Do you want to delete this appointment?", style="Data.TLabel")
            lbl_question.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

            close_button =  ttk.Button(container, text='No', command=self.destroy)
            close_button.grid(row=7, column=0)
            
            save_button =  ttk.Button(container, text='Yes', command=self.delete_appointment)
            save_button.grid(row=7, column=1, padx=10, pady=10)
        else:
            self.title("New Appointment")
            # Timeslot is empty. No appointment yet
            lbl_header = ttk.Label(container, text="New Appointment", style="DialogHeader.TLabel")
            lbl_header.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
            
            lbl_customer = ttk.Label(container, text="Select Customer")
            lbl_customer.grid(row=1, column=0, padx=5, pady=5, sticky="W")
            
            # Create an optionMenu widget that shows customer names
            # Create a dictionary with customer names as keys and IDs as values
            """
            # Test Data
            self.customers = {"Antonopoulos Ilias":123, "Pappas George":234, "Santel Marina":231, "Tatopoulou Korina":1244}
            """
            # Get a dictionary that contains customer names and customer IDs
            self.customers = self.get_customers_dict()
            # Initialize the ID to -1, which makes no sense
            self.selected_customer_id = -1
            
            ###############################################################
            ##### ListBox START
            ###############################################################
            """
            I use a ListBox with scroll bars to display the list of customers.
            User selects the customer for the appointment.
            """
            frame = ttk.Frame(container)
            frame.grid(row=1, column=1, padx=15, pady=15)
            
            # Create a scrollbar
            scrollbar = tk.Scrollbar(frame)
            scrollbar.grid(row=0, column=1, sticky='ns')

            # Create a listbox
            self.listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, height=8, width=30)
            for name in self.customers.keys():
                self.listbox.insert(tk.END, name)
            self.listbox.bind('<<ListboxSelect>>', self.on_select)
            self.listbox.grid(row=0, column=0, sticky='nsew')

            # Configure the scrollbar
            scrollbar.config(command=self.listbox.yview)

            # Configure the grid to expand properly when resizing
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(0, weight=1)
            ###############################################################
            ##### END ListBox
            ###############################################################

            lbl_time1 = ttk.Label(container, text="Appointment Start Time")
            lbl_time1.grid(row=2, column=0, padx=5, pady=5, sticky="W")

            lbl_start_time = ttk.Label(container, text=self.wdg_timeslot.timeslot_obj.get_str_starttime(), style="Times.TLabel")
            lbl_start_time.grid(row=2, column=1, padx=5, pady=5, sticky="W")

            lbl_time2 = ttk.Label(container, text="Appointment End Time")
            lbl_time2.grid(row=3, column=0, padx=5, pady=5, sticky="W")

            lbl_end_time = ttk.Label(container, text=self.wdg_timeslot.timeslot_obj.get_str_endtime(), style="Times.TLabel")
            lbl_end_time.grid(row=3, column=1, padx=5, pady=5, sticky="W")

            close_button =  ttk.Button(container, text='Cancel', command=self.destroy)
            close_button.grid(row=4, column=0)
            
            save_button =  ttk.Button(container, text='Save', command=self.save_appointment)
            save_button.grid(row=4, column=1)

    def on_select(self, event):
        """
        Handles the select event of the ListBox that displays customers
        """
        # Get selected line index
        list_index = self.listbox.curselection()[0]
        # Get the line's text
        self.selected_customer_name = self.listbox.get(list_index)
        # Print the corresponding ID from the dictionary
        print('Customer Name:', self.selected_customer_name)
        print('Customer ID:', self.customers[self.selected_customer_name])
        # Store the selected customer's ID to 
        # self.selected_customer_id variable
        self.selected_customer_id = self.customers[self.selected_customer_name]
    
    def save_appointment(self):
        """
        Saves the appointment to the database.
        """
        if self.selected_customer_id == -1:
            messagebox.showerror ("Error!", "You haven't selected a customer!\nPlease select a customer, to add a new appointment.")
            return
        else:
            # Save the appointment
            # Add code to save the appointment
            # - Update database
            # - Update widget's info
            """
            Saves the appointment to the database.
            Connects to the database, executes the statement.
            Displays a message box if something went wrong
            """
            db = appDatabase()
            db.connect()
            appointment_data = (self.selected_customer_id, self.wdg_timeslot.timeslot_obj.get_db_startdate(), self.wdg_timeslot.timeslot_obj.get_db_enddate(), 0)
            # Add the appointment and return its appointment id
            app_id = db.add_appointment(appointment_data)
            db.close()
            if app_id is None:
                messagebox.showerror ("Error!", "Unable to store appointment data to the data base.")
            else:
                # Split the full name to LastName and FirstName
                split_name = self.selected_customer_name.split(' ')
                last_name = split_name[0]
                first_name = split_name[1]
                # Display new appointment info
                self.wdg_timeslot.show_appointment_to_timeslot(self.wdg_timeslot.timeslot_obj.get_str_starttime(), self.wdg_timeslot.timeslot_obj.get_str_endtime(), last_name, first_name, self.selected_customer_id)
                # Create a new appointment object
                self.wdg_timeslot.appointment = Appointment(self.wdg_timeslot.timeslot_obj.get_db_startdate(), self.wdg_timeslot.timeslot_obj.get_db_enddate(), app_id, 0, self.selected_customer_id, first_name, last_name)
                # Close Window
                self.destroy()

    def delete_appointment(self):
        """Delete an appointment"""
        db = appDatabase()
        db.connect()
        # Delete the appointment from the db
        db.delete_appointment(self.wdg_timeslot.appointment.appointment_id)
        db.close()

        # Delete appointment object from the timeslot
        self.wdg_timeslot.appointment = None
        # Remove appointment info from the timeslot
        self.wdg_timeslot.empty_timeslot(self.wdg_timeslot.timeslot_obj.get_str_starttime(), self.wdg_timeslot.timeslot_obj.get_str_endtime())
        # Close Window
        self.destroy()
    
    
    def customer_changed(self, *args):
        """
        OptionMenu - When a selection is made, get the ID using the selected name
        """
        # When a selection is made, get the ID using the selected name
        print("Selected ID:", self.customers[self.selected_customer.get()])

    def get_customers_dict(self):
        """
        Returns a dictionary that contains all customers as:
        {"FullName":CustomerID, etc}
        Connects to the database, runs the query and returns the result as a dictionary
        """
        db = appDatabase()
        db.connect()
        dict_all_customers = db.all_customers_dict()
        db.close()
        return dict_all_customers

    def get_customer_data(self, customer_id):
        """
        Returns a tuple that contains all customer's data:
        CustomerID, FirstName, LastName, Phone, Email, Deleted
        Connects to the database, runs the query and returns the result as a tuple
        """
        db = appDatabase()
        db.connect()
        tuple_data = db.get_customer_data(customer_id)
        db.close()
        return tuple_data


if __name__ == "__main__":
    pass