-- a) Present consumption reports of a region.(For Example:Guzelyurt)--
SELECT 
    a.address_ID,
    a.city,
    em.Energy_meter_id,
    m.Date,
    m.Volt,
    m.Watt_Hour,
    m.Watt
FROM 
    Address a
JOIN 
    Energy_Meter em ON a.address_ID = em.address_ID
JOIN 
    Measurements m ON em.Energy_meter_id = m.EM_ID
WHERE 
    a.city = 'Guzelyurt';


-- b) Present consumption reports of registered user addresses. --

-- Create View for all users--
CREATE OR REPLACE VIEW Users AS
SELECT 
    user_id,
    user_Fname AS first_name,
    user_Lname AS last_name,
    'Individual_Customer' AS user_role
FROM Individual_Customer

UNION ALL

SELECT 
    user_id,
    user_Fname AS first_name,
    user_Lname AS last_name,
    'Commercial_Customer' AS user_role
FROM Commercial_Customer

UNION ALL

SELECT 
    user_id,
    user_Fname AS first_name,
    user_Lname AS last_name,
    'Individual_Individual' AS user_role
FROM Individual_Individual

UNION ALL

SELECT 
    user_id,
    user_Fname AS first_name,
    user_Lname AS last_name,
    'Commercial_Individual' AS user_role
FROM Commercial_Individual;


-- DataQuery--

SELECT 
    u.user_id,
    u.first_name,
    u.last_name,
    a.city,
    a.House_num,
    a.street_num,
    m.Date AS consumption_date,
    m.Volt AS voltage,
    m.Watt_Hour AS watt_hour,
    m.Watt AS watt
FROM 
    Users u
JOIN 
    Address a ON u.user_id = a.user_id
JOIN 
    Energy_Meter em ON a.address_ID = em.address_ID
JOIN 
    Measurements m ON em.Energy_meter_id = m.EM_ID
ORDER BY 
    u.user_id, m.Date;

-- c) List complaints registered by users. --

SELECT 
    -- U.user_id,
    U.first_name,
    U.last_name,
    U.user_role,
    -- T.ticket_id,
    T.description
FROM Ticket T
JOIN Users U ON T.user_id = U.user_id;

-- d) List jobs to be done registered by workers. --

SELECT 
    J.description AS job_description,
    J.completion_date,
    J.Report_date
FROM 
    Job J;
    
    -- e) List user bills with their date and monthly debt. -- 
    
SELECT 
    u.first_name, 
    u.last_name, 
    Bill.Date, 
    Bill.Montly_dept
FROM Users u
LEFT JOIN Address ON u.user_id = Address.user_id
LEFT JOIN Energy_Meter ON Address.address_ID = Energy_Meter.address_ID
LEFT JOIN Bill ON Energy_Meter.Energy_meter_id = Bill.EM_ID
WHERE Bill.Date IS NOT NULL 
  AND Bill.Montly_dept IS NOT NULL;


    -- f) List technician details that worked on a specific job. -- 
SELECT t.e_id, t.e_name, t.e_surname 
FROM Technician t
INNER JOIN Complates c ON t.e_id = c.e_id
INNER JOIN Job j ON c.Job_id = j.Job_id
WHERE j.description = 'Routine inspection';

    -- g) List unordinary monthly consumptions of users . -- 
    
/*NOT ENOUGH DATA TO COMPUTE*/
    
    
    -- h) List the number of users registered on Guzelyurt -- 
SELECT COUNT(DISTINCT u.user_id) AS user_count
FROM (
    SELECT user_id FROM Individual_Customer
    UNION
    SELECT user_id FROM Commercial_Customer
    UNION
    SELECT user_id FROM Individual_Individual
    UNION
    SELECT user_id FROM Commercial_Individual
) AS u
INNER JOIN Address a ON u.user_id = a.user_id
WHERE a.city = 'Guzelyurt';

    -- i) List of Energy meter IDs that have greater than 15 kWh consumption in Guzelyurt -- 
SELECT DISTINCT em.Energy_meter_id
FROM Energy_Meter em
INNER JOIN Address a ON em.address_ID = a.address_ID
INNER JOIN Measurements m ON em.Energy_meter_id = m.EM_ID
WHERE a.city = 'Guzelyurt'
AND m.Watt > 15;
    -- j) List the user name, surname, address, and energy meter ID of all properties in Guzelyurt, ordered by consumption amount. -- 
SELECT 
  u.user_Fname,
  u.user_Lname,
  a.House_num,
  a.street_num,
  a.city,
  em.Energy_meter_id,
  SUM(m.Watt_Hour) AS total_watt_hour
FROM (
    SELECT user_id, user_Fname, user_Lname FROM Individual_Customer
    UNION
    SELECT user_id, user_Fname, user_Lname FROM Commercial_Customer
    UNION
    SELECT user_id, user_Fname, user_Lname FROM Commercial_Individual
    UNION
    SELECT user_id, user_Fname, user_Lname FROM Individual_Individual
) u
JOIN Address a ON u.user_id = a.user_id
JOIN Energy_Meter em ON a.address_ID = em.address_ID
JOIN Measurements m ON em.Energy_meter_id = m.EM_ID
WHERE a.city = 'Guzelyurt'
GROUP BY 
  u.user_id, 
  u.user_Fname,  
  u.user_Lname,   
  a.House_num, 
  a.street_num, 
  a.city,
  em.Energy_meter_id
