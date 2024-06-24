# ############################ ############################
# Avgeros Kostas, 166187     
# avgerosk@gmail.com    
# Appointment Project 2023-2024 Hellenic Open University
# ############################ ############################
# Define Appointments Search Page
# ############################ ############################

import tkinter as tk
from tkinter import ttk, Menu, messagebox, Toplevel, Frame, scrolledtext

# We have to install this to use normal images in Tkinter
from PIL import ImageTk, Image
from librarycalendar07 import *
from database import *
from class_clock import *
import time
import re
from tkcalendar import Calendar
from datetime import datetime, date
import os
import sqlite3
# from src.utils import fetch_email, send_email, save_to_excel, show_popup
from src.utils import show_popup, fetch_email, save_to_excel
from src.models.process_excel import ModuleExcel


class AppointmentsSearch(tk.Frame):
    '''
    A class used to represent appointments page
    '''
    def __init__(self, parent, controller):     
        tk.Frame.__init__(self, parent)          

        # Contents / gridding at the end 
        label1 = ttk.Label(self, text ="Appointments Search Page", font = ("Verdana", 15)) 
        label1.grid(row = 0, column = 0, padx = 20, pady = 10) 

        label2 = ttk.Label(self, text ="Enter or Select a date to show the appointments for that date.")
        label2.grid(row = 1, column = 0, padx = 20, pady = 10) 

        label3 = ttk.Label(self, text ="Next, we can send reminders to customers having an appointment using emails, or export the list of appointments as an Excel file.")
        label3.grid(row = 2, column = 0, padx = 20, pady = 10) 

        # Create the main frame #4 where all functions will be hosted
        frame = ttk.LabelFrame(self, text="Central Window")
        frame.grid(row = 3, column = 0) 

        # Create a new frame to hold email & excel functions
        search_frame = ttk.LabelFrame(frame, text="Functions")
        search_frame.grid(row=0, column=0)

        # Add Buttons
        button_mail = ttk.Button(search_frame, text="Send Email", command= lambda: send_email_handler(cal.get_date()))
        button_excel = ttk.Button(search_frame, text="Create Excel", command= lambda: save_to_excel_handler(cal.get_date()))
        button_preview = ttk.Button(frame, text = "Preview", command= lambda: show_popup_handler(cal.get_date()))

        # Grid it side by side
        button_mail.grid(row=1, column=0)
        button_excel.grid(row=1, column=1)
        button_preview.grid(row = 1, column = 0) 

        # Create Calendar
        cal = Calendar(frame, date_pattern="yyyy-mm-dd")
        cal.grid(row=2, column=0)

        date = ttk.Label(frame, text = " ")
        date.grid(row=3, column=0)

        # Smart trick. Change padding and more pythonic
        def configure_widgets(frame, padx, pady):
            for widget in frame.winfo_children():
                widget.grid_configure(sticky="news", padx=padx, pady=pady)

        configure_widgets(frame, padx=50, pady=10)
        configure_widgets(search_frame, padx=20, pady=10)


def send_email_handler(date):  
    '''
    Function that handles email query db
    ''' 
    time_now = datetime.now().strftime('%H:%M')
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\tToday: {today}\ttime-now: {time_now}\t\tselected date: {date}")
    db = appDatabase()
    db.connect()
    results = db.query_email(today, time_now, date)
    db.close()
    fetch_email(results)


def save_to_excel_handler(date):   
    '''
    Function that handles excel query db
    '''
    db = appDatabase()            
    db.connect()
    results = db.query_excel(date)
    db.close()
    save_to_excel(results, date)
  

def show_popup_handler(date):
    '''
    Executes query and shows result in a popup window
    '''
    db = appDatabase()         
    db.connect()
    results = db.query_preview(date)
    db.close()
    print(results)
    show_popup(results)


# # # START. This code is not part of the active code. It is here only for informational purposes. # # # 
class SecureSQLite: 
    '''
    A class used to represent SQLite
    '''
    def __init__(self, db_path):
        '''
        Parameters
        ----------
        db_path : string 
            Path of the database
        '''
        self.db_path = db_path
        self.conn = None

    def execute_query(self, query, params=None):
        '''Executes the query with or without parameters'''
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if conn:
                print("\tDB closed")
                conn.close()
# # # END. This code is not part of the active code. It is here only for informational purposes. # # # 

if __name__ == "__main__":
    # handler = ModuleExcel()
    pass