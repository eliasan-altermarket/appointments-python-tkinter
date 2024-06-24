# ############################ ############################
# Avgeros Kostas, 166187     
# avgerosk@gmail.com    
# Appointments Project 2023-2024 Hellenic Open University
# ############################ ############################
# 
# ############################ ############################

import tkinter as tk
from tkinter import  scrolledtext
from datetime import datetime


def show_popup(data):
    '''
    Constructs a pop up message with appointment data
    '''
    # Create a new Tkinter window for displaying results
    popup = tk.Toplevel() 
    popup.title("Query results")
    
    # Add a scrolledtext widget to display results with scrollbar
    text_area = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=70, height=20)
    text_area.pack(expand=True, fill='both')

    # Populate scrolledtext widget with queried data
    if isinstance(data, str): # Check if data is str
        text_area.insert(tk.END, data)
    else:
        for row in data:
            email_q, slot_q, AppointmentID_q, firstname_q, lastname_q = row
            slot_q = datetime.strptime(slot_q, '%Y-%m-%dT%H:%M').strftime('%B %d, %Y at %I:%M %p')
            # Insert each piece of data into the text area
            text_area.insert(tk.END, f"Email: {email_q}\n")
            text_area.insert(tk.END, f"Slot: {slot_q}\n")
            text_area.insert(tk.END, f"Appointment ID: {AppointmentID_q}\n")
            text_area.insert(tk.END, f"First Name: {firstname_q}\n")
            text_area.insert(tk.END, f"Last Name: {lastname_q}\n")
            # Add a newline after each row
            text_area.insert(tk.END, '\n')
