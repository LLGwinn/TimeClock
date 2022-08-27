#####################################################################################
#  TIME CLOCK APPLICATION                                                           #
#                                                                                   #
#  In the absence of a database, we store data in a json data file.                 #
#  Each employee 'record' is an instance of the Employee class.                     #
#                                                                                   #
#  Since an employee can technically have multiple breaks and lunches during one    #
#  shift, we have classes for those elements, and the instances are kept in         #
#  lists in the Shift class.                                                        #
#                                                                                   #
#  Employee IDs would normally be serially generated in a database, but for this    #
#  exercise, we will use the employee's SSN (terrible idea normally, but at least   #
#  it will be unique).                                                              # 
#####################################################################################

import datetime
import json

class Employee:
    def __init__(self, emp_id, first_name, last_name):
        self.id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = False;
        self.shifts = [];
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
            emp1 = Employee(123456789, 'John', 'Doe').__dict__
            emp2 = Employee(234567890, 'Jane', 'Doe').__dict__
            # create some date/time objects
            datetime1 = datetime.datetime(2022, 8, 10, 8, 0, 0)
            datetime2 = datetime.datetime(2022, 8, 11, 8, 0, 0)
            datetime3 = datetime.datetime(2022, 8, 12, 8, 0, 0)
            # create some mock shifts
            shift1 = Shift(123456789, datetime1.strftime("%x"), datetime1.strftime("%X")).__dict__
            shift2 = Shift(123456789, datetime2.strftime("%x"), datetime1.strftime("%X")).__dict__
            shift3 = Shift(234567890, datetime3.strftime("%x"), datetime1.strftime("%X")).__dict__
            # format data
            mock_data = {'employees': [emp1, emp2],
                         'shifts': [shift1, shift2, shift3]}
            # add data to time_clock_data.json file
            json.dump(mock_data, data_file, indent=4)
            data_file.seek(0)
            # append the mock data to 'employees' list and 'shifts' list
            employees.append(emp1)
            employees.append(emp2)
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
    # Prepare data to write to file
    emp_data = []
    for employee in employees:
        emp_data.append(employee)

    shift_data = []
    for shift in shifts:
        shift_data.append(shift)

    data_to_export = {'employees': emp_data, 'shifts': shift_data}

    # Write updated data to data file
    with open("time_clock_data.json", "w") as data_file:
        json.dump(data_to_export, data_file, indent=4)

def show_start_options():
    """ Prompts user to sign in, register as new user, or quit the program. """
    
    print('Please choose from the following options:')
    print('PRESS 1 to sign in\nPRESS 2 to register as a new user\
        \nPRESS 0 to quit the Time Clock program\n')
    option = input()
    if option == '1':
        validate_emp_id()
    elif option == '2':
        register()
    elif option == '0':
        print('\nExiting the Time Clock program. Goodbye!\n')
        quit()
    else:
        print('You did not select a valid option.')
        show_start_options()

def validate_emp_id():
    """ Prompts user for employee id, then checks user input against the employees list 
        for valid employee id """

    emp_id = int(input('Please enter Employee ID: '))
    all_ids = []
    for emp in employees:
        all_ids.append(emp['id'])

    if emp_id != '' and emp_id in all_ids:
        global current_employee
        current_employee = [employee for employee in employees if employee['id'] == emp_id][0]
        print('\nHello,', current_employee['first_name'] + '.')
        show_menu_options()
    else:
        print('\n*** Employee ID not valid. ***\n')
        show_start_options()

def show_menu_options():
    """Display options for various clock punches based on current shift, break, and lunch status"""

    print('Please select an option:')

    if current_employee['shift_active'] == False:
        print('\nPRESS 1 to start a shift')
    elif current_employee['on_break'] == True:
        print('PRESS 2 to end your break')
    elif current_employee['at_lunch'] == True:
        print('PRESS 3 to end your lunch')
    else:
        print('PRESS 4 to start your break')
        print('PRESS 5 to start your lunch')
        print('PRESS 6 to end your shift')
    print('PRESS 9 to sign out\n')

    option = input()
    process_clock_punch(option)

