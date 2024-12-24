CREATE TABLE Caregivers (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Availabilities (
    Time date,
    Username varchar(255) REFERENCES Caregivers,
    PRIMARY KEY (Time, Username)
);

CREATE TABLE Vaccines (
    Name varchar(255),
    Doses int,
    PRIMARY KEY (Name)
);

CREATE TABLE Patients (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Reservations (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Patient_Name VARCHAR(255) REFERENCES Patients(Username),
    Caregiver_Name VARCHAR(255) REFERENCES Caregivers(Username),
    Vaccine_Name VARCHAR(255) REFERENCES Vaccines(Name),
    Reservation_Time DATE,
    UNIQUE (Caregiver_Name, Reservation_Time) --a caregiver can only have one reservation per day
);