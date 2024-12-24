from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime
import re

'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None

def is_strong_password(password):
    if len(password) < 8:
        print("Password length check failed. See Guideline a")
        return False
    if not re.search("[a-z]", password):
        print("Lowercase letter check failed. See Guideline b")
        return False
    if not re.search("[A-Z]", password):
        print("Uppercase letter check failed. See Guideline b")
        return False
    if not re.search("[0-9]", password):
        print("Number check failed. See Guideline c")
        return False
    if not re.search("[!@#?]", password):
        print("Special character check failed. See Guideline d")
        return False
    return True

def create_patient(tokens):
    # TODO: Part 1
    # create_patient <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]

    # check 2: check if the username has been taken already
    if username_exists_patient(username):
        print("Username taken, try again!")
        return

    # check 3: validate the password strength
    if not is_strong_password(password):
        print(
            "Password is not strong enough. It must be:\n"
            "a. At least 8 characters\n"
            "b. A mixture of both uppercase and lowercase letters\n"
            "c. A mixture of letters and numbers\n"
            "d. Inclusion of at least one special character, from “!”, “@”, “#”, “?” ")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the patient
    patient = Patient(username, salt=salt, hash=hash)

    # save to patient information to our database
    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)

def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    # check 3: validate the password strength
    if not is_strong_password(password):
        print(
            "Password is not strong enough. It must be:\n"
            "a. At least 8 characters\n"
            "b. A mixture of both uppercase and lowercase letters\n"
            "c. A mixture of letters and numbers\n"
            "d. Inclusion of at least one special character, from “!”, “@”, “#”, “?” ")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)


def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):
    # TODO: Part 1
    # login_patient <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_patient
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    patient = None
    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if patient is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_patient = patient


def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if caregiver is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    # TODO: Part 2
    # search_caregiver_schedule <date>
    global current_patient
    global current_caregiver
    # check 1: if not logged in, they need to log in first
    if current_caregiver is None and current_patient is None:
        print("Please login first")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])

    # Retrieve available caregivers for the given date
    get_caregivers = "SELECT Username FROM Availabilities WHERE Time = %s ORDER BY Username"

    cm = ConnectionManager()
    conn = cm.create_connection()
    try:
        cursor = conn.cursor(as_dict=True)
        d = datetime.datetime(year, month, day)
        cursor.execute(get_caregivers, d)
        caregivers = [row['Username'] for row in cursor]

        get_vaccines = "SELECT Name, Doses FROM Vaccines"
        cursor.execute(get_vaccines)
        vaccines = [(row['Name'], row['Doses']) for row in cursor]

        # Output the results
        for caregiver in caregivers:
            print(caregiver)
        for vaccine, doses in vaccines:
            print(f"{vaccine} {doses}")

    except IndexError:
        print("Please try again")
    except pymssql.Error as e:
        print("Please try again")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Please try again")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False

def reserve(tokens):
    """
    TODO: Part 2
    """
    #  reserve <date> <vaccine>
    global current_patient
    global current_caregiver
    # check 1: if not logged in, they need to log in first
    if current_caregiver is None and current_patient is None:
        print("Please login first")
        return
    # check 2: check if the current logged-in user is a patient
    if current_patient is None and current_caregiver is not None:
        print("Please login as a patient first!")
        return

    # check 3: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    date = tokens[1]
    vaccine_name = tokens[2]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])

    # Retrieve available caregivers for the given date
    get_caregivers = "SELECT Username FROM Availabilities WHERE Time = %s ORDER BY Username"

    cm = ConnectionManager()
    conn = cm.create_connection()

    try:
        cursor = conn.cursor(as_dict=True)
        d = datetime.datetime(year, month, day)
        cursor.execute(get_caregivers, d)
        caregivers = [row['Username'] for row in cursor]
        if not caregivers:
            print("No caregiver is available")
            return

        # Check vaccine availability
        select_vaccines = "SELECT Doses FROM Vaccines WHERE Name = %s"
        cursor.execute(select_vaccines, vaccine_name)
        vaccine = cursor.fetchone()
        if not vaccine or vaccine['Doses'] <= 0:
            print("Not enough available doses")
            return

        # Choose the caregiver by alphabetical order
        selected_caregiver = caregivers[0]

        # Create a reservation
        insert_reservation = "INSERT INTO Reservations (Patient_Name, Caregiver_Name, Vaccine_Name, Reservation_Time) VALUES (%s, %s, %s, %s)"

        cursor.execute(insert_reservation, (current_patient.username, selected_caregiver, vaccine_name, d))
        conn.commit()

        # Update caregiver availability and vaccine doses
        delete_availability = "DELETE FROM Availabilities WHERE Username = %s AND Time = %s"
        cursor.execute(delete_availability, (selected_caregiver, d))

        update_vaccine = "UPDATE Vaccines SET Doses = Doses - 1 WHERE Name = %s"
        cursor.execute(update_vaccine, vaccine_name)
        conn.commit()

        # Get the reservation ID
        cursor.execute("SELECT SCOPE_IDENTITY() AS id")
        reservation_id = cursor.fetchone()['id']

        # Output the results
        print(f"Appointment ID {reservation_id}, Caregiver username {selected_caregiver}")

    except IndexError:
        print("Please try again")
    except pymssql.Error as e:
        print("Please try again")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Please try again")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    try:
        d = datetime.datetime(year, month, day)
        current_caregiver.upload_availability(d)
    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        return
    print("Availability uploaded!")


