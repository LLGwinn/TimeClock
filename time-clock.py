#####################################################################################
#  TIME CLOCK APPLICATION                                                           #
#                                                                                   #
#  In the absence of a database, we store data in a json data file.                 #
#  Each employee 'record' is an instance of the Employee class.                     #
#  Each shift 'record' is an instance of the Shift class. This program assumes      #
#  one shift per day.                                                               #
#                                                                                   #
#  Since an employee can technically have multiple breaks and lunches during one    #
#  shift, we have classes for those elements, and the instances are kept in         #
#  lists in the Shift class.                                                        #
#                                                                                   #                                                              # 
#####################################################################################

import datetime
import json

class Employee:
    def __init__(self, emp_id, first_name, last_name):
        self.id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = False;
        self.shift_active = False;
        self.at_lunch = False;
        self.on_break = False;


class Shift:
    def __init__(self, emp_id, date, shift_start=None):
        self.emp_id = emp_id
        self.date = date
        self.shift_start = shift_start
        self.shift_end = None
        self.breaks = []
        self.lunches = []

class Lunch:
    def __init__(self, start=None, end=None):
        self.lunch_start = start
        self.lunch_end = end

class Break:
    def __init__(self, start=None, end=None):
        self.break_start = start
        self.break_end = end

# Lists to simulate database tables for employees and recorded shifts
employees = []
shifts = []

# Keep track of current employee
current_employee = None

def get_employee_data():
    """ Look for time_clock_data.json file and loads its data into 'employees' list and 'shifts' list.
        If no data file exists (first program run), create file and populate with mock data,
        then add data to 'employees' list and 'shifts' list.
    """
    with open("time_clock_data.json", "a+") as data_file:
        data_file.seek(0)
        if data_file.read() == "":
            # create two mock employees
            emp1 = Employee('12345', 'John', 'Doe').__dict__
            emp2 = Employee('23456', 'Jane', 'Doe').__dict__
            emp3 = Employee('99999', 'Admin', 'Person').__dict__
            emp3['is_admin'] = True
            # create some date/time objects for shifts
            datetime1 = datetime.datetime(2022, 8, 10, 8, 0, 0)
            datetime2 = datetime.datetime(2022, 8, 11, 8, 0, 0)
            datetime3 = datetime.datetime(2022, 8, 12, 8, 0, 0)
            # create some mock shifts
            shift1 = Shift('12345', datetime1.strftime("%x"), datetime1.strftime("%X")).__dict__
            shift2 = Shift('12345', datetime2.strftime("%x"), datetime1.strftime("%X")).__dict__
            shift3 = Shift('23456', datetime3.strftime("%x"), datetime1.strftime("%X")).__dict__
            # format data
            mock_data = {'employees': [emp1, emp2, emp3],
                         'shifts': [shift1, shift2, shift3]}
            # add data to time_clock_data.json file
            json.dump(mock_data, data_file, indent=4)
            data_file.seek(0)
            # append the mock data to 'employees' list and 'shifts' list
            employees.append(emp1)
            employees.append(emp2)
            employees.append(emp3)
            shifts.append(shift1)
            shifts.append(shift2)
            shifts.append(shift3)
        else:
            data_file.seek(0)
            imported_data = json.loads(data_file.read())
            for employee in imported_data['employees']:
                employees.append(employee)
            for shift in imported_data['shifts']:
                shifts.append(shift)

def update_data_file():
    """ When a change is made to employee or shift status, write a new data file"""

    data_to_export = {'employees': employees, 'shifts': shifts}

    # Write updated data to data file
    with open("time_clock_data.json", "w") as data_file:
        json.dump(data_to_export, data_file, indent=4)

def show_start_menu():
    """ Prompts user to sign in, register as new user, or quit the program. """
    
    print('Please choose from the following options:\n')
    print('PRESS 1 to sign in\nPRESS 2 to register as a new user\nPRESS 0 to quit the Time Clock program\n')
    option = input()

    if option == '1':    
        emp_id = input('\nPlease enter Employee ID: ')
        if validate_emp_id(emp_id) == False:
            show_start_menu()
        else:
            global current_employee
            current_employee = [employee for employee in employees if emp_id == employee['id']][0]
            print('\nWelcome back,', current_employee['first_name'])
            show_main_menu()

    elif option == '2':
        current_employee = register()
        if current_employee == None:
            print('\nERROR: Some of your input was blank. Try again.\n')
            show_start_menu()
        else:
            print('\nWelcome to the team,', current_employee['first_name'], current_employee['last_name'] + '!\n')
            show_main_menu()

    elif option == '0':
        print('\nExiting the Time Clock program. Goodbye!\n')
        quit()
    else:
        print('\n*** INVALID ENTRY ***\n')
        show_start_menu()

