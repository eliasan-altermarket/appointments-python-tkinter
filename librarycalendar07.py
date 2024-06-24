"""
Author: Ilias Antonopoulos
eliasan@altermarket.com
www.altermarket.com, www.kalliergo.gr
Appointments Project, 2023-2024 Hellenic Open University

Defines the following classes:
* Appointment
* TimeSlot
* Day
* Month
Month contains Day objects. One for each day that belongs to the month
These Day objects are grouped into weeks. 5 (0-4) weeks for each month.
Each Day object contains the Timeslots for that day.
Day object queries the database.
If a Timeslot contains an Appointment, it is associated with it.
"""

from datetime import datetime, timedelta, date
# import random, just for creating random inclussions or exclusions of Appointment objects
import random
from database import appDatabase
import calendar
from itertools import zip_longest

class Appointment:
    """
    Define class Appointment
    == THESE values are as those stored in the database ==
    start_time: Stores the start time (string in the format YYYY-MM-DDTHH:MM)
    end_time: Stores the end time (string in the format YYYY-MM-DDTHH:MM)
    appointment_id: The appointment's ID (int)
    deleted: Is the appointment is deleted or not (int, 0, 1)
    customer_id: The ID of the customer that booked the appointment (int)
    customer_fn: The First Name of the customer (string)
    customer_ln: The Last Name of the customer (string)
    During initialization, sets these values
    """
    def __init__(self, start_time, end_time, appointment_id, deleted, customer_id, customer_fn, customer_ln):
        self.start_time = start_time
        self.end_time = end_time
        self.appointment_id = appointment_id
        self.deleted = deleted
        self.customer_id = customer_id
        self.customer_fn = customer_fn
        self.customer_ln = customer_ln

    def __str__(self):
        return f"Appointment {self.appointment_id} from {self.start_time} to {self.end_time}. Deleted = {self.deleted}. For Customer '{self.customer_fn} {self.customer_ln}' with CustomerID = {str(self.customer_id)}"

class TimeSlot:
    """
    Define class TimeSlot
    start_time: Stores the start time (datetime object)
    appointment: An appointment object, if exists. Otherwise set to None.
    end_time: Stores the end time (interval of 30 minutes) (datetime object)
    During initialization, sets these values
    """
    def __init__(self, start_time, appointment):
        self.start_time = start_time
        self.appointment = appointment
        self.end_time = start_time + timedelta(minutes=30)

    def get_str_starttime(self):
        """Return as a string the start time (Hours:Minutes)"""
        return self.start_time.strftime('%H:%M')

    def get_str_endtime(self):
        """Return as a string the end time (Hours:Minutes)"""
        return self.end_time.strftime('%H:%M')

    def get_db_startdate(self):
        """Return as a string the Start Date in database format"""
        return self.start_time.strftime('%Y-%m-%dT%H:%M')

    def get_appointment(self):
        """Return the appointment object"""
        return self.appointment

    def get_db_enddate(self):
        """Return as a string the End Date in database format"""
        return self.end_time.strftime('%Y-%m-%dT%H:%M')

    def __str__(self):
        """#return f"Timeslot from {self.start_time.strftime('%Y-%m-%dT%H:%M')} to {self.end_time.strftime('%H:%M')}. Appointment = {self.appointment}."""
        return f"{self.start_time.strftime('%Y-%m-%dT%H:%M')}-{self.end_time.strftime('%H:%M')}. Appointment = {self.appointment}."

class Day:
    """
    Define class Day
    date: A date (it is an input)
    timeslots: A list of possible timeslots
    """
    #global db
    def __init__(self, date):
        self.date = date
        # Query the database for appointments for this day
        db = appDatabase()
        db.connect()
        # self.lst_appointments list contains tuples with records from db
        # records are appointment data for that particular day
        self.query_date = self.date.strftime('%Y-%m-%d')
        self.lst_appointments = db.get_days_appointments(self.query_date)
        # print("Appointments from DB: ", self.lst_appointments)
        db.close()
        self.timeslots = self.create_timeslots(self.date)

    def search_for_appointment(self, lst_app, timeslot_datetime):
        """
        Search the list for a tuple that contains in the first position, the datetime of the current time slot.
        If you find such a tuple, return it.
        If the list is empty, or it doesn't contain such a tuple, return none.
        lst_app: The list that contains tuples (appointments)
        timeslot_datetime: A string of the form: '2024-04-12T11:00'
        """
        if not lst_app:
            return None
        for tup in lst_app:
            if tup[0] == timeslot_datetime:
                return tup
        return None        
    
    def create_timeslots(self, date):
        timeslots = []
        #start_time = datetime.strptime('08:00' , '%H:%M')
        start_time = datetime.strptime(date.strftime('%Y-%m-%d') + ' ' + '09:00' , '%Y-%m-%d %H:%M')
        # end_time = datetime.strptime('22:00', '%H:%M')
        end_time = datetime.strptime(date.strftime('%Y-%m-%d') + ' ' + '20:30' , '%Y-%m-%d %H:%M')
        interval = timedelta(minutes=30)
        current_time = start_time
        while current_time <= end_time:
            # I will search the list self.lst_appointments, if it contains a tuple that
            # is actually an appointment, for this time slot.
            # If it has, I will use tuple's data to for an appointment object 
            # and add it to the time slot object
            # Add here code to query the database and give value to appointment object

            # Form the string that contains date + time separated by 'T'
            datetime_str = date.strftime('%Y-%m-%d') + 'T' + current_time.strftime('%H:%M')
            tup_appointment = self.search_for_appointment(self.lst_appointments, datetime_str)
            if tup_appointment:
                # Unpack tuple
                start_dt, end_dt, app_id, app_deleted, app_customer_id, app_customer_fn, app_customer_ln = tup_appointment
                if int(app_deleted) == 0:
                    self.appointment = Appointment(start_dt, end_dt, app_id, app_deleted, app_customer_id, app_customer_fn, app_customer_ln)
                else:
                    self.appointment = None
            else:
                self.appointment = None

            timeslots.append(TimeSlot(current_time, self.appointment))
            current_time += interval
        return timeslots

    def get_weekday_name(self):
        return self.date.strftime('%A')

    def get_weekday_date(self):
        return self.date.strftime('%d-%m-%Y')

    def __str__(self):
        return "\n".join(str(timeslot) for timeslot in self.timeslots)