ORDER BY total_watt_hour DESC;


-- k) Identify the technician with at least ten energy meter checks and completed more than 20 jobs in Guzelyurt(tested well) -- 
SELECT t.e_id, t.e_name, t.e_surname
FROM Technician t
WHERE t.e_id IN (
    SELECT c.e_id
    FROM Complates c
    JOIN Job j ON c.Job_id = j.Job_id
    GROUP BY c.e_id
    HAVING 
        COUNT(CASE WHEN j.description LIKE '%Check%' THEN 1 END) >= 10
        AND 
        COUNT(CASE WHEN j.description NOT LIKE '%Check%' THEN 1 END) >= 20
);
    -- l) Identify the total number of ticked and the sum of type “3” urgent code  -- 
SELECT 
    COUNT(*) AS total_tickets,
    SUM(Urgency_Type = 3) AS urgent_type3_count
FROM Ticket;
    -- m) List User A's energy meter’s which has 3-phase and  “GPRS” communication --  (For Example TicB)
SELECT em.Energy_meter_id
FROM (
    SELECT user_id 
    FROM Individual_Customer 
    WHERE user_Fname = 'TicB'
    UNION ALL
    SELECT user_id 
    FROM Commercial_Customer 
    WHERE user_Fname = 'TicB'
    UNION ALL
    SELECT user_id 
    FROM Individual_Individual 
    WHERE user_Fname = 'TicB'
    UNION ALL
    SELECT user_id 
    FROM Commercial_Individual 
    WHERE user_Fname = 'TicB'
) u
JOIN Address a ON u.user_id = a.user_id
JOIN Energy_Meter em ON a.address_ID = em.address_ID
JOIN Communication c ON em.Energy_meter_id = c.EM_ID
WHERE em.Type_Phase_Name = 'three phase'
  AND c.comminication_type = 'GPRS';
  
    -- n)List specific users statistics for daily, monthly and yearly basis. -- 

SELECT 
    'DAILY' AS Time_Granularity,
    m.Date AS Time_Value,
    NULL AS Month,
    NULL AS Year,
    SUM(m.Watt_Hour) AS Total_Watt_Hour,
    SUM(m.Watt) AS Total_Watt,
    a.user_id,
    u.user_Fname,
    u.user_Lname
FROM 
    Measurements m
JOIN Energy_Meter em ON m.EM_ID = em.Energy_meter_id
JOIN Address a ON em.address_ID = a.address_ID
JOIN Individual_Individual u ON a.user_id = u.user_id
WHERE a.user_id = 203456
GROUP BY m.Date, a.user_id, u.user_Fname, u.user_Lname

UNION ALL

SELECT 
    'MONTHLY' AS Time_Granularity,
    NULL AS Time_Value,
    MONTH(m.Date) AS Month,
    YEAR(m.Date) AS Year,
    SUM(m.Watt_Hour) AS Total_Watt_Hour,
    SUM(m.Watt) AS Total_Watt,
    a.user_id,
    u.user_Fname,
    u.user_Lname
FROM 
    Measurements m
JOIN Energy_Meter em ON m.EM_ID = em.Energy_meter_id
JOIN Address a ON em.address_ID = a.address_ID
JOIN Individual_Individual u ON a.user_id = u.user_id
WHERE a.user_id = 203456
GROUP BY YEAR(m.Date), MONTH(m.Date), a.user_id, u.user_Fname, u.user_Lname

UNION ALL

SELECT 
    'YEARLY' AS Time_Granularity,
    NULL AS Time_Value,
    NULL AS Month,
    YEAR(m.Date) AS Year,
    SUM(m.Watt_Hour) AS Total_Watt_Hour,
    SUM(m.Watt) AS Total_Watt,
    a.user_id,
    u.user_Fname,
    u.user_Lname
FROM 
    Measurements m
JOIN Energy_Meter em ON m.EM_ID = em.Energy_meter_id
JOIN Address a ON em.address_ID = a.address_ID
JOIN Individual_Individual u ON a.user_id = u.user_id
WHERE a.user_id = 203456
GROUP BY YEAR(m.Date), a.user_id, u.user_Fname, u.user_Lname;


    
    -- o) Identify the total number of jobs done by a specific technician in the last three months.. -- 
    
SELECT 
    T.e_id,
    T.e_name,
    T.e_surname,
    COUNT(C.job_id) AS completed_jobs_last_3_months
FROM 
    complates C
JOIN 
    job J ON C.job_id = J.job_id
JOIN 
    technician T ON C.e_id = T.e_id
WHERE 
    J.completion_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
    AND T.e_id = 200003
GROUP BY 
    T.e_id, T.e_name, T.e_surname
ORDER BY 
    completed_jobs_last_3_months DESC;