def validate_emp_id(emp_id):
    """ Check user input against the employees list for valid employee id.
        If valid employee id, return True.
        If invalid employee id, display error message and return False.
    """

    if emp_id != '':
        global current_employee
        current_employee_list = [employee for employee in employees if employee['id'] == emp_id]
        if len(current_employee_list) < 1:
            print('\n*** Employee ID not valid. ***\n')
            return False
        else:
            return True
    else:
        print('\n*** Employee ID not valid. ***\n')
        return False

def show_main_menu():
    """ Display options for various clock punches based on current shift, break, and lunch status. """
    
    print('Please select an option:\n')
    if current_employee['shift_active'] == False:
        # If there is already a shift for this day, prompt them to sign out
        this_day_shifts = [shift for shift in shifts if shift['emp_id'] == current_employee['id'] and
            shift['date'] == datetime.datetime.now().strftime("%x")]
        if len(this_day_shifts) > 0:
            print('\nYou have completed your shift for the day. Thank you!\n')
        else:
            print('\nPRESS 1 to start a shift')
    elif current_employee['on_break'] == True:
        print('PRESS 2 to end your break')
    elif current_employee['at_lunch'] == True:
        print('PRESS 3 to end your lunch')
    else:
        print('PRESS 4 to start your break')
        print('PRESS 5 to start your lunch')
        print('PRESS 6 to end your shift')

    if current_employee['is_admin'] == True:
        print('PRESS 8 for the Administrator menu')
    print('PRESS 9 to sign out\n')

    option = input()
    process_main_menu_input(option)

def show_admin_menu():
    """ Display options to allow administrators to perform any function. """

    if current_employee['is_admin'] == False:
        print('Unauthorized to access this menu.')
        show_main_menu()
    else:
        print('Please select an option:')
        print('\nPRESS 1 adjust an employee time record')
        print('PRESS 2 to display a shift report')
        print('PRESS 3 to update employee profile')
        print('PRESS 4 to go back to the main menu\n')

    option = input()
    process_admin_task(option)

def start_shift(emp, date, time):
    # Make sure there isn't already a shift for this date
    all_emp_shifts = [shift for shift in shifts if shift['emp_id'] == emp['id'] and shift['date'] == date]
    if len(all_emp_shifts) > 0:
        print('\nThere is already a shift for this employee on this date.\n')
    else:
        new_shift = Shift(emp['id'], date, time).__dict__
        shifts.append(new_shift)
        emp['shift_active'] = True
        update_data_file()
        print ('\nSHIFT STARTED:', emp['first_name'], emp['last_name'], '--', new_shift['date'], new_shift['shift_start'],'\n')

def end_shift(emp, date, time):
    shift_to_end = [shift for shift in shifts if shift['date'] == date and shift['emp_id'] == emp['id']][0]
    if shift_to_end['shift_end'] == None:
        shift_to_end['shift_end'] = time
        emp['shift_active'] = False
        update_data_file()
        print ('\nSHIFT ENDED:', emp['first_name'], emp['last_name'], '--', shift_to_end['date'], shift_to_end['shift_end'],'\n')
    else:
        print('\n This shift was already ended on', shift_to_end['date'], 'at', shift_to_end['shift_end'], '.\n')
    
def start_break(emp, date, time):
    emp_shifts = [shift for shift in shifts if shift['emp_id'] == emp['id'] and shift['date'] == date]
    if len(emp_shifts) > 0:
        shift = emp_shifts[0]
        new_break = Break(time).__dict__
        shift['breaks'].append(new_break)
        emp['on_break'] = True
        update_data_file()
        print ('\nBREAK STARTED:', emp['first_name'], emp['last_name'], '--', shift['date'], new_break['break_start'],'\n')

def end_break(emp, date, time):
    emp_shifts = [shift for shift in shifts if shift['emp_id'] == emp['id'] and shift['date'] == date]
    if len(emp_shifts) > 0:
        shift = emp_shifts[0]
        for brk in shift['breaks']:
            if brk['break_start'] != None and brk['break_end'] == None:
                brk['break_end'] = time
                emp['on_break'] = False
                update_data_file()
                print ('\nBREAK ENDED:', emp['first_name'], emp['last_name'], '--', shift['date'], brk['break_end'],'\n')
            else:
                print('\nThere is no active break for this shift.')

def start_lunch(emp, date, time):
    emp_shifts = [shift for shift in shifts if shift['emp_id'] == emp['id'] and shift['date'] == date]
    if len(emp_shifts) > 0:
        shift = emp_shifts[0]
        new_lunch = Lunch(time).__dict__
        shift['lunches'].append(new_lunch)
        emp['at_lunch'] = True
        update_data_file()
        print ('\nLUNCH STARTED:', emp['first_name'], emp['last_name'], '--', shift['date'], new_lunch['lunch_start'],'\n')

