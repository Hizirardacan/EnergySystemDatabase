from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import random
from datetime import datetime
app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL database config
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '0000',
    'database': 'energysystem',
    'port': 3306
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

def get_table_columns(table_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DESCRIBE {table_name}")
    columns = [column[0] for column in cursor.fetchall()]
    conn.close()
    return columns

def get_primary_key_column(table_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COLUMN_NAME
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND CONSTRAINT_NAME = 'PRIMARY'
    """, (DB_CONFIG['database'], table_name))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_city_code(city_name):
    city_codes = {
        'Lefkosa': '01',
        'Girne': '02',
        'Gazimagusa': '03',
        'Guzelyurt': '04',
        'Iskele': '05',
        'Lefke': '06'
    }
    return city_codes.get(city_name, None)

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    result = []
    columns = []
    query_description = ""
    selected_query = None
    
    if request.method == 'POST':
        query_id = request.form.get('query_id')
        
        if query_id:
            selected_query = query_id
            user_id = request.form.get('user_id')  # Get user_id from form
            
            try:
                # Connect to the database
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                # Query a - Regional Consumption Reports
                if query_id == 'a':
                    region = request.form.get('region', 'Guzelyurt')  # Get region from form with default 'Guzelyurt'
                    query_description = f"Consumption reports of region: {region}"
                    query = """
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
                        a.city = %s
                    """
                    cursor.execute(query, (region,))
                    result = cursor.fetchall()
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                
                # Query b - User Address Consumption Reports
                elif query_id == 'b':
                    query_description = "Consumption reports of registered user addresses"
                    if user_id:
                        query = """
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
                        WHERE
                            u.user_id = %s
                        ORDER BY 
                            m.Date
                        """
                        cursor.execute(query, (user_id,))
                    else:
                        query = """
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
                            u.user_id, m.Date
                        """
                        cursor.execute(query)
                    result = cursor.fetchall()
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                
                # Query c - User Complaints List
                elif query_id == 'c':
                    query_description = "List complaints registered by users"
                    query = """
                    SELECT 
                        U.first_name,
                        U.last_name,
                        U.user_role,
                        T.description
                    FROM Ticket T
                    JOIN Users U ON T.user_id = U.user_id
                    """
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                
                # Query d - Jobs To Be Done
                elif query_id == 'd':
                    query_description = "List jobs to be done registered by workers"
                    query = """
                    SELECT 
                        J.description AS job_description,
                        J.completion_date,
                        J.Report_date
                    FROM 
                        Job J
                    """
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                
                # Query e - User Bills Summary
                elif query_id == 'e':
                    query_description = "List user bills with their date and monthly debt"
                    if user_id:
                        query = """
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
                          AND Bill.Montly_dept IS NOT NULL
                          AND u.user_id = %s
                        """
                        cursor.execute(query, (user_id,))
                    else:
                        query = """
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
                          AND Bill.Montly_dept IS NOT NULL
                        """
                        cursor.execute(query)
                    result = cursor.fetchall()
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                
                # Query f - Technicians by Job
                elif query_id == 'f':
                    job_desc = request.form.get('job_desc')
                    query_description = f"List technician details that worked on: {job_desc}"
                    query = """
                    SELECT t.e_id, t.e_name, t.e_surname 
                    FROM Technician t
                    INNER JOIN Complates c ON t.e_id = c.e_id
                    INNER JOIN Job j ON c.Job_id = j.Job_id
                    WHERE j.description = %s
                    """
                    cursor.execute(query, (job_desc,))
                    result = cursor.fetchall()
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                
                # Query h - User Count by Region (Guzelyurt)
                elif query_id == 'h':
                    region = request.form.get('region', 'Guzelyurt')  # Get region parameter
                    query_description = f"Number of users registered in {region}"
                    query = """
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
                    WHERE a.city = %s
                    """
                    cursor.execute(query, (region,))
                    result = cursor.fetchall()
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                
                # Query i - High Consumption Meters in Guzelyurt
                elif query_id == 'i':
                    query_description = "Energy meter IDs with high consumption in Guzelyurt"
                    query = """
                    SELECT DISTINCT em.Energy_meter_id
                    FROM Energy_Meter em
                    INNER JOIN Address a ON em.address_ID = a.address_ID
                    INNER JOIN Measurements m ON em.Energy_meter_id = m.EM_ID
                    WHERE a.city = 'Guzelyurt'
                    AND m.Watt > 15
                    """
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                
                # Query j - Properties in Guzelyurt by Consumption
                elif query_id == 'j':
                    query_description = "Properties in Guzelyurt by consumption"
                    query = """
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
                    ORDER BY total_watt_hour DESC
                    """
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                
                # Query k - Top Technicians
                elif query_id == 'k':
                    query_description = "Technicians with high performance"
                    query = """
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
                    )
                    """
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                
                # Query l - Ticket Summary Report
                elif query_id == 'l':
                    query_description = "Ticket summary with urgent codes"
                    query = """
                    SELECT 
                        COUNT(*) AS total_tickets,
                        SUM(Urgency_Type = 3) AS urgent_type3_count
                    FROM Ticket
                    """
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                
                # Query m - Special Energy Meters (3-phase GPRS)
                elif query_id == 'm':
                    query_description = "User's energy meters with 3-phase and GPRS"
                    user_fname = request.form.get('user_fname', 'TicB')
                    query = """
                    SELECT em.Energy_meter_id
                    FROM (
                        SELECT user_id 
                        FROM Individual_Customer 
                        WHERE user_Fname = %s
                        UNION ALL
                        SELECT user_id 
                        FROM Commercial_Customer 
                        WHERE user_Fname = %s
                        UNION ALL
                        SELECT user_id 
                        FROM Individual_Individual 
                        WHERE user_Fname = %s
                        UNION ALL
                        SELECT user_id 
                        FROM Commercial_Individual 
                        WHERE user_Fname = %s
                    ) u
                    JOIN Address a ON u.user_id = a.user_id
                    JOIN Energy_Meter em ON a.address_ID = em.address_ID
                    JOIN Communication c ON em.Energy_meter_id = c.EM_ID
                    WHERE em.Type_Phase_Name = 'three phase'
                      AND c.comminication_type = 'GPRS'
                    """
                    cursor.execute(query, (user_fname, user_fname, user_fname, user_fname))
                    result = cursor.fetchall()
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                
                # Query n - User Statistics
                elif query_id == 'n':
                    query_description = "User statistics for daily, monthly, yearly basis"
                    stat_user_id = request.form.get('stat_user_id', '203456')
                    query = """
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
                    WHERE a.user_id = %s
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
                    WHERE a.user_id = %s
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
                    WHERE a.user_id = %s
                    GROUP BY YEAR(m.Date), a.user_id, u.user_Fname, u.user_Lname
                    """
                    cursor.execute(query, (stat_user_id, stat_user_id, stat_user_id))
                    result = cursor.fetchall()
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                
                # Query o - Technician Job Performance
                elif query_id == 'o':
                    query_description = "Technician job performance in last three months"
                    tech_id = request.form.get('tech_id', '200003')
                    query = """
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
                        AND T.e_id = %s
                    GROUP BY 
                        T.e_id, T.e_name, T.e_surname
                    ORDER BY 
                        completed_jobs_last_3_months DESC
                    """
                    cursor.execute(query, (tech_id,))
                    result = cursor.fetchall()
                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                
                # Close database connection
                cursor.close()
                conn.close()
                
            except Exception as e:
                query_description = f"Error executing query: {str(e)}"
    
    return render_template('reports.html', 
                          result=result, 
                          columns=columns, 
                          query_description=query_description,
                          selected_query=selected_query)

@app.route('/')
def index():
    tables = get_tables()
    return render_template('index.html', tables=tables)

@app.route('/view/<table_name>')
def view_table(table_name):
    conn = get_connection()
    cursor = conn.cursor()
    columns = get_table_columns(table_name)
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    conn.close()
    return render_template('view.html', table_name=table_name, columns=columns, rows=rows)

@app.route('/insert/<table_name>', methods=['GET', 'POST'])
def insert(table_name):
    columns = get_table_columns(table_name)
    primary_key = get_primary_key_column(table_name)

# Remove the primary key from input fields if it is an automatically generated ID,
# excluding specific IDs like address_ID, user_id, Bill_ID, etc.
    if primary_key in columns and primary_key.lower().endswith('_id') and primary_key not in ['address_ID', 'user_id', 'Bill_ID', 'Local_IP_ID', 'Energy_meter_id','e_id','Ticket_ID','Job_id']:
        columns.remove(primary_key)

    def find_next_available_id(cursor, table_name, id_col):
        ranges = {
            'user_id': {
                'individual_customer': (100001, 150000),
                'commercial_customer': (150001, 200000),
                'individual_individual': (200001, 250000),
                'commercial_individual': (250001, 300000),
            },
            'e_id': {
                'technician': (200001, 300000),
                'manager': (300001, 400000),
                'worker': (400001, 500000),
            }
        }

        id_ranges = ranges.get(id_col, {})
        table_key = table_name.lower()

        if table_key not in id_ranges:
            raise Exception(f"ID range not defined for table '{table_name}' and column '{id_col}'.")

        min_id, max_id = id_ranges[table_key]

        cursor.execute(f"""
            SELECT {id_col} FROM {table_name} 
            WHERE {id_col} >= %s AND {id_col} < %s ORDER BY {id_col}
        """, (min_id, max_id))
        existing_ids = [row[0] for row in cursor.fetchall()]

        for candidate_id in range(min_id, max_id):
            if candidate_id not in existing_ids:
                return candidate_id

        raise Exception(f"No available {id_col} in range for table {table_name}.")



    def generate_unique_bill_id(cursor, table_name):
        while True:
            bill_id = str(random.randint(10000000, 99999999))
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE Bill_ID = %s", (bill_id,))
            if cursor.fetchone()[0] == 0:
                return bill_id

    def generate_unique_energy_meter_id(cursor):
        min_id = 10000000
        max_id = 99999999
        cursor.execute("SELECT energy_meter_id FROM Energy_Meter WHERE energy_meter_id BETWEEN %s AND %s", (min_id, max_id))
        used_ids = set(row[0] for row in cursor.fetchall())
        for _ in range(1000):
            candidate_id = random.randint(min_id, max_id)
            if candidate_id not in used_ids:
                return candidate_id
        raise Exception("No available energy_meter_id found.")

    def generate_unique_local_ip_id(cursor):
        min_id = 300101
        max_id = 400099
        cursor.execute("SELECT Local_IP_ID FROM Communication WHERE Local_IP_ID BETWEEN %s AND %s ORDER BY Local_IP_ID", (min_id, max_id))
        used_ids = [row[0] for row in cursor.fetchall()]
        for candidate_id in range(min_id, max_id + 1):
            if candidate_id not in used_ids:
                return candidate_id
        raise Exception("No available Local_IP_ID in range.")
    
    def find_next_ticket_id(cursor):
        min_id = 100001
        max_id = 130000
        cursor.execute("SELECT Ticket_ID FROM Ticket WHERE Ticket_ID BETWEEN %s AND %s ORDER BY Ticket_ID", (min_id, max_id))
        used_ids = [row[0] for row in cursor.fetchall()]
        for candidate_id in range(min_id, max_id + 1):
            if candidate_id not in used_ids:
                return candidate_id
        raise Exception("No available Ticket_ID in the range 100000-130000.")

    def get_random_worker_eid(cursor):
        cursor.execute("SELECT e_id FROM Worker WHERE e_id BETWEEN 400001 AND 500000")
        worker_ids = [row[0] for row in cursor.fetchall()]
        if not worker_ids:
            raise Exception("No workers found in employee table.")
        return random.choice(worker_ids)


    if request.method == 'POST':
        try:
            conn = get_connection()
            cursor = conn.cursor()

            form_data = request.form.to_dict()

            # Generation of address_ID
            if table_name.lower() == 'address':
                city_name = form_data.get('city')
                city_code = get_city_code(city_name)
                cursor.execute("SELECT address_ID FROM Address WHERE address_ID LIKE %s ORDER BY address_ID", (city_code + '%',))
                existing_ids = [row[0] for row in cursor.fetchall()]
                existing_serials = sorted([int(aid[2:]) for aid in existing_ids])
                next_serial = 1
                for serial in existing_serials:
                    if serial != next_serial:
                        break
                    next_serial += 1
                address_id_serial = str(next_serial).zfill(4)
                form_data['address_ID'] = city_code + address_id_serial

            # Check for user_id or e_id and automatic generation
            if 'user_id' in columns:
                user_id_input = request.form.get('user_id')
                if user_id_input and user_id_input.strip().isdigit():
                    form_data['user_id'] = int(user_id_input.strip())
                else:
                    form_data['user_id'] = find_next_available_id(cursor, table_name, 'user_id')

            # e_id: use manually provided value if available; otherwise, generate automatically
            if 'e_id' in columns:
                if table_name.lower() == 'ticket':
                    form_data['e_id'] = get_random_worker_eid(cursor)
                else:
                    e_id_input = request.form.get('e_id')
                    if e_id_input and e_id_input.strip().isdigit():
                        form_data['e_id'] = int(e_id_input.strip())
                    else:
                        form_data['e_id'] = find_next_available_id(cursor, table_name, 'e_id')
            
            # Generate Bill_ID if it exists in columns and is not provided in form data
            if 'Bill_ID' in columns and 'Bill_ID' not in form_data:
                form_data['Bill_ID'] = generate_unique_bill_id(cursor, table_name)

            # Generate Local_IP_ID if it exists in columns and is not provided in form data
            if 'Local_IP_ID' in columns and 'Local_IP_ID' not in form_data:
                form_data['Local_IP_ID'] = generate_unique_local_ip_id(cursor)

            # Generate Energy_meter_id if it exists in columns and is not provided in form data
            if 'Energy_meter_id' in columns and 'Energy_meter_id' not in form_data:
                form_data['Energy_meter_id'] = generate_unique_energy_meter_id(cursor)
            
            # For the 'ticket' table, automatically generate Ticket_ID and assign a random worker e_id
            if table_name.lower() == 'ticket':
                form_data['Ticket_ID'] = find_next_ticket_id(cursor)
                form_data['e_id'] = get_random_worker_eid(cursor)

            # For the 'job' table, generate a unique Job_id within a specified range
            if table_name.lower() == 'job':
                
                cursor.execute("SELECT Job_id FROM Job ORDER BY Job_id ASC")
                existing_ids = [row[0] for row in cursor.fetchall()]
                job_id = next((i for i in range(200000, 300001) if i not in existing_ids), None)
                if job_id is None:
                    flash("Uygun Job_id bulunamadı.", "error")
                    return redirect(request.url)
                form_data['Job_id'] = job_id

                # For the 'job' table, fetch Urgency_Type and description from the related Ticket using T_ID
                t_id = int(form_data.get('T_ID'))
                cursor.execute("SELECT Urgency_Type, description FROM Ticket WHERE Ticket_ID = %s", (t_id,))
                ticket_data = cursor.fetchone()
                if not ticket_data:
                    flash("Geçerli bir Ticket ID giriniz.", "error")
                    return redirect(request.url)
                urgency_type, description = ticket_data
                form_data['Urgency_Type'] = urgency_type
                form_data['description'] = description

                # Convert 'Report_date' string to a date object
                # Convert 'Est_Job_time' string to a time object
                form_data['Report_date'] = datetime.strptime(form_data.get('Report_date'), "%Y-%m-%d").date()
                form_data['Est_Job_time'] = datetime.strptime(form_data.get('Est_Job_time'), "%H:%M").time()

                # Convert 'completion_date' string to a date object if provided, otherwise set as None
                completion_str = form_data.get('completion_date')
                form_data['completion_date'] = datetime.strptime(completion_str, "%Y-%m-%d").date() if completion_str else None


            # Column and value list for the insert operation
            values = [form_data.get(col, None) for col in columns]
            placeholders = ", ".join(["%s"] * len(columns))
            cols = ", ".join(columns)

            query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
            cursor.execute(query, values)
            conn.commit()
            conn.close()

            flash(f"{table_name} Record successfully added", "success")
            return redirect(url_for('view_table', table_name=table_name))

        except Exception as e:
            flash(f"Hata: {str(e)}", "error")

    return render_template('insert.html', table_name=table_name, columns=columns)

def get_city_code(city_name):
    # We map the city name to its corresponding city code
    city_codes = {
        'Lefkosa': '01',
        'Girne': '02',
        'Gazimagusa': '03',
        'Guzelyurt': '04',
        'Iskele': '05',
        'Lefke': '06'
    }
    return city_codes.get(city_name, '00')  # Returns '00' if there is no valid city name provided

@app.route('/update/<table_name>/<primary_key>', methods=['GET', 'POST'])
def update(table_name, primary_key):
    conn = get_connection()
    cursor = conn.cursor()
    primary_column = get_primary_key_column(table_name)
    columns = get_table_columns(table_name)
    '''Insert what you don't want to see in update table'''
    hidden_columns = ['Bill_ID', 'address_ID', 'e_ID', 'Local_IP_ID','e_id','Ticket_ID','Job_id','Energy_meter_id']

    if request.method == 'POST':
        try:
            updates = []
            values = []

            for col in columns:
                if col != primary_column and col not in hidden_columns:
                    if col == 'Communication_Type':
                        selected_types = request.form.getlist('communication_types')
                        value = ",".join(selected_types)
                        updates.append(f"{col} = %s")
                        values.append(value)
                    elif col in request.form:
                        val = request.form[col]

                        # Here, we convert only if the value is 'None' or empty to None
                        if val.strip().lower() == 'none' or val.strip() == '':
                            val = None

                        updates.append(f"{col} = %s")
                        values.append(val)

            set_clause = ", ".join(updates)
            values.append(primary_key)
            query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_column} = %s"
            cursor.execute(query, values)
            conn.commit()
            flash(f"Record in {table_name} updated successfully!", "success")
            return redirect(url_for('view_table', table_name=table_name))

        except Exception as e:
            flash(f"Error: {str(e)}", "error")


    cursor.execute(f"SELECT * FROM {table_name} WHERE {primary_column} = %s", (primary_key,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        flash("Record not found", "error")
        return redirect(url_for('view_table', table_name=table_name))

    record = dict(zip(columns, row))
    return render_template('update.html', table_name=table_name, record=record, columns=columns, hidden_columns=hidden_columns)

@app.route('/delete/<table_name>/<primary_key>')
def delete(table_name, primary_key):
    primary_column = get_primary_key_column(table_name)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE {primary_column} = %s", (primary_key,))
        conn.commit()
        conn.close()
        flash(f"Record deleted from {table_name} successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
    return redirect(url_for('view_table', table_name=table_name))

@app.route('/query', methods=['GET', 'POST'])
def custom_query():
    result = None
    columns = []
    error = None
    if request.method == 'POST':
        query = request.form['query']
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                if result:
                    columns = [desc[0] for desc in cursor.description]
            else:
                conn.commit()
                flash("Query executed successfully!", "success")
            conn.close()
        except Exception as e:
            error = str(e)
    return render_template('query.html', result=result, columns=columns, error=error)

if __name__ == '__main__':
    try:
        conn = get_connection()
        conn.close()
    except Exception as e:
        print("Could not connect to the database. Error:", e)
    app.run(debug=True)
