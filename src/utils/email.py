# ############################ ############################
# Avgeros Kostas, 166187     
# avgerosk@gmail.com    
# Appointment Project 2023-2024 Hellenic Open University
# ############################ ############################
# https://www.geeksforgeeks.org/python-collections-module/
# https://www.geeksforgeeks.org/search-for-value-in-the-python-dictionary-with-multiple-values-for-a-key/ 
# append takes only one argument
# https://www.freecodecamp.org/news/python-list-to-string-how-to-convert-lists-in-python/ 
# ############################ ############################

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from .popup import show_popup
from collections import defaultdict


def fetch_email(data):

    '''Processes a list of appointment data supporting groupped by date'''
    if not data:
        message = "\tYour list is empty"
        print(message)
        show_popup(message)

    # Group appointments by email AND date
    appointments_by_customer = defaultdict(list)

    for row in data:
        email_q, slot_q, AppointmentID_q, firstname_q, lastname_q = row # This is a tupple!
        email_date_key = (email_q, datetime.strptime(slot_q, '%Y-%m-%dT%H:%M').date()) # Two key elements 
        # 1st create tupple,  2nd append to list, double parentheses to create a tuple SOS
        appointments_by_customer[email_date_key].append((slot_q, AppointmentID_q, firstname_q, lastname_q))

    # {('avgerosk1+pikos@gmail.com', datetime.date(2024, 6, 2)): 
        # [('2024-06-02T11:30', 55, 'Pikos', 'Apikos'), ('2024-06-02T12:30', 56, 'Pikos', 'Apikos')]})
    
    # Send an email for each group of appointments
    for (email, date), appointments in appointments_by_customer.items():
        appointments_cust_by_email = [] # initialize every loop
        for slot_q, AppointmentID_q, firstname_q, lastname_q in appointments:
            # Format the slot to a readable string
            formatted_slot = datetime.strptime(slot_q, '%Y-%m-%dT%H:%M').strftime('%B %d, %Y at %I:%M %p')
            # Append the formatted details to a new list
            appointments_cust_by_email.append((formatted_slot, AppointmentID_q, firstname_q, lastname_q))
        # Send email with the formatted appointments
        send_email(email, appointments_cust_by_email) # every loop
      

def send_email(email, appointments):
    ''' Sends a (confirmation) email with params as text or html'''

    # Email credentials
    sender_email = "avgerosk@gmail.com"
    sender_password = "kyes mryc ypib raoo"
    project_team = "Project Python Team"
    team_name_1 = "Antonopoulos Ilias"
    team_name_2 = "Avgeros Kostas"

    # Recipient email
    recipient_email = [email] # as list

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Appointment Confirmation"
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_email) 

    # print(appointments)
    # [('June 02, 2024 at 11:30 AM', 55, 'Pikos', 'Apikos'), ('June 02, 2024 at 12:30 PM', 56, 'Pikos', 'Apikos')]
    fname = appointments[0][2]
    lname = appointments[0][3]
    date = appointments[0][0].split(' at ')[0]

    # Create the msg plain text
    generator_expr = (f"\nAppointment Slot: {slot}\nAppointment ID: {appointment_id}\nName: {firstname} {lastname}"
        for slot, appointment_id, firstname, lastname in appointments)
    separator = '\n'
    appointment_details_plainText = separator.join(generator_expr)

    # Create the msg html
    generator_expr = (f"<li><strong>Appointment Slot:</strong> {slot}<br><strong>Appointment ID:</strong> \
                      {appointment_id}<br><strong>Name:</strong> {firstname} {lastname}</li>"
        for slot, appointment_id, firstname, lastname in appointments)
    separator = ' '
    appointment_details_html = separator.join(generator_expr)

    # Create the body of the message (a plain-text and an HTML version).
    text = f"""
        Dear {fname},

        I am writing to confirm your appointment scheduled for {date}. Below are the details of your appointment:

        {appointment_details_plainText}

        Please let me know if you need any additional information or if there are any changes to the scheduled time.

        Thank you.

        Best regards,
        {team_name_1}
        {team_name_2}
        {project_team}
        """

    html = f"""\
        <html>
        <head></head>
        <body>
            <p>Dear {fname},</p>
            <p>I am writing to confirm your appointment scheduled for <strong>{date}</strong>. Below are the details of your appointment:</p>
            <ul>
            {appointment_details_html}
            </ul>
            <p>Please let me know if you need any additional information or if there are any changes to the scheduled time.</p>
            <p>Thank you.</p>
            <p>Best regards,<br>{team_name_1}
            <br>{team_name_2}
            <br>{project_team}</p>
        </body>
        </html>
        """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container
    # The last one is that to be sent SOS
    msg.attach(part1)
    msg.attach(part2)
    
    # Send the message via SMTP server.
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(sender_email, sender_password)
        smtp_server.sendmail(sender_email, recipient_email, msg.as_string())
        smtp_server.close()
        message = f"\tEmail to {recipient_email} sent successfully!"
        print(message)
        show_popup(message)
    except Exception as e:
        print(e)
        show_popup(e)