def end_lunch(emp, date, time):
    emp_shifts = [shift for shift in shifts if shift['emp_id'] == emp['id'] and shift['date'] == date]
    if len(emp_shifts) > 0:
        shift = emp_shifts[0]
        for lunch in shift['lunches']:
            if lunch['lunch_start'] != None and lunch['lunch_end'] == None:
                lunch['lunch_end'] = time
                emp['at_lunch'] = False
                update_data_file()
                print ('\nLUNCH ENDED:', emp['first_name'], emp['last_name'], '--', shift['date'], lunch['lunch_end'],'\n')
            else:
                print('\nThere is no active lunch for this shift.')

def process_main_menu_input(user_input):
    time = datetime.datetime.now()
    # Main menu Option 1 - Start Shift (current employee)
    if user_input == '1':
        # Make sure there isn't already a shift for this day (active or complete)
        all_emp_shifts = [shift for shift in shifts if shift['emp_id'] == current_employee['id'] and shift['date'] == time.strftime("%x")]
        if len(all_emp_shifts) > 0 or current_employee['shift_active'] == True:
            print('\nThere is already a shift for this employee on this date.\n')
            show_main_menu()
        else:
            start_shift(current_employee, time.strftime("%x"), time.strftime("%X"))
            current_employee['shift_active'] = True
            show_main_menu()

    # Main menu Option 2 - End Break (current employee)
    elif user_input == '2':
        if current_employee['on_break'] == False or current_employee['shift_active'] == False:
            print('\n*** INVALID ENTRY ***\n')
            show_main_menu()
        else:
            end_break(current_employee, time.strftime("%x"), time.strftime("%X"))
            current_employee['on_break'] = False
            show_main_menu()

    # Main menu Option 3 - End Lunch (current employee)
    elif user_input == '3':
        if current_employee['at_lunch'] == False or current_employee['shift_active'] == False:
            print('\n*** INVALID ENTRY ***\n')
            show_main_menu()
        else:
            end_lunch(current_employee, time.strftime("%x"), time.strftime("%X"))
            current_employee['at_lunch'] = False
            show_main_menu()

    # Main menu Option 4 - Start Break (current employee)
    elif user_input == '4':
        if current_employee['on_break'] == True or current_employee['shift_active'] == False:
            print('\n*** INVALID ENTRY ***\n')
            show_main_menu()
        else:
            start_break(current_employee, time.strftime("%x"), time.strftime("%X"))
            current_employee['on_break'] = True
            show_main_menu()

    # Main menu Option 5 - Start Lunch (current employee)
    elif user_input == '5':
        if current_employee['at_lunch'] == True or current_employee['shift_active'] == False:
            print('\n*** INVALID ENTRY ***\n')
            show_main_menu()
        else:
            start_lunch(current_employee, time.strftime("%x"), time.strftime("%X"))
            current_employee['at_lunch'] = True
            show_main_menu()

    # Main menu Option 6 - End Shift (current employee)
    elif user_input == '6':
        if current_employee['shift_active'] == False or\
            current_employee['on_break'] == True or current_employee['at_lunch'] == True:
            print('\n*** INVALID ENTRY ***\n')
            show_main_menu()
        else:
            end_shift(current_employee, time.strftime("%x"), time.strftime("%X"))
            current_employee['shift_active'] = False
            show_main_menu()

    # Main menu Option 8 - display administrator menu
    elif user_input == '8':
        show_admin_menu()

    # Main menu Option 9 - sign out
    elif user_input == '9':
        print('\nSigning out. Goodbye,', current_employee['first_name'] + '!\n')
        show_start_menu()

    # Invalid input
    else:
        print('\n*** INVALID ENTRY ***\n')
        show_main_menu()

def process_admin_task(option):
    # Admin menu Option 1 - adjust time clock punch
    if option == '1':
        selected_emp_id = input("\nPlease enter an Employee ID: ")
        if validate_emp_id(selected_emp_id) == True:
            selected_employee = [employee for employee in employees if selected_emp_id == employee['id']][0]
            admin_adjust_time(selected_employee)
        else:
            print("No user with that id.\n")
            show_admin_menu()

    # Admin menu Option 2 - display shift report
    elif option == '2':
        selected_emp_id = input("\nPlease enter an employee's ID to see their shift report: ")
        if validate_emp_id(selected_emp_id) == True:
            display_shift_report(selected_emp_id)
        else:
            print("No user with that id.\n")
            show_admin_menu()

    # Admin menu Option 3 - change employee profile
    elif option == '3':
        selected_emp_id = input("\nPlease enter an employee's ID to update their profile: ")
        if validate_emp_id(selected_emp_id) == True:
            update_profile(selected_emp_id)
        else:
            print("No user with that id.\n")
            show_admin_menu()

    # Admin menu Option 4 - Go back to main menu
    elif option == '4':
        show_main_menu()

    else:
        print('\n*** INVALID ENTRY ***\n')
        show_admin_menu()