def process_clock_punch(user_input):
    time = datetime.datetime.now()

    # Start a shift
    if int(user_input) == 1:
        if current_employee['shift_active'] == True:
            print('You already have an active shift.')
        else:
            new_shift = Shift(current_employee['id'], 
                            time.strftime("%x"),
                            time.strftime("%X"))
            current_employee['shifts'].append(new_shift.__dict__)
            current_employee['shift_active'] = True
            print ('\nSHIFT START:', time.strftime("%x"), 'at', time.strftime("%X"), '.\n')

    # End a break
    elif int(user_input) == 2:
        if current_employee['on_break'] == False or current_employee['shift_active'] == False:
            print('Invalid entry.')
        else:
            current_shift = [shift for shift in current_employee['shifts'] if shift['date'] == time.strftime("%x")][0]
            for brk in current_shift['breaks']:
                if brk['break_start'] != None and brk['break_end'] == None:
                    brk['break_end'] = time.strftime("%X")
                    current_employee['on_break'] = False
                    print ('\nBREAK END:', time.strftime("%x"), 'at', time.strftime("%X"), '.\n')

    # End a lunch
    elif int(user_input) == 3:
        if current_employee['at_lunch'] == False or current_employee['shift_active'] == False:
            print('Invalid entry.')
        else:
            current_shift = [shift for shift in current_employee['shifts'] if shift['date'] == time.strftime("%x")][0]
            for lunch in current_shift['lunches']:
                if lunch['lunch_start'] != None and lunch['lunch_end'] == None:
                    lunch['lunch_end'] = time.strftime("%X")
                    current_employee['at_lunch'] = False
                    print ('\nLUNCH END:', time.strftime("%x"), 'at', time.strftime("%X"), '.\n')

    # Start a break
    elif int(user_input) == 4:
        if current_employee['on_break'] == True or current_employee['shift_active'] == False:
            print('Invalid entry.')
        else:
            for shift in current_employee['shifts']:
                if shift['date'] == time.strftime("%x"):
                    shift['breaks'].append(Break(time.strftime("%X")).__dict__)
                    current_employee['on_break'] = True
                    print ('\nBREAK START:', time.strftime("%x"), 'at', time.strftime("%X"), '.\n')

    # Start a lunch
    elif int(user_input) == 5:
        if current_employee['at_lunch'] == True or current_employee['shift_active'] == False:
            print('Invalid entry.')
        else:
            for shift in current_employee['shifts']:
                if shift['date'] == time.strftime("%x"):
                    shift['lunches'].append(Lunch(time.strftime("%X")).__dict__)
                    current_employee['at_lunch'] = True
                    print ('\nLUNCH START:', time.strftime("%x"), 'at', time.strftime("%X"), '.\n')

    # End a shift
    elif int(user_input) == 6:
        if current_employee['shift_active'] == False:
            print('You have no active shift.')
        else:
            current_shift = [shift for shift in current_employee['shifts'] if shift['date'] == time.strftime("%x")][0]
            if current_shift['shift_end'] == None:
                current_shift['shift_end'] = time.strftime("%X")
                current_employee['shift_active'] = False
                print ('\nSHIFT END:', time.strftime("%x"), 'at', time.strftime("%X"), '.\n')

    # Sign out
    elif int(user_input) == 9:
        print('\nSigning out. Goodbye,', current_employee['first_name'] + '!\n')
        show_start_options()

    # Invalid input
    else:
        print('\nInvalid input. Try again.\n')
        show_start_options()

    update_data_file()
    show_menu_options()


def register():
    """ Enter id, first name, and last name to register as new user """

    id_num = input('Please enter your SSN: ')
    first = input('Please enter your first name: ')
    last = input('Please enter your last name: ')

    new_user = Employee(id_num, first, last)
    employees.append(new_user)
    global current_employee
    current_employee = new_user.__dict__
    print('\nWelcome to the team,', current_employee['first_name'], current_employee['last_name'] + '!\n')
    update_data_file()
    show_menu_options()

### MAIN PROGRAM ###
print ('\nTIME CLOCK APPLICATION\n')
get_employee_data()
show_start_options()