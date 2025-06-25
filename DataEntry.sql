
-- DATA ENTRY--
-- 1. User for the Individual_Customer table
INSERT INTO Individual_Customer (user_id, user_Fname, user_Lname)
VALUES (900003, 'Ali', 'Yılmaz');

-- 2. User for the Commercial_Customer table
INSERT INTO Commercial_Customer (user_id, user_Fname, user_Lname)
VALUES (900004, 'Ayşe', 'Demir');

-- 3. User for the Individual_Individual table
INSERT INTO Individual_Individual (user_id, user_Fname, user_Lname)
VALUES (900005, 'Mehmet', 'Kara');

-- 4. User for the Commercial_Individual table
INSERT INTO Commercial_Individual (user_id, user_Fname, user_Lname)
VALUES (900006, 'Zeynep', 'Öztürk');

-- 5. Add Ticket
INSERT INTO Ticket (Ticket_ID, Urgency_Type, description, e_id, user_id)
VALUES (700015, 1, 'Yuksek Voltaj Arizasi', 400005, 238901);

-- 6. Enter jobs from tickets by worker
INSERT INTO Job (Job_id, e_id, Urgency_Type, Report_date, Est_Job_time, completion_date, description, T_ID)
VALUES (200099, 400005, 3, '2023-01-15', '02:30:00', '2023-01-16', 'Broken Meter', 700015);

-- 7. Enter the new energy meter properties
INSERT INTO Energy_Meter (Energy_meter_id, mac_id, Type_Phase_Name, PhaseType_id, address_ID) VALUES
(99999999, 'a2:00:99:c9:13:4c', 'Two Phase', 2, '010123');

-- 8. Enter the details of energy meter communication configuration
INSERT INTO Communication (Local_IP_ID, EM_ID, comminication_type) VALUES
(300999, 99999999, 'WiFi');