def cancel(tokens):
    # TODO: Extra Credit
    global current_patient
    global current_caregiver
    # check 1: if not logged in, they need to log in first
    if current_caregiver is None and current_patient is None:
        print("Please login first")
        return

    #  check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    id = int(tokens[1])

    cm = ConnectionManager()
    conn = cm.create_connection()
    try:
        cursor = conn.cursor(as_dict=True)
        # Retrieve the appointment details
        get_appointment = "SELECT ID, Patient_Name, Caregiver_Name, Vaccine_Name, Reservation_Time FROM Reservations WHERE ID = %s"
        cursor.execute(get_appointment, id)
        appointment = cursor.fetchone()
        if not appointment:
            print("Please try again")
            print("Error: Appointment not found")
            return

        # Ensure the logged-in user is authorized to cancel the appointment
        if current_caregiver is not None and appointment['Caregiver_Name'] != current_caregiver.username:
            print("Please try again")
            print("Error: Unauthorized action")
            return

        if current_patient is not None and appointment['Patient_Name'] != current_patient.username:
            print("Please try again")
            print("Error: Unauthorized action")
            return

        # Delete the appointment
        delete_appointment = "DELETE FROM Reservations WHERE ID = %s"
        cursor.execute(delete_appointment, id)

        # Update caregiver availability
        insert_availability_query = "INSERT INTO Availabilities (Time, Username) VALUES (%s, %s)"
        cursor.execute(insert_availability_query, (appointment['Reservation_Time'], appointment['Caregiver_Name']))

        # Update vaccine doses
        update_vaccine = "UPDATE Vaccines SET Doses = Doses + 1 WHERE Name = %s"
        cursor.execute(update_vaccine, appointment['Vaccine_Name'])
        conn.commit()

        # Output the results
        print(f"Appointment {id} canceled successfully")

    except IndexError:
        print("Please try again")
    except pymssql.Error as e:
        print("Please try again")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Please try again")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        vaccine = Vaccine(vaccine_name, doses).get()
    except pymssql.Error as e:
        print("Error occurred when adding doses")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when adding doses")
        print("Error:", e)
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    print("Doses updated!")


def show_appointments(tokens):
    # TODO: Part 2
    global current_patient
    global current_caregiver
    # check : if not logged in, they need to log in first
    if current_caregiver is None and current_patient is None:
        print("Please login first")
        return

    cm = ConnectionManager()
    conn = cm.create_connection()
    try:
        cursor = conn.cursor(as_dict=True)
        if current_caregiver is not None:
            # Caregiver is logged in
            show_appointments_caregiver = "SELECT ID, Vaccine_Name, Reservation_Time, Patient_Name FROM Reservations WHERE Caregiver_Name = %s ORDER BY ID"
            cursor.execute(show_appointments_caregiver, current_caregiver.username)
            appointments = cursor.fetchall()
            if not appointments:
                print("No appointments found")
                return
            # Output the caregiver's appointments
            for appointment in appointments:
                print(f"{appointment['ID']} {appointment['Vaccine_Name']} "
                        f"{appointment['Reservation_Time'].strftime('%m-%d-%Y')} {appointment['Patient_Name']}")

        elif current_patient is not None:
            # Patient is logged in
            show_appointments_patient = "SELECT ID, Vaccine_Name, Reservation_Time, Caregiver_Name FROM Reservations WHERE Patient_Name = %s ORDER BY ID"
            cursor.execute(show_appointments_patient, current_patient.username)
            appointments = cursor.fetchall()
            if not appointments:
                print("No appointments found")
                return
            # Output the patient's appointments
            for appointment in appointments:
                print(f"{appointment['ID']} {appointment['Vaccine_Name']} "
                        f"{appointment['Reservation_Time'].strftime('%m-%d-%Y')} {appointment['Caregiver_Name']}")

    except pymssql.Error as db_error:
        print("Please try again")
        print("Database Error:", db_error)
    except Exception as e:
        print("Please try again")
        print("Error:", e)
    finally:
        cm.close_connection()


def logout(tokens):
    # TODO: Part 2
    global current_patient
    global current_caregiver
    # check: if not logged in, they need to log in first
    if current_caregiver is None and current_patient is None:
        print("Please login first")
    else:
        try:
            current_caregiver = None
            current_patient = None
            print("Successfully logged out")
        except Exception as e:
            print("Please try again")
            print("Error:", e)


def start():
    stop = False
    print()
    print(" *** Please enter one of the following commands *** ")
    print("> create_patient <username> <password>")  # //TODO: implement create_patient (Part 1)
    print("> create_caregiver <username> <password>")
    print("> login_patient <username> <password>")  # // TODO: implement login_patient (Part 1)
    print("> login_caregiver <username> <password>")
    print("> search_caregiver_schedule <date>")  # // TODO: implement search_caregiver_schedule (Part 2)
    print("> reserve <date> <vaccine>")  # // TODO: implement reserve (Part 2)
    print("> upload_availability <date>")
    print("> cancel <appointment_id>")  # // TODO: implement cancel (extra credit)
    print("> add_doses <vaccine> <number>")
    print("> show_appointments")  # // TODO: implement show_appointments (Part 2)
    print("> logout")  # // TODO: implement logout (Part 2)
    print("> Quit")
    print()
    while not stop:
        response = ""
        print("> ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Please try again!")
            break

        #response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Please try again!")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == "cancel":
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Bye!")
            stop = True
        else:
            print("Invalid operation name!")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()
