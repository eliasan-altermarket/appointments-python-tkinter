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
from datetime import datetime, timedelta, date
from tkinter.font import Font
from src.utils import fetch_email, send_email, save_to_excel


# Define About Page
class AboutPage01(tk.Frame):
    """
    Displays the about info.
    """
     
    def __init__(self, parent, controller):
         
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        # Set the minimum width of the row that will hold the
        # controls to 1400
        # That way, we prevent the flickering as we recreate
        # the week widget.
        self.grid_columnconfigure(0, weight=1, minsize=1400)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        # Set column 0 width
        self.column0_width=700
        # Set padx, pady values for frames
        self.padx_frame = 10
        self.pady_frame = 10
        # Set padx, pady values for widgets
        self.padx_widget = 5
        self.pady_widget = 2
        # Set the color used for headers
        # Picked among the list found in https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html
        self._header_color = "navy"

        ############################################
        # Header START
        ############################################
        # Set the minimum width of the topHeader frame that will hold the controls to 700
        # That way, we prevent the flickering as we recreate
        # the week widget.
        top_header = ttk.Frame(self, width=self.column0_width, height=120)
        top_header.grid(row=0, column=0, pady=self.pady_frame)
        # Use the grid_propagate method to prevent the frame from resizing to fit its contents
        top_header.grid_propagate(True)
        
        # Get today's date in a datetime object
        self.today = datetime.today()

        header = ttk.Label(top_header, text="About the Appointments Application", style='Header.TLabel')
        header.grid(row=0, column=0, columnspan=3)
        headerLabel01 = ttk.Label(top_header, text=self.today.strftime('%Y-%m-%d'), style='Clock.TLabel')
        headerLabel01.grid(row=1, column=0)

        clock = Clock(top_header, style='Clock.TLabel')
        clock.grid(row=1, column=2)
        ############################################
        # Header END
        ############################################


        about_header = ttk.Frame(self, width=self.column0_width, height=120)
        about_header.grid(row=1, column=0, pady=self.pady_frame)
        # Use the grid_propagate method to prevent the frame from resizing to fit its contents
        about_header.grid_propagate(True)

        header_title = ttk.Label(about_header, text="Hellenic Open University :: Python Course 2023-2024", font="Arial 24 bold", foreground=self._header_color)
        header_title.grid(row=0, column=0, pady=(50,10), padx=50)

        header_project = ttk.Label(about_header, text="\"This application for managing appointments, was developed as part of the Python course, class 2023-2024. It is based on Python and Tkinter.\"", font="Arial 12 bold")
        header_project.grid(row=1, column=0, pady=1, padx=50)

        header_professor = ttk.Label(about_header, text="Professor", font="Arial 20", foreground=self._header_color)
        # pady and padx can take as input tupples that represnet the (top,bottom) and (left, right) padding
        header_professor.grid(row=2, column=0, pady=(50,10))

        header_professor_name = ttk.Label(about_header, text="Kiourt Chairi", font="Arial 16")
        header_professor_name.grid(row=3, column=0, pady=1)


        label_students = ttk.Label(about_header, text="Developers", font="Arial 20 ", foreground=self._header_color)
        label_students.grid(row=4, column=0, pady=(50,10))

        label_name01 = ttk.Label(about_header, text="Ilias Antonopoulos", font="Arial 16")
        label_name01.grid(row=5, column=0, pady=1)
        label_name01_details = ttk.Label(about_header, text="Email: eliasan@altermarket.com", font="Arial 12")
        label_name01_details.grid(row=6, column=0, pady=1)

        label_name02 = ttk.Label(about_header, text="Kostas Avgeros", font="Arial 16")
        label_name02.grid(row=7, column=0, pady=(20,1))
        label_name02_details = ttk.Label(about_header, text="Email: avgerosk@gmail.com", font="Arial 12")
        label_name02_details.grid(row=8, column=0, pady=1)


if __name__ == "__main__":
    pass


