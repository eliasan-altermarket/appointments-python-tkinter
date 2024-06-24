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


# Define Customers Page 
class CustomersPage01(tk.Frame):
     
    def __init__(self, parent, controller):
         
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        # Set the minimum width of the row that will hold the
        # controls to 1400
        # That way, we prevent the flickering as we recreate
        # the week widget.
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        # Set column 0 width
        self.column0_width=500
        # Set padx, pady values for frames
        self.padx_frame = 10
        self.pady_frame = 10
        # Set padx, pady values for widgets
        self.padx_widget = 5
        self.pady_widget = 2
        # How many customers to show in table view
        self.how_many_customers_to_show = 5
        # Limit of the query (how many records to return each time)
        self.limit = 10
        self.offset = 0
        # List that holds parts that form the query
        # [0]: SELECT part
        # [1]: WHERE part
        # [2]: ORDER part
        # [3]: LIMIT part TO (limit)
        self.query_parts = ["SELECT * FROM customers", "WHERE Deleted=0", "ORDER BY CustomerID", self.limit]
        # self.current_customer holds either -1 (meaning no selection), or the list with values from selected row
        self.current_customer = -1

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

        header = ttk.Label(top_header, text="Customers Management", style='Header.TLabel')
        header.grid(row=0, column=0, columnspan=3)
        headerLabel01 = ttk.Label(top_header, text=self.today.strftime('%Y-%m-%d'), style='Clock.TLabel')
        headerLabel01.grid(row=1, column=0)

        clock = Clock(top_header, style='Clock.TLabel')
        clock.grid(row=1, column=2)
        ############################################
        # Header END
        ############################################

        ############################################
        # Search Form START
        ############################################
        search_form = ttk.Frame(self, width=self.column0_width, height=120)
        search_form.grid(row=1, column=0, padx=self.padx_frame, pady=self.pady_frame, sticky="W")
        
        # Display title
        lbl_search_title = ttk.Label(search_form, text="Search Form")
        lbl_search_title.grid(row=0, column=0, columnspan=2, sticky="W")

        # Display Labels and Fields
        self.search_id = tk.StringVar()
        lbl_id = ttk.Label(search_form, text="ID")  
        lbl_id.grid(row=1, column=0, padx=self.padx_widget, pady=self.pady_widget, sticky="W")
        entr_id = ttk.Entry (search_form, textvariable=self.search_id)  
        entr_id.grid(row=1, column=1, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        self.search_first_name = tk.StringVar()
        lbl_id = ttk.Label(search_form, text="First Name")  
        lbl_id.grid(row=2, column=0, padx=self.padx_widget, pady=self.pady_widget, sticky="W")
        entr_id = ttk.Entry (search_form, textvariable=self.search_first_name)  
        entr_id.grid(row=2, column=1, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        self.search_last_name = tk.StringVar()
        lbl_id = ttk.Label(search_form, text="Last Name")  
        lbl_id.grid(row=3, column=0, padx=self.padx_widget, pady=self.pady_widget, sticky="W")
        entr_id = ttk.Entry (search_form, textvariable=self.search_last_name)  
        entr_id.grid(row=3, column=1, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        self.search_phone = tk.StringVar()
        lbl_id = ttk.Label(search_form, text="Phone")  
        lbl_id.grid(row=4, column=0, padx=self.padx_widget, pady=self.pady_widget, sticky="W")
        entr_id = ttk.Entry (search_form, textvariable=self.search_phone)  
        entr_id.grid(row=4, column=1, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        self.search_email = tk.StringVar()
        lbl_id = ttk.Label(search_form, text="Email")  
        lbl_id.grid(row=5, column=0, padx=self.padx_widget, pady=self.pady_widget, sticky="W")
        entr_id = ttk.Entry (search_form, textvariable=self.search_email)  
        entr_id.grid(row=5, column=1, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        # Frame to hold search related buttons
        search_buttons = ttk.Frame(search_form, width=self.column0_width, height=120)
        search_buttons.grid(row=6, column=0, padx=self.padx_frame, pady=self.pady_frame, columnspan=2, sticky="W")

        bt_search = ttk.Button(search_buttons, text="Search", command=self.search_customers)
        bt_search.grid(row=0, column=0, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        bt_clear = ttk.Button(search_buttons, text="Clear", command=self.clear_search_fields)
        bt_clear.grid(row=0, column=1, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        bt_all = ttk.Button(search_buttons, text="All", command=self.all_customers)
        bt_all.grid(row=0, column=2, padx=self.padx_widget, pady=self.pady_widget, sticky="W")
        ############################################
        # Search Form END
        ############################################

        # Show customers in Table View, with offset=0
        self.display_table(offset=0)


    ############################################
    # Customers Treeview START
    ############################################
    def display_table(self, offset):
        """
        Display the treeview widget that shows customers and the related buttons
        """

        # Make sure that no customer is selected.
        self.current_customer = -1

        # Get the number of customers
        self.customers_count = self.number_of_records()
        self.table_frame = ttk.Frame(self, width=self.column0_width, height=120)
        self.table_frame.grid(row=2, column=0, padx=self.padx_frame)
        
        column_headers = ("ID", "F. Name", "L. Name", "Phone", "Email")

        # Get the recorset that contains the customers
        db = appDatabase()
        db.connect()
        # The recorset that contains the customers
        self.customers_rd = db.get_customers_with_limit(self.query_parts, offset)
        db.close()
        
        # ATTENTION! Height for Treeview is set on number of rows. Not pixels.
        self.tbl_customers = ttk.Treeview(
            self.table_frame, columns=column_headers, show="headings", padding=0, height=self.how_many_customers_to_show, selectmode="browse"
        )

        #############################################  #TODO @kostas
        # Define the widths for each column index in a dictionary
        column_widths = {
            0: 40,
            1: 120,
            2: 120,
            3: 120,
            4: 120
        }

        # Iterate over the column headers
        for i in column_headers:
            # Get the index of the current header
            index = column_headers.index(i)
            
            # Get the width from the dictionary, defaulting to a specific width if the index is not found
            width = column_widths.get(index, 120)
            
            # Set the column properties
            self.tbl_customers.column(i, anchor="center", width=width)

            # Place header strings
            self.tbl_customers.heading(i, text=column_headers[index])
        #############################################

        # Fill tree view with rows from the recordset
        for i in range(0, len(self.customers_rd)):
            # We start with "" because we create a new top-level item.
            # We use tk.END to tell that the next item will be added at the end of the list.
            self.tbl_customers.insert("", tk.END, values=self.customers_rd[i])
        
        self.tbl_customers.grid(row=0, column=0, sticky=tk.NSEW, padx=0, pady=0)

        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tbl_customers.yview)
        self.tbl_customers.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Bind the Left Mouse Button Release event
        self.tbl_customers.bind('<ButtonRelease-1>', self.select_customer)

        # Add Prev, Next buttons
        nav_buttons_frame = ttk.Frame(self.table_frame, width=self.column0_width, height=30)
        nav_buttons_frame.grid(row=1, column=0, padx=self.padx_frame, pady=self.pady_frame)

        int_back = offset - self.limit
        
        int_next = offset + self.limit

        bt_prev = ttk.Button( nav_buttons_frame, text="< Previous", command=lambda: self.display_table(int_back))
        bt_prev.grid(row=0, column=0, sticky="E")

        bt_next = ttk.Button( nav_buttons_frame, text="Next >", command=lambda: self.display_table(int_next))
        bt_next.grid(row=0, column=1, sticky="E")

        # If we have reached the end of the recordset, disable next button
        bt_next['state'] = 'disabled'
        if self.customers_count <= int_next:
            bt_next['state'] = 'disabled'
        else:
            bt_next['state'] = 'normal'

        # If we have reached the start of the recordset, disable prev button
        bt_prev['state'] = 'disabled'
        if int_back >= 0:
            bt_prev['state'] = 'normal'
        else:
            bt_prev['state'] = 'disabled'

        # Edit buttons
        edit_buttons_frame = ttk.Frame(self.table_frame, width=self.column0_width, height=30)
        edit_buttons_frame.grid(row=2, column=0, padx=self.padx_frame, pady=self.pady_frame)
        
        bt_edit = ttk.Button( edit_buttons_frame, text="Edit", command=self.edit_customer)
        bt_edit.grid(row=0, column=0, sticky="E")

        bt_unselect = ttk.Button( edit_buttons_frame, text="Unselect", command=self.unselect_customer)
        bt_unselect.grid(row=0, column=1, sticky="E")

        bt_add = ttk.Button( edit_buttons_frame, text="Add", command=self.add_customer)
        bt_add.grid(row=0, column=2, sticky="E")

        bt_delete = ttk.Button( edit_buttons_frame, text="Delete", command=self.delete_customer)
        bt_delete.grid(row=0, column=3, sticky="E")

        bt_email = ttk.Button( edit_buttons_frame, text="Appointments", command=self.list_appointments_customer)
        bt_email.grid(row=0, column=4, sticky="E")

        ############################################
        # Customers Treeview END
        ############################################

    ############################################
    # Edit Customers START
    ############################################
    def edit_customer_form(self, show=0):
        """
        Configure and display the customer's edit form
        """
        if self.current_customer != -1:
            customer_id = int(self.tbl_customers.item(self.current_customer)['values'][0])
            customer_fn = self.tbl_customers.item(self.current_customer)['values'][1]
            customer_ln = self.tbl_customers.item(self.current_customer)['values'][2]
            customer_phone = self.tbl_customers.item(self.current_customer)['values'][3]
            customer_email = self.tbl_customers.item(self.current_customer)['values'][4]
        else:
            # self.current_customer isn't valid. Return.
            return

        # Edit Form
        self.edit_customer_frame = ttk.Frame(self, width=self.column0_width, height=30)
        self.edit_customer_frame.grid(row=1, column=1, padx=self.padx_frame, pady=self.pady_frame)

        # Display title
        lbl_search_title = ttk.Label(self.edit_customer_frame, text="Custmer Data")
        lbl_search_title.grid(row=0, column=0, columnspan=1, sticky="W")

        # Display Labels and Fields
        lbl_id = ttk.Label(self.edit_customer_frame, text="ID")  
        lbl_id.grid(row=1, column=0, padx=self.padx_widget, pady=self.pady_widget, sticky="W")
        lbl_id_value = ttk.Label(self.edit_customer_frame, text=customer_id)  
        lbl_id_value.grid(row=1, column=1, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        self.customer_first_name = tk.StringVar()
        self.customer_first_name.set(customer_fn)
        lbl_fn = ttk.Label(self.edit_customer_frame, text="First Name")  
        lbl_fn.grid(row=2, column=0, padx=self.padx_widget, pady=self.pady_widget, sticky="W")
        entr_fn = ttk.Entry (self.edit_customer_frame, textvariable=self.customer_first_name)  
        entr_fn.grid(row=2, column=1, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        self.customer_last_name = tk.StringVar()
        self.customer_last_name.set(customer_ln)
        lbl_ln = ttk.Label(self.edit_customer_frame, text="Last Name")  
        lbl_ln.grid(row=3, column=0, padx=self.padx_widget, pady=self.pady_widget, sticky="W")
        entr_ln = ttk.Entry (self.edit_customer_frame, textvariable=self.customer_last_name)  
        entr_ln.grid(row=3, column=1, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        self.customer_phone = tk.StringVar()
        self.customer_phone.set(customer_phone)
        lbl_phone = ttk.Label(self.edit_customer_frame, text="Phone")  
        lbl_phone.grid(row=4, column=0, padx=self.padx_widget, pady=self.pady_widget, sticky="W")
        entr_phone = ttk.Entry (self.edit_customer_frame, textvariable=self.customer_phone)  
        entr_phone.grid(row=4, column=1, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        self.customer_email = tk.StringVar()
        self.customer_email.set(customer_email)
        lbl_email = ttk.Label(self.edit_customer_frame, text="Email")  
        lbl_email.grid(row=5, column=0, padx=self.padx_widget, pady=self.pady_widget, sticky="W")
        entr_email = ttk.Entry (self.edit_customer_frame, textvariable=self.customer_email)  
        entr_email.grid(row=5, column=1, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        # Buttons frame
        edit_buttons_frame = ttk.Frame(self.edit_customer_frame, width=self.column0_width, height=30)
        edit_buttons_frame.grid(row=6, column=0, padx=self.padx_frame, pady=self.pady_frame, columnspan=2)        

        # Edit buttons
        bt_save = ttk.Button( edit_buttons_frame, text="Save", command=lambda: self.save_customer_db(customer_id))
        bt_save.grid(row=0, column=0, sticky="E")

        bt_cancel = ttk.Button( edit_buttons_frame, text="Cancel", command=self.hide_edit_customer)
        bt_cancel.grid(row=0, column=1, sticky="E")
        ############################################
        # Edit Customers END
        ############################################


    ############################################
    # Add Customer START
    ############################################
    def add_customer_form(self):
        """
        Configure and display the "add a customer" form
        """
        # Add Form
        self.add_customer_frame = ttk.Frame(self, width=self.column0_width, height=30)
        self.add_customer_frame.grid(row=1, column=1, padx=self.padx_frame, pady=self.pady_frame)

        # Display title
        lbl_search_title = ttk.Label(self.add_customer_frame, text="Add Customer")
        lbl_search_title.grid(row=0, column=0, columnspan=1, sticky="W")

        # Display Labels and Fields
        self.customer_first_name = tk.StringVar()
        lbl_fn = ttk.Label(self.add_customer_frame, text="First Name")  
        lbl_fn.grid(row=2, column=0, padx=self.padx_widget, pady=self.pady_widget, sticky="W")
        entr_fn = ttk.Entry (self.add_customer_frame, textvariable=self.customer_first_name)  
        entr_fn.grid(row=2, column=1, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        self.customer_last_name = tk.StringVar()
        lbl_ln = ttk.Label(self.add_customer_frame, text="Last Name")  
        lbl_ln.grid(row=3, column=0, padx=self.padx_widget, pady=self.pady_widget, sticky="W")
        entr_ln = ttk.Entry (self.add_customer_frame, textvariable=self.customer_last_name)  
        entr_ln.grid(row=3, column=1, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        self.customer_phone = tk.StringVar()
        lbl_phone = ttk.Label(self.add_customer_frame, text="Phone")  
        lbl_phone.grid(row=4, column=0, padx=self.padx_widget, pady=self.pady_widget, sticky="W")
        entr_phone = ttk.Entry (self.add_customer_frame, textvariable=self.customer_phone)  
        entr_phone.grid(row=4, column=1, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        self.customer_email = tk.StringVar()
        lbl_email = ttk.Label(self.add_customer_frame, text="Email")  
        lbl_email.grid(row=5, column=0, padx=self.padx_widget, pady=self.pady_widget, sticky="W")
        entr_email = ttk.Entry (self.add_customer_frame, textvariable=self.customer_email)  
        entr_email.grid(row=5, column=1, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        # Buttons frame
        add_buttons_frame = ttk.Frame(self.add_customer_frame, width=self.column0_width, height=30)
        add_buttons_frame.grid(row=6, column=0, padx=self.padx_frame, pady=self.pady_frame, columnspan=2)        

        # Edit buttons
        bt_save = ttk.Button( add_buttons_frame, text="Save", command=lambda: self.add_customer_db(self.customer_first_name.get(), self.customer_last_name.get(), self.customer_phone.get(), self.customer_email.get()))
        bt_save.grid(row=0, column=0, sticky="E")

        bt_cancel = ttk.Button(add_buttons_frame, text="Cancel", command=self.hide_add_customer)
        bt_cancel.grid(row=0, column=1, sticky="E")
        ############################################
        # Add Customer END
        ############################################


    ############################################
    # Show Customer's Appointments START
    ############################################
    def show_customer_appointments_form(self, show=0):
        """
        Display customer's appointments
        """
        self.todays_date = datetime.today().strftime('%Y-%m-%d')
        if self.current_customer != -1:
            customer_id = int(self.tbl_customers.item(self.current_customer)['values'][0])
        else:
            # self.current_customer isn't valid. Return.
            return

        # Appointments Form
        self.appointments_frame = ttk.Frame(self, width=self.column0_width, height=250)
        self.appointments_frame.grid(row=1, column=1, padx=self.padx_frame, pady=self.pady_frame)

        # Display title
        lbl_search_title = ttk.Label(self.appointments_frame, text="Customer's Upcomming Apointments", font="Arial 14 bold", foreground="black")
        lbl_search_title.grid(row=0, column=0, columnspan=1, sticky="W")

        db = appDatabase()
        db.connect()
        self.lst_customer_appointments = db.get_customer_future_appointments(self.todays_date, customer_id)
        # print("Appointments from DB: ", self.lst_customer_appointments)
        db.close()

        # Create a scrollbar
        scrollbar = tk.Scrollbar(self.appointments_frame)
        scrollbar.grid(row=1, column=1, sticky='ns')

        txt_appointments = tk.Text(self.appointments_frame, height=10, width=30, yscrollcommand=scrollbar.set)  
        txt_appointments.grid(row=1, column=0, padx=self.padx_widget, pady=self.pady_widget, sticky="W")

        # Configure the scrollbar to scroll the Text widget
        scrollbar.config(command=txt_appointments.yview)

        # Define the font properties
        txt_appointments.tag_configure('bold', font=('Helvetica', 12, 'bold'))
        txt_appointments.tag_configure('normal', font=('Helvetica', 12))

        if isinstance(self.lst_customer_appointments, list):
            # query returned a list. Check if has items.
            if len(self.lst_customer_appointments) > 0:
                for a in self.lst_customer_appointments:
                    txt_appointments.insert('end', a[2].split('T')[0] + "\n", 'bold')
                    txt_appointments.insert('end', "From: " + a[2].split('T')[1] + " To: " + a[3].split('T')[1] + "\n", 'normal')
            else:
                txt_appointments.insert('end', "There are no appointments.", 'bold')

        # Buttons frame
        edit_buttons_frame = ttk.Frame(self.appointments_frame, width=self.column0_width, height=30)
        edit_buttons_frame.grid(row=2, column=0, padx=self.padx_frame, pady=self.pady_frame, columnspan=2)        

        # Edit buttons
        bt_save = ttk.Button( edit_buttons_frame, text="Send Email", command=lambda: self.send_email_customer_handler(customer_id))
        bt_save.grid(row=0, column=0, sticky="E")
        bt_save = ttk.Button( edit_buttons_frame, text="Export", command=lambda: self.print_customer_appointments_handler(customer_id))
        bt_save.grid(row=0, column=1, sticky="E")
        bt_cancel = ttk.Button(edit_buttons_frame, text="Close", command=self.hide_appointments_customer)
        bt_cancel.grid(row=0, column=2, sticky="E")

        ############################################
        # Show Customer's Appointments END
        ############################################



    def save_customer_db(self, customer_id):
        """
        Saves the customer updated info to the db.
        """
        if self.is_email(self.customer_email.get()) and self.is_number(self.customer_phone.get()):
            db = appDatabase()
            db.connect()
            db.update_customer(customer_id, self.customer_first_name.get(), self.customer_last_name.get(), self.customer_phone.get(), self.customer_email.get())
            db.close()
            messagebox.showinfo("Success, Customer's data have been updated.")
            self.unselect_customer()
            self.current_customer = -1
            try:
                if self.table_frame.winfo_viewable():
                    self.table_frame.grid_forget()
                    self.display_table(0)
            except Exception as e:
                print(e)            
        else:
            error_message = "Error!"
            if not self.is_email(self.customer_email.get()):
                error_message += "\nEntered Email, is not a valid email address."
            if not self.is_number(self.customer_phone.get()):
                error_message += "\nEntered phone is not a valid phone. It should contain only numbers."
            error_message += "\nPlease fix and try again."

            messagebox.showerror ("Error!", error_message)           


    def add_customer_db(self, fn, ln, phone, email):
        """
        Saves the customer updated info to the db.
        """
        if self.is_email(email) and self.is_number(phone) and fn != "" and ln != "":
            db = appDatabase()
            db.connect()
            db.add_customer(fn, ln, phone, email)
            db.close()
            messagebox.showinfo("Success", "You have added a new customer.")
            self.hide_add_customer()
            self.current_customer = -1
            try:
                if self.table_frame.winfo_viewable():
                    self.table_frame.grid_forget()
                    self.display_table(0)
            except Exception as e:
                print(e)            
        else:
            error_message = "Error!"
            if fn == "":
                error_message += "\nFirst Name entry is not valid."
            if ln == "":
                error_message += "\nLast Name entry is not valid."
            if not self.is_number(phone):
                error_message += "\nPhone entry is not valid. It should contain only numbers."
            if not self.is_email(email):
                error_message += "\nEmail entry is not a valid email address."
            error_message += "\nPlease fix and try again."

            messagebox.showerror ("Error!", error_message)           



    def is_number(self, test):
        """
        Checks if test variable is a number
        """
        if test.isdigit():
            return True
        else:
            return False        

    def is_email(self, test):
        """
        Checks if test contains a valid email address.
        It accepts as valid, email addresses that username contains + and _ characters.
        It is also accepts domain names like .co.uk.
        """
        # Regular expression pattern for an email address
        pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        if re.match(pattern, test):
            return True
        else:
            return False        

    def select_customer(self, event):
        """
       Select customer
        """
        self.current_customer = self.tbl_customers.focus()
        # # # Kostas # # #
        # TODO kostas
        # print(self.current_customer)
        # print(self.tbl_customers.item(self.current_customer))
        # print(event)

    def hide_edit_customer(self):
        try:
            # Hide the self.edit_customer_frame, if visible
            if self.edit_customer_frame.winfo_viewable():
                self.edit_customer_frame.grid_forget()
        except Exception as e:
            print(e)

    def hide_add_customer(self):
        try:
            # Hide the self.add_customer_frame, if visible
            if self.add_customer_frame.winfo_viewable():
                self.add_customer_frame.grid_forget()
        except Exception as e:
            print(e)

    def hide_appointments_customer(self):
        try:
            # Hide the self.appointments_frame, if visible
            if self.appointments_frame.winfo_viewable():
                self.appointments_frame.grid_forget()
        except Exception as e:
            print(e)


    def hide_add_customer(self):
        """
        Hide Add Customer Form
        """
        self.current_customer = -1
        selected_items = self.tbl_customers.selection() # get selected items
        for item in selected_items:
            self.tbl_customers.selection_remove(item)
        try:
            # Hide the self.add_customer_frame, if visible
            if self.add_customer_frame.winfo_viewable():
                self.add_customer_frame.grid_forget()
        except Exception as e:
            print(e)


    def unselect_customer(self):
        """
        Unselect customer from TreeView widget
        """
        self.current_customer = -1
        selected_items = self.tbl_customers.selection() # get selected items
        for item in selected_items:
            self.tbl_customers.selection_remove(item)
        try:
            # Hide the self.edit_customer_frame, if visible
            if self.edit_customer_frame.winfo_viewable():
                self.edit_customer_frame.grid_forget()
        except Exception as e:
            print(e)

    
    def edit_customer(self):
        """
        Edit selected customer
        """
        if self.current_customer == -1:
            messagebox.showerror ("Error!", "Please select a customer first.")
            return

        # Hide open forms
        try:
            # Hide the self.edit_customer_frame, if visible
            if self.edit_customer_frame.winfo_viewable():
                self.edit_customer_frame.grid_forget()
        except Exception as e:
            pass
        
        try:
            # Hide the self.add_customer_frame, if visible
            if self.add_customer_frame.winfo_viewable():
                self.add_customer_frame.grid_forget()
        except Exception as e:
            pass
        
        try:
            # Hide the self.appointments_frame, if visible
            if self.appointments_frame.winfo_viewable():
                self.appointments_frame.grid_forget()
        except Exception as e:
            pass

        self.edit_customer_form()

    
    def delete_customer(self):
        """
        Delete selected customer
        """
        if self.current_customer == -1:
            messagebox.showerror ("Error!", "Please select a customer first.")
            return
        # Get customer's ID from selected row in TreeView
        customer_id = self.tbl_customers.item(self.current_customer)['values'][0]
        # Check if customer has active appointments
        db = appDatabase()
        db.connect()
        count_appointments = db.find_appointments_count(customer_id)
        db.close()
        if count_appointments > 0:
            # Customer has active appointments
            response = messagebox.askquestion  ("Attention!", f"Customer with ID: {customer_id} has active appointments.\nThe count of active appointments is: {count_appointments}\nDo you want to proceed and delete customer?")
            if response == 'yes':
                db = appDatabase()
                db.connect()
                result = db.delete_appointments_customer(customer_id)
                db.close()
            if result == -1:
                messagebox.showinfo("Error", "Something went wrong while deleting appointments.")
                return
            db = appDatabase()
            db.connect()
            result = db.delete_customer(customer_id)
            db.close()
            if result == -1:
                messagebox.showinfo("Error", "Something went wrong while deleting customer.")
                return
        else:
            # Customer has NO active appointments
            response = messagebox.askquestion  ("Attention!", f"You are about to delete customer with ID: {customer_id}.\nDo you want to proceed with the deletion?")
            if response == 'yes':
                db = appDatabase()
                db.connect()
                result = db.delete_customer(customer_id)
                db.close()
                if result == -1:
                    messagebox.showinfo("Error", "Something went wrong while deleting customer.")
                    return
                self.display_table(0)



    def add_customer(self):
        """
        Add customer
        """
        # Hide open forms
        try:
            # Hide the self.edit_customer_frame, if visible
            if self.edit_customer_frame.winfo_viewable():
                self.edit_customer_frame.grid_forget()
        except Exception as e:
            pass
        
        try:
            # Hide the self.add_customer_frame, if visible
            if self.add_customer_frame.winfo_viewable():
                self.add_customer_frame.grid_forget()
        except Exception as e:
            pass
        
        try:
            # Hide the self.appointments_frame, if visible
            if self.appointments_frame.winfo_viewable():
                self.appointments_frame.grid_forget()
        except Exception as e:
            pass

        self.add_customer_form()


    def list_appointments_customer(self):
        """
        Send email to the selected customer
        """
        if self.current_customer == -1:
            messagebox.showerror ("Error!", "Please select a customer first.")
            return

        # Hide open forms
        try:
            # Hide the self.edit_customer_frame, if visible
            if self.edit_customer_frame.winfo_viewable():
                self.edit_customer_frame.grid_forget()
        except Exception as e:
            pass
        
        try:
            # Hide the self.add_customer_frame, if visible
            if self.add_customer_frame.winfo_viewable():
                self.add_customer_frame.grid_forget()
        except Exception as e:
            pass
        
        try:
            # Hide the self.appointments_frame, if visible
            if self.appointments_frame.winfo_viewable():
                self.appointments_frame.grid_forget()
        except Exception as e:
            pass

        self.show_customer_appointments_form()


    def search_customers(self):
        """
        Build the search form and display customers table (TreeView)
        """
        self.form_search_query()
        self.display_table(0)


    def number_of_records(self):
        """
        Returns number of customers based on current WHERE part of the query
        """
        db = appDatabase()
        db.connect()
        count = db.get_customers_count(self.query_parts)
        db.close()
        return count

    def form_search_query(self):
        """
        Reads the search form's fields and creates the WHERE part of the SQL query. Stores the WHERE part to self.query_parts[1]
        """
        if self.search_id == "" and self.search_first_name == "" and self.search_last_name == "" and self.search_phone == "" and self.search_email == "":
            # Return ALL customers
            self.query_parts[0] = "SELECT * FROM customers"
            self.query_parts[1] = "WHERE Deleted=0"
            # self.query_parts[2] = "ORDER BY CustomerID ASC"
            #query = "SELECT * FROM customers WHERE Deleted=0 ORDER BY CustomerID ASC"
            #return query
        else:
            self.query_parts[0] = "SELECT * FROM customers"
            where_criteria = "WHERE Deleted=0"
            where_criteria += " AND " + "CustomerID LIKE '%" + self.search_id.get() + "%'" + " "
            where_criteria += " AND " + "FirstName LIKE '%" + self.search_first_name.get() + "%'" + " "
            where_criteria += " AND " + "LastName LIKE '%" + self.search_last_name.get() + "%'" + " "
            where_criteria += " AND " + "Phone LIKE '%" + self.search_phone.get() + "%'" + " "
            where_criteria += " AND " + "Email LIKE '%" + self.search_email.get() + "%'" + " "
            self.query_parts[1] = where_criteria


    def clear_search_fields(self):
        """
        Clear the search form fields
        """
        self.search_id.set("")
        self.search_first_name.set("")
        self.search_last_name.set("")
        self.search_phone.set("")
        self.search_email.set("")

    def all_customers(self):
        """
        Show ALL customers
        """
        self.clear_search_fields()
        self.query_parts[1] = "WHERE Deleted=0"
        self.display_table(0)

    # # #  kostas  # # # 

    def send_email_customer_handler(self, customer_id):  
        """
        Function that handles email query db
        """
        time_now = datetime.now().strftime('%H:%M')
        db = appDatabase()
        db.connect()
        results = db.customer_appointments_data(self.todays_date, time_now, customer_id)
        db.close()
        # print("results", results) # TODO
        fetch_email(results)

    def print_customer_appointments_handler(self, customer_id):
        """
        Print customer's appointments
        """
        time_now = datetime.now().strftime('%H:%M')
        db = appDatabase()
        db.connect()
        results = db.customer_appointments_data(self.todays_date, time_now, customer_id)
        db.close()
        save_to_excel(results, self.todays_date)
        pass

# TODO
# def handle_db(fun, *args):
#     db = appDatabase()
#     db.connect()
#     result = db.fun(*args)
#     db.close()
#     return result

if __name__ == "__main__":
    pass


