-- Updating the first and last name of Ali Yilmaz in the Individual_Customer table
UPDATE Individual_Customer
SET user_Fname = 'Aliyye', user_Lname = 'Yilmazoglu'
WHERE user_id = 103456;

-- Deleting Mehmet Demir from the Individual_Customer table
DELETE FROM Individual_Customer
WHERE user_id = 122345;

-- Updating the first and last name of FirmaB in the Commercial_Customer table
UPDATE Commercial_Customer
SET user_Fname = 'FirmaEnergyP', user_Lname = 'EnerjiPlus'
WHERE user_id = 155678;

-- Deleting FirmaF from the Commercial_Customer table
DELETE FROM Commercial_Customer
WHERE user_id = 180123;

-- Updating the first and last name of Derya Sari in the Individual_Individual table
UPDATE Individual_Individual
SET user_Fname = 'Deda', user_Lname = 'Sarihan'
WHERE user_id = 238901;

-- Deleting Murat Sezer from the Individual_Individual table
DELETE FROM Individual_Individual
WHERE user_id = 240789;

-- Updating the first and last name of TicI in the Commercial_Individual table
UPDATE Commercial_Individual
SET user_Fname = 'TicX', user_Lname = 'EnerjiNet'
WHERE user_id = 263210;

-- Deleting TicH from the Commercial_Individual table
DELETE FROM Commercial_Individual
WHERE user_id = 298765;

-- Updating the address of an Individual_Customer (user_id: 122345)
UPDATE Address
SET city = 'Iskele', House_num = 85
WHERE user_id = 203456;

-- Deleting the address of an Individual_Customer (user_id: 107654)
DELETE FROM Address
WHERE user_id = 244321;

-- Update the energy meter phase type for a specific user by their user_id
-- Retrieves the address_ID based on the user_id and updates the corresponding energy meter
UPDATE Energy_Meter
SET Type_Phase_Name = 'Two Phase', PhaseType_id = 2
WHERE address_ID = (
    SELECT address_ID FROM Address WHERE user_id = 203456
);

-- Delete the energy meter entry for a specific user by their user_id
-- Finds the related address_ID and deletes the associated energy meter record
DELETE FROM Energy_Meter
WHERE address_ID = (
    SELECT address_ID FROM Address WHERE user_id = 244321
);

-- Update the surname of the manager with e_id = 300001
UPDATE Manager
SET e_surname = 'Yılmaz'
WHERE e_id = 300001;

-- Delete the manager record with e_id = 300010
DELETE FROM Manager
WHERE e_id = 300010;

-- Update the first name of the worker with e_id = 400005
UPDATE Worker
SET e_name = 'Omer'
WHERE e_id = 400005;

-- Delete the worker record with e_id = 400002
DELETE FROM Worker
WHERE e_id = 400002;

-- Update the surname of the technician with e_id = 200003
UPDATE Technician
SET e_surname = 'Kurt'
WHERE e_id = 200003;

-- Delete the technician record with e_id = 200007
DELETE FROM Technician
WHERE e_id = 200007;

-- Update Some details of the ticket with Ticket_ID = 107890  (If A worker had too many tickets and wrong urgency type and wrong description)
UPDATE Ticket
SET 
    Urgency_Type = 1,
    description = 'System Update',
    e_id = 400010
WHERE Ticket_ID = 107890;

-- Update the description of the ticket with Ticket_ID = 101234 (Wrong Description)
UPDATE Ticket
SET description = 'Meter upgrade'
WHERE Ticket_ID = 101234;

-- Delete the ticket with Ticket_ID = 107890 (Spam Ticket)
DELETE FROM Ticket
WHERE Ticket_ID = 107890;

-- Delete all tickets associated with user_id = 103456 (User Created ticket wrongly)
DELETE FROM Ticket
WHERE user_id = 103456;

-- Delete all tickets with Urgency_Type = 1
DELETE FROM Ticket
WHERE Urgency_Type = 1;

-- Update all details of Job with Job_id = 200003
UPDATE Job
SET
    e_id = 400003,
    Urgency_Type = 1,
    Report_date = '2023-03-22',
    Est_Job_time = '01:00:00',
    completion_date = '2023-03-23',
    description = 'Routine inspection and part replacement',
    T_ID = 103456
WHERE Job_id = 200003;

-- Delete the job with Job_id = 200006
DELETE FROM Job
WHERE Job_id = 200006;

--  Delete the job attached to a specific ticket (for example T_ID = 107890))
DELETE FROM Job
WHERE T_ID = 107890;