class Month():
    """
    Finds the days in a month.
    Splits these days into 7-day weeks, forming a list of 5 weeks.
    For each day, creates a Day object and stores it to the day.
    Each Day object has info about the time slots and the appointments
    """
    def __init__(self, date):
        self.date = date
        # Create a calendar object with first day=0 (Monday)
        self.mcal = calendar.Calendar(firstweekday=0)
        # Get the dates of this month (YYYY, MM) and create a list
        self.month_dates = list( self.mcal.itermonthdates( int( self.date.strftime('%Y') ), int( self.date.strftime('%m') ) ) )
        # Now group days into weeks
        # How it works??
        self.month_weeks = list(zip_longest(*[iter(self.month_dates)]*7))
        self.weeks = []
        for self.month_week in self.month_weeks:
            self.week = []
            for self.month_d in self.month_week:
                self.week.append(Day(self.month_d))
                # date_string = self.month_d.strftime("%Y:%m:%d")
                # print(date_string)
            self.weeks.append(self.week)
        self.current_week_index = self.get_week_index_for_day(self.date)

    def print_weeks(self):
        count = 1
        for week in self.weeks:
            print(f"===== WEEK {count} =====")
            for d in week:
                print(d)
            count+=1

    def get_week_index_for_day(self, target_date):
        """
        Return the index of the week list a day is in
        """
        for i, week in enumerate(self.weeks):
            if any(day.date.strftime("%Y:%m:%d") == target_date.strftime("%Y:%m:%d") for day in week):
                return i

    def get_day(self, target_date):
        """
        Return the Day object of a day
        """
        for week in self.weeks:
            if any(day.date.strftime("%Y:%m:%d") == target_date.strftime("%Y:%m:%d") for day in week):
                return day

    def get_week_days(self, week_index):
        """
        Return a list that contains the days (Day objects) of a week based on an index
        """
        if week_index >=0 and week_index <=4:
            return self.weeks[week_index]
        return none
    
    def get_todays_week_days(self):
        """
        Returns a list with the Day objects that belong to current date.
        """
        week_index = self.get_week_index_for_day(self.date)
        return self.get_week_days(week_index)

    def get_next_week(self):
        """
        Increases the index by 1 and
        returns a list with the Day objects that belong to that week.
        """
        if self.current_week_index < 4:
            self.current_week_index += 1
        return self.get_week_days(self.current_week_index)

    def get_previous_week(self):
        """
        Decreases the index by 1 and
        returns a list with the Day objects that belong to that week.
        """
        if self.current_week_index > 0:
            self.current_week_index -= 1
        return self.get_week_days(self.current_week_index)

if __name__ == '__main__':

    m = Month(datetime.today())
    
    # TESTINGS
    """
    # Create a Day object for today
    day = Day(datetime.today())
    print("**** DAY Today **********************")
    # Print the timeslots for the day
    print(day)

    test_date = date(2024,4,29)
    # Create a Day object for 2024.04.13
    day = Day(test_date)
    print("**** DAY 2024.04.15 **********************")
    # Print the timeslots for the day
    print(day)
    """
    
    """
    # TESTS
    print("***** PRINT WEEK INDEX A DAY IS IN *****")
    print( m.get_week_index_for_day( test_date ) )

    print("***** PRINT DAY FROM MONTH *****")
    print( m.get_day( test_date ) )

    print("***** PRINT DAYS FROM THE WEEK TODAY BELONGS *****")
    print(m.get_todays_week_days())

    print("***** PRINT DAYS FROM THE PREVIOUS WEEK *****")
    print(m.get_previous_week())

    print("***** PRINT DAYS FROM THE NEXT WEEK *****")
    print(m.get_next_week())

    print("***** PRINT DAYS FROM THE NEXT WEEK *****")
    print(m.get_next_week())

    print("***** PRINT DAYS FROM THE NEXT WEEK *****")
    print(m.get_next_week())
    """