def admin_adjust_time(emp):
    """ Admin can manually enter time clock data for employees. """

    print('\nADJUST TIME CLOCK DATA FOR', emp['first_name'], emp['last_name'])
    print('\nPRESS 1 to start a shift')
    print('PRESS 2 to end a shift')
    print('PRESS 3 to start a break')
    print('PRESS 4 to end a break')
    print('PRESS 5 to start a lunch')
    print('PRESS 6 to end a lunch')
    print('PRESS 9 to go back to Admin menu\n')

    option = input()

    def get_date_time():
        date = input('\nEnter date (MM/DD/YY): ')
        time = input('\nEnter time (HH:MM:SS): ')
        if date != "" and time != "":
            return {date, time}
        else:
            print('\nDate and/or time input was blank. Operation cancelled.\n')
            return {'date': "", 'time': ""}

    # Start shift
    if option == '1':
        date, time = get_date_time()
        if date != "" and time != "":
            start_shift(emp, date, time)
    elif option == '2':
        date, time = get_date_time()
        if date != "" and time != "":
            end_shift(emp, date, time)
    elif option == '3':
        date, time = get_date_time()
        if date != "" and time != "":
            start_break(emp, date, time)
    elif option == '4':
        date, time = get_date_time()
        if date != "" and time != "":
            end_break(emp, date, time)
    elif option == '5':
        date, time = get_date_time()
        if date != "" and time != "":
            start_lunch(emp, date, time)
    elif option == '6':
        date, time = get_date_time()
        if date != "" and time != "":
            end_lunch(emp, date, time)
    else:
        print('\n*** INVALID ENTRY ***\n')

    show_admin_menu()

def register():
    """ Enter id, first name, and last name to register as new user """

    id_num = input('Please enter Employee ID number: ')
    first = input('First name: ')
    last = input('Last name: ')
    if id_num != "" and first != "" and last != "":
        new_user = Employee(id_num, first, last).__dict__
        employees.append(new_user)
        update_data_file()
        return new_user

def update_profile(emp_id):
    employee = [emp for emp in employees if emp['id'] == emp_id][0]
    print('\nCHANGE PROFILE FOR', employee['first_name'], employee['last_name'])

    answer = input('\nUpdate first name (y/n)? ')
    if answer == 'Y' or answer == 'y':
        employee['first_name'] = input('\nEnter new first name: ')
        print('\nFIRST NAME UPDATED')

    answer = input('\nUpdate last name (y/n)? ')
    if answer == 'Y' or answer == 'y':
        employee['last_name'] = input('\nEnter new last name: ')
        print('\nLAST NAME UPDATED')

    answer = input('\nUpdate admin status (y/n)? ')
    if answer == 'Y' or answer == 'y':
        status = input('\nGive this employee admin status (y/n)? ')
        if status == 'Y' or status == 'y':
            employee['is_admin'] = True
        else:
            employee['is_admin'] = False
        print('\nADMIN STATUS UPDATED\n')

    update_data_file()
    print('\nEmployee: ', employee['first_name'], employee['last_name'], '\nAdmin status:', employee['is_admin'],'\n')
    show_admin_menu()

def display_shift_report(emp_id):
    employee = [emp for emp in employees if emp['id'] == emp_id][0]
    employee_shifts = [shift for shift in shifts if shift['emp_id'] == emp_id]

    print('\nSHIFT REPORT FOR', employee['first_name'], employee['last_name'] + ':\n')
    for shift in employee_shifts:
        print('\tDate:', shift['date'])
        print('\tShift Start:', shift['shift_start'], '--> Shift End:', shift['shift_end'])
        print('\t\tLunches: (', len(shift['lunches']),')')
        if len(shift['lunches']) > 0:
            for lunch in shift['lunches']:
                print('\t\t\tLunch Start:', lunch['lunch_start'], '--> Lunch End:', lunch['lunch_end'])
        print('\t\tBreaks: (', len(shift['breaks']),')')
        if len(shift['breaks']) > 0:
            for brk in shift['breaks']:
                print('\t\t\tBreak Start:', brk['break_start'], '--> Break End:', brk['break_end'])
        print('\t-------------------------------------------------')
    
    print('END OF REPORT')
    input('\nPress Enter to continue\n')
    show_admin_menu()

### MAIN PROGRAM ###
print ('\nTIME CLOCK APPLICATION\n')
get_employee_data()
show_start_menu()

