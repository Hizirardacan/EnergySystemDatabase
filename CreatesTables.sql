/*use energysystem;*/

CREATE TABLE Individual_Customer (
    user_id INT PRIMARY KEY,
    user_Fname VARCHAR(50),
    user_Lname VARCHAR(50)
);

CREATE TABLE Commercial_Customer (
    user_id INT PRIMARY KEY,
    user_Fname VARCHAR(50),
    user_Lname VARCHAR(50)
);

CREATE TABLE Individual_Individual (
    user_id INT PRIMARY KEY,
    user_Fname VARCHAR(50),
    user_Lname VARCHAR(50)
);

CREATE TABLE Commercial_Individual (
    user_id INT PRIMARY KEY,
    user_Fname VARCHAR(50),
    user_Lname VARCHAR(50)
);

CREATE TABLE Manager (
	e_id INT PRIMARY KEY,
    e_name VARCHAR(50),
    e_surname VARCHAR(50)
);

CREATE TABLE Worker (
    e_id INT PRIMARY KEY,
    e_name VARCHAR(50),
    e_surname VARCHAR(50)
);

CREATE TABLE Technician (
    e_id INT PRIMARY KEY,
    e_name VARCHAR(50),
    e_surname VARCHAR(50)
);


CREATE TABLE Address (
    address_ID VARCHAR(10) PRIMARY KEY,
    city VARCHAR(50),
    House_num INT,
    street_num INT,
    user_id INT,
    user_type ENUM('Individual_Customer', 'Commercial_Customer', 'Individual_Individual', 'Commercial_Individual'),
    CHECK (user_type IN ('Individual_Customer', 'Commercial_Customer', 'Individual_Individual', 'Commercial_Individual'))
);

ALTER TABLE Address
DROP COLUMN user_type;

CREATE TABLE Energy_Meter (
    Energy_meter_id BIGINT PRIMARY KEY,
    mac_id VARCHAR(17),
    Type_Phase_Name VARCHAR(20),
    PhaseType_id INT,
    address_ID VARCHAR(10),
    FOREIGN KEY (address_ID) REFERENCES Address(address_ID)
    ON DELETE CASCADE
);

CREATE TABLE Bill (
    Bill_ID INT PRIMARY KEY,
    Total_debt DECIMAL(10,2),
    kwh_rate DECIMAL(5,2),
    Date DATE,
    Montly_dept DECIMAL(10,2),
    Is_paid BOOLEAN,
    EM_ID BIGINT,
    FOREIGN KEY (EM_ID) REFERENCES Energy_Meter(Energy_meter_id)
    ON DELETE CASCADE
);

CREATE TABLE Statistics (
    Stats_No INT PRIMARY KEY,
    EM_ID BIGINT,
    FOREIGN KEY (EM_ID) REFERENCES Energy_Meter(Energy_meter_id)
    ON DELETE CASCADE
);

CREATE TABLE Ticket (
    Ticket_ID INT PRIMARY KEY,
    Urgency_Type INT,
    description VARCHAR(100),
    e_id INT,
    user_id INT,
    user_type ENUM('Individual_Customer', 'Commercial_Customer', 'Individual_Individual', 'Commercial_Individual'),
    CHECK (user_type IN ('Individual_Customer', 'Commercial_Customer', 'Individual_Individual', 'Commercial_Individual')) -- user type donduruyor baska yolunu bulamadim
);

ALTER TABLE Ticket
DROP COLUMN user_type;


CREATE TABLE Job (
    Job_id INT PRIMARY KEY,
    e_id INT,
    Urgency_Type INT,
    Report_date DATE,
    Est_Job_time TIME,
    completion_date DATE NULL,
    description VARCHAR(100),
    T_ID INT,
    FOREIGN KEY (e_id) REFERENCES Worker(e_id),
    FOREIGN KEY (T_ID) REFERENCES Ticket(Ticket_ID)
    ON DELETE CASCADE
);

