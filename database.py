"""
Author: Ilias Antonopoulos
eliasan@altermarket.com
www.altermarket.com, www.kalliergo.gr
Appointments Project, 2023-2024 Hellenic Open University

This class, talks to the database. Returns, Updates, Deletes records.
"""

import sqlite3
import os.path

class appDatabase:
    def __init__(self):
        """
        Initialize the database connection.
        """
        # The name of the db file. Must be located the same directory as the application.
        self.database_file = 'appdb01.db'
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, self.database_file)
        self.db_name = db_path
        #self.connection = None

    def connect(self):
        """
        Establish a connection to the SQLite database.
        """
        try:
            self.connection = sqlite3.connect(self.db_name)
            # print(f"Connected to {self.db_name}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def create_table(self, table_name, sqlcommand):
        """
        Create a new table in the database.
        :param table_name: Name of the table.
        """
        try:
            cur = self.connection.cursor()
            cur.execute(sqlcommand)
            self.connection.commit()
            print(f"Table '{table_name}' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_data(self, table_name, data):
        """
        Insert data into the specified table.
        :param table_name: Name of the table.
        :param data: Tuple or list of values to insert (e.g., ("The Matrix", 1999, 8.7))
        """
        try:
            cur = self.connection.cursor()
            placeholders = ", ".join("?" for _ in data)
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
            cur.execute(insert_query, data)
            self.connection.commit()
            # print("Data inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def add_appointment(self, appointment):
        """
        Add appointment into the appointments table.
        :param appointment: Tuple or list of values to insert (e.g., ("The Matrix", 1999, 8.7))
        Returns 1 on success and 0 on failure
        """
        try:
            cur = self.connection.cursor()
            placeholders = ", ".join("?" for _ in appointment)
            insert_query = f"INSERT INTO appointments (CustomerID, Start, End, Deleted) VALUES ({placeholders})"
            cur.execute(insert_query, appointment)
            self.connection.commit()
            # print("Appointment added successfully.")
            # Return the Appointment ID (The Id of the last row inserted)
            return cur.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding appointment: {e}")
            return None



    def get_days_appointments(self, day):
        """
        Retrieve all appointments for the specified day.
        :param day: Day string in the form "YYYY-MM-DD".
        """
        try:
            cur = self.connection.cursor()

            query = "SELECT a.Start, a.End, a.AppointmentID, a.Deleted, a.CustomerID, c.FirstName, c.LastName FROM appointments a INNER JOIN customers c ON a.CustomerID = c.CustomerID WHERE a.Start LIKE ?"  

            # Use this method to prevent SQL injections
            appointments_list = cur.execute(query, ('%'+day+'%',)).fetchall()
            # appointments_list contains [(), (), ... ()]

            return appointments_list
        
        except sqlite3.Error as e:
            print(f"Error querying data: {e}")        


    def get_customer_future_appointments(self, day, customer_id):
        """
        Retrieve all appointments for a customer that are scheduled from today and in the future.
        :param day: Day string in the form "YYYY-MM-DD".
        """
        try:
            cur = self.connection.cursor()

            query = "SELECT * FROM appointments WHERE SUBSTR(Start, 1, 10) >= '" +day+ "' AND CustomerID = "+str(customer_id)+" AND Deleted = 0 ORDER BY Start"  

            appointments_list = cur.execute(query).fetchall()
            # appointments_list contains [(), (), ... ()]

            return appointments_list
        
        except sqlite3.Error as e:
            print(f"Error querying data: {e}")        


    def get_customers_count(self, query_parts):
        """
        Get the number of records in customers table.
        """
        try:
            cur = self.connection.cursor()
            # When you use count in SQL, it doesn't make sense
            # to use LIMIT and ORDER BY, as count returns only 1 row.
            query = "SELECT count(*) as no_customers from customers " + query_parts[1]

            cur.execute(query)
            data_row = cur.fetchone()
            customers_count = data_row[0] # Total number of rows in table customers
            return customers_count
        
        except sqlite3.Error as e:
            print(f"Error getting number of records from customers table: {e}")
            return -1

    #def get_customers_with_limit(self, query_parts, offset, limit):
    def get_customers_with_limit(self, query_parts, offset):
        """
        Get a limited number of customers from customers table.
        """
        try:
            cur = self.connection.cursor()
            query = query_parts[0] + " " + query_parts[1] + " " + query_parts[2] + " LIMIT " + str(offset) + ", " + str(query_parts[3])
            cur.execute(query)
            records = cur.fetchall()
            return records
        
        except sqlite3.Error as e:
            print(f"Error getting a limited number of customers from customers table: {e}")
            return -1


    def query_data(self, table_name):
        """
        Retrieve all data from the specified table.
        :param table_name: Name of the table.
        """
        try:
            cur = self.connection.cursor()
            cur.execute(f"SELECT * FROM {table_name}")
            rows = cur.fetchall()
            #for row in rows:
            #    print(row)
        except sqlite3.Error as e:
            print(f"Error querying data: {e}")

    def all_customers_dict(self):
        """
        Return all customers as a dictionary
        """
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT CustomerID, FirstName, LastName, Phone, Email, Deleted FROM customers WHERE Deleted=0 ORDER BY LastName ASC")
            rows = cur.fetchall()

            # Create a dictionary with 'FirstName+LastName' as key and 'CustomerID' as value
            customers_dict = {row[2] + " " + row[1]: row[0] for row in rows}
        except sqlite3.Error as e:
            print(f"Error getting all customers: {e}")
        
        print (customers_dict)
        return customers_dict

    def get_customer_data(self, customer_id):
        """
        Return a customer's data based on his id
        """
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT CustomerID, FirstName, LastName, Phone, Email, Deleted FROM customers WHERE CustomerID=" + str(customer_id))
            row = cur.fetchone()
            if row is not None:
                return tuple(row) # Return result as a tuple
            return None
        except sqlite3.Error as e:
            print(f"Error getting customer data: {e}")
            return None

    def delete_appointment(self, app_id):
        """
        Delete an appointment based on its id
        It doesn't actually deletes the record.
        It only changes its Deleted field value from 0 to 1.
        """
        try:
            cur = self.connection.cursor()
            #cur.execute("DELETE FROM appointments WHERE AppointmentID=" + str(app_id))
            cur.execute("UPDATE appointments SET Deleted=? WHERE AppointmentID=?", (1, app_id))
            self.connection.commit()
            return 0
        except sqlite3.Error as e:
            print(f"Error deleting appointment: {e}")
            return -1

    def update_customer(self, id, fn, ln, phone, email):
        """
        Update a customer's record
        """
        try:
            cur = self.connection.cursor()
            cur.execute("UPDATE customers SET FirstName=?, LastName=?, Phone=?, Email=? WHERE CustomerID=?", (fn, ln, phone, email, id))
            self.connection.commit()
            return 0
        except sqlite3.Error as e:
            print(f"Error updating customer: {e}")
            return -1

    def add_customer(self, fn, ln, phone, email):
        """
        Add a new customer
        """
        try:
            cur = self.connection.cursor()
            cur.execute("INSERT INTO customers (FirstName, LastName, Phone, Email, Deleted) VALUES(?, ?, ?, ?, 0)", (fn, ln, phone, email))
            self.connection.commit()
            return 0
        except sqlite3.Error as e:
            print(f"Error adding new customer: {e}")
            return -1

    def find_appointments_count(self, customer_id):
        """
        Get the number of appointments for a given customer.
        """
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT count(*) AS count_appointments FROM appointments WHERE CustomerID = ? AND Deleted=0", (customer_id,))
            data_row = cur.fetchone()
            appointments_count = data_row[0] # Total number of rows in table appointments
            return appointments_count
        
        except sqlite3.Error as e:
            print(f"Error getting number of appointments from appointments table: {e}")
            return -1

    def delete_appointments_customer(self, customer_id):
        """
        Delete all apointments that belong to a customer.
        """
        try:
            cur = self.connection.cursor()
            cur.execute("UPDATE appointments SET Deleted = 1 WHERE CustomerID = ?", (customer_id,))
            self.connection.commit()
            return 0
        except sqlite3.Error as e:
            print(f"Error deleting appointments for customer: {e}")
            return -1

    def delete_customer(self, customer_id):
        """
        Delete a customer.
        """
        try:
            cur = self.connection.cursor()
            cur.execute("UPDATE customers SET Deleted = 1 WHERE CustomerID = ?", (customer_id,))
            self.connection.commit()
            return 0
        except sqlite3.Error as e:
            print(f"Error deleting a customer: {e}")
            return -1


    def close(self):
        """
        Close the database connection.
        """
        if self.connection:
            self.connection.close()
            #print(f"Connection to {self.db_name} closed.")

    # # # # # # # #   Kostas  # # # # # # # # 
            
    def query_email(self, today, time_now, date):
        '''
        Executes query mail
        '''
        query = f'''SELECT customers.Email, appointments.Start, 
                        appointments.AppointmentID, customers.FirstName, customers.LastName
                        FROM appointments JOIN customers 
                        WHERE customers.CustomerID = appointments.CustomerID
                        AND appointments.Start LIKE '{date}%' 
                        AND appointments.Start >= '{today}T{time_now}'
                        AND appointments.Deleted = 0
                        ORDER BY appointments.Start ASC'''
        try:
            cur = self.connection.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Error fetch query data: {e}")
            return -1
        
    def query_excel(self, start_date):
        '''
        Executes query and saves result with styles in user defined path
        '''
        query = f'''SELECT customers.Email, appointments.Start, 
                    appointments.AppointmentID, customers.Firstname, customers.LastName
                    FROM appointments JOIN customers 
                    WHERE customers.CustomerID = appointments.CustomerID
                    AND appointments.Start LIKE '{start_date}%'
                    AND appointments.Deleted = 0
                    ORDER BY appointments.Start ASC'''
        try:
            cur = self.connection.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Error fetch query data: {e}")
            return -1
        
    def query_preview(self, date):
        '''
        Executes query and shows result in a popup window
        '''
        query = f'''SELECT customers.Email, appointments.Start, 
            appointments.AppointmentID, customers.Firstname, customers.LastName
            FROM appointments JOIN customers 
            WHERE customers.CustomerID = appointments.CustomerID
            AND appointments.Start LIKE '{date}%'
            AND appointments.Deleted = 0
            ORDER BY appointments.Start ASC'''
        try:
            cur = self.connection.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            if not rows: rows = 'No data to display!' # (('No data to display!'),) # tupple
            return rows
        except sqlite3.Error as e:
            print(f"Error fetch query data: {e}")
            return -1

    def customer_appointments_data(self, start_date, time, customer_id):
        '''
        Executes query and shows result in a popup window
        '''
        query = f'''SELECT customers.Email, appointments.Start, 
                    appointments.AppointmentID, customers.Firstname, customers.LastName
                    FROM appointments JOIN customers 
                    WHERE customers.CustomerID = appointments.CustomerID
                    AND appointments.Start >= '{start_date}T{time}'
                    AND customers.CustomerID = '{customer_id}'
                    AND appointments.Deleted = 0
                    ORDER BY appointments.Start ASC'''
        try:
            cur = self.connection.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Error fetch query data: {e}")
            return -1

        
