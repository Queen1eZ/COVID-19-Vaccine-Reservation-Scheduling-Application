# COVID-19 Vaccine Reservation Scheduling Application

## Overview
The project is to build a vaccine scheduling application (with a database hosted on Microsoft Azure) that can be deployed by hospitals or clinics and supports interaction with users through the terminal/command-line interface. In the real world it is unlikely that users would be using the command line terminal instead of a GUI, but all of the application logic would remain the same. For simplicity of programming, we use the command line terminal as our user interface for this assignment.

We need the following entity sets in our database schema design

●	Patients: these are customers that want to receive the vaccine.

●	Caregivers: these are employees of the health organization administering the vaccines.

●	Vaccines: these are vaccine doses in the health organization’s inventory of medical supplies that are on hand and ready to be given to the patients.

●	Reservations: these are appointments that patients will book.


## Details
●	scheduler.py
  * the main runner for your command-line interface

●	scheduler.model
  * Caregiver.py: data model for caregivers
  * Vaccine.py: data model for vaccines
  * Patient.py: data model for patients

●	scheduler.db
  * ConnectionManager.py: a wrapper class to help instantiate the connection to the SQL Server database

●	resources
  * create.sql: the create statement for tables