CREATE TABLE Checks (
    e_id INT,
    EM_ID BIGINT,
    FOREIGN KEY (e_id) REFERENCES Technician(e_id),
    FOREIGN KEY (EM_ID) REFERENCES Energy_Meter(Energy_meter_id)
    ON DELETE CASCADE
);

CREATE TABLE Complates (
    e_id INT,
    Job_id INT,
    FOREIGN KEY (e_id) REFERENCES Technician(e_id),
    FOREIGN KEY (Job_id) REFERENCES Job(Job_id)
    ON DELETE CASCADE
);

CREATE TABLE Report (
    e_id INT,
    Stats_No INT,
    FOREIGN KEY (e_id) REFERENCES Manager(e_id),
    FOREIGN KEY (Stats_No) REFERENCES Statistics(Stats_No)
    ON DELETE CASCADE
);


CREATE TABLE Communication (
    Local_IP_ID INT PRIMARY KEY,
    EM_ID BIGINT,
    comminication_type VARCHAR(20),
    FOREIGN KEY (EM_ID) REFERENCES Energy_Meter(Energy_meter_id)
    ON DELETE CASCADE
);

CREATE TABLE Measurements (
    Date DATE,
    EM_ID BIGINT,
    Volt INT,
    Watt_Hour INT,
    Watt INT,
    FOREIGN KEY (EM_ID) REFERENCES Energy_Meter(Energy_meter_id)
    ON DELETE CASCADE
);


CREATE TABLE Daily_Min_Stats (
    Stats_No INT,
    EM_ID BIGINT,
    Daily_min_consume_time DATE,
    FOREIGN KEY (Stats_No) REFERENCES Statistics(Stats_No) ON DELETE CASCADE,
    FOREIGN KEY (EM_ID) REFERENCES Energy_Meter(Energy_meter_id)ON DELETE CASCADE
);

CREATE TABLE Daily_Max_Stats (
    Stats_No INT,
    EM_ID BIGINT,
    Daily_max_consume_time DATE,
    FOREIGN KEY (Stats_No) REFERENCES Statistics(Stats_No) ON DELETE CASCADE,
    FOREIGN KEY (EM_ID) REFERENCES Energy_Meter(Energy_meter_id)ON DELETE CASCADE
);

CREATE TABLE Monthly_Min_Stats (
    Stats_No INT,
    EM_ID BIGINT,
    Monthly_min_consume_time VARCHAR(7),  -- Format: YYYY-MM
    FOREIGN KEY (Stats_No) REFERENCES Statistics(Stats_No) ON DELETE CASCADE,
    FOREIGN KEY (EM_ID) REFERENCES Energy_Meter(Energy_meter_id)ON DELETE CASCADE
);

CREATE TABLE Monthly_Max_Stats (
    Stats_No INT,
    EM_ID BIGINT,
    Monthly_max_consume_time VARCHAR(7),
    FOREIGN KEY (Stats_No) REFERENCES Statistics(Stats_No) ON DELETE CASCADE,
    FOREIGN KEY (EM_ID) REFERENCES Energy_Meter(Energy_meter_id)ON DELETE CASCADE
);

CREATE TABLE Yearly_Min_Stats (
    Stats_No INT,
    EM_ID BIGINT,
    Yearly_min_consume_time YEAR,
    FOREIGN KEY (Stats_No) REFERENCES Statistics(Stats_No) ON DELETE CASCADE,
    FOREIGN KEY (EM_ID) REFERENCES Energy_Meter(Energy_meter_id)ON DELETE CASCADE
);

CREATE TABLE Yearly_Max_Stats (
    Stats_No INT,
    EM_ID BIGINT,
    Yearly_max_consume_time YEAR,
    FOREIGN KEY (Stats_No) REFERENCES Statistics(Stats_No) ON DELETE CASCADE,
    FOREIGN KEY (EM_ID) REFERENCES Energy_Meter(Energy_meter_id)ON DELETE CASCADE
);