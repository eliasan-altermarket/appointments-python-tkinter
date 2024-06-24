# ############################ ############################
# Avgeros Kostas, 166187     
# avgerosk@gmail.com    
# Appointment Project 2023-2024 Hellenic Open University
# ############################ ############################
# 
# ############################ ############################

import os
from datetime import datetime
from src.models.process_excel import ModuleExcel


def save_to_excel(data, date):    # 2nd step
    '''
    Fucntion using model 'create_excel' to save the excel file
    '''
    handler = ModuleExcel(date)
    file_path = handler.path_to_save()

    if not file_path:
        print("Save operation cancelled.")
        return
    
    if os.path.exists(file_path):
        handler.del_previous_data(file_path) # During the same date
    else:
        handler.add_heading()
        handler.set_header_dimensions()
        handler.add_styles()
    handler.save(file_path)

    if not data: # TODO -> print messagebox ?
        print("\tYour list is empty")
        return

    try: 
        for row in data:
            email_q, slot_q, AppointmentID_q, firstname_q, lastname_q= row
            # Convert the slot_q, parse -> format
            slot_q = datetime.strptime(slot_q, '%Y-%m-%dT%H:%M').strftime('%B %d, %Y at %I:%M %p')
            handler.add_data(email_q, slot_q, AppointmentID_q, firstname_q, lastname_q)
            
        handler.set_dimensions(slot_q, AppointmentID_q, firstname_q, lastname_q) # without email_q
        handler.add_styles()
        handler.save(file_path) 
    except UnboundLocalError as e:
        print("Cancel button pressed")
    except Exception as e:
        print("An error occured: ", e)