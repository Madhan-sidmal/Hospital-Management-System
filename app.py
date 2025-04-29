from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import get_db_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'madhan' and password == 'madhan@g15':
            session['user'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid Credentials!')
    return render_template('login.html')

# Home Page
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

# Patients
@app.route('/patients')
def patients():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM patients')
    patients = cursor.fetchall()
    connection.close()
    return render_template('patients.html', patients=patients)

# Add Patient
@app.route('/add_patient', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    contact = request.form['contact']
    address = request.form['address']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO patients (name, age, gender, contact, address) VALUES (%s, %s, %s, %s, %s)',
                   (name, age, gender, contact, address))
    connection.commit()
    connection.close()
    flash('New patient added successfully!')
    return redirect(url_for('patients'))

# Doctors
@app.route('/doctors')
def doctors():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM doctors')
    doctors = cursor.fetchall()
    connection.close()
    return render_template('doctors.html', doctors=doctors)

# Add Doctor
@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    name = request.form['name']
    specialization = request.form['specialization']
    contact = request.form['contact']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO doctors (name, specialization, contact) VALUES (%s, %s, %s)',
                   (name, specialization, contact))
    connection.commit()
    connection.close()
    flash('New doctor added successfully!')
    return redirect(url_for('doctors'))

# Appointments
@app.route('/appointments')
def appointments():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('''
        SELECT a.id, p.name as patient_name, d.name as doctor_name, a.appointment_date
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
    ''')
    appointments = cursor.fetchall()
    connection.close()
    return render_template('appointments.html', appointments=appointments)

# Add Appointment
@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    patient_id = request.form['patient_id']
    doctor_id = request.form['doctor_id']
    appointment_date = request.form['appointment_date']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO appointments (patient_id, doctor_id, appointment_date) VALUES (%s, %s, %s)',
                   (patient_id, doctor_id, appointment_date))
    connection.commit()
    connection.close()
    flash('Appointment added successfully!')
    return redirect(url_for('appointments'))

# Billing
@app.route('/billing')
def billing():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute('''
        SELECT b.id, p.name as patient_name, 
               b.total_amount, 
               b.paid_amount, 
               b.balance
        FROM billing b
        JOIN patients p ON b.patient_id = p.id
    ''')
    billing = cursor.fetchall()
    
    cursor.execute('SELECT id, name FROM patients')
    patients = cursor.fetchall()
    cursor.execute('SELECT id, name, price FROM medicines')
    medicines = cursor.fetchall()
    
    connection.close()
    return render_template('billing.html', billing=billing, patients=patients, medicines=medicines)

# Add Bill
@app.route('/add_bill', methods=['POST'])
def add_bill():
    patient_id = request.form['patient_id']
    medicine_ids = request.form.getlist('medicine_id')
    quantities = request.form.getlist('quantity')
    paid_amount = float(request.form['paid_amount'])

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    total_amount = 0

    try:
        for medicine_id, qty in zip(medicine_ids, quantities):
            cursor.execute('SELECT price, quantity FROM medicines WHERE id = %s', (medicine_id,))
            medicine = cursor.fetchone()
            if not medicine:
                flash(f'Medicine ID {medicine_id} not found!')
                return redirect(url_for('billing'))
            if medicine['quantity'] < int(qty):
                flash(f'Not enough stock for Medicine ID {medicine_id}!')
                return redirect(url_for('billing'))
            
            total_amount += medicine['price'] * int(qty)
            new_quantity = medicine['quantity'] - int(qty)
            cursor.execute('UPDATE medicines SET quantity = %s WHERE id = %s', (new_quantity, medicine_id))
        
        balance_amount = total_amount - paid_amount
        cursor.execute('''
            INSERT INTO billing (patient_id, total_amount, paid_amount, balance)
            VALUES (%s, %s, %s, %s)
        ''', (patient_id, total_amount, paid_amount, balance_amount))
        
        connection.commit()
        flash('Bill added successfully!')
    except Exception as e:
        connection.rollback()
        flash(f'Error: {str(e)}')
    finally:
        connection.close()
    
    return redirect(url_for('billing'))

# Medicines
@app.route('/medicines')
def medicines():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM medicines')
    medicines = cursor.fetchall()
    connection.close()
    return render_template('medicines.html', medicines=medicines)

# Add Medicine
@app.route('/add_medicine', methods=['POST'])
def add_medicine():
    name = request.form['name']
    quantity = request.form['quantity']
    price = request.form['price']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO medicines (name, quantity, price) VALUES (%s, %s, %s)',
                   (name, quantity, price))
    connection.commit()
    connection.close()
    flash('Medicine added successfully!')
    return redirect(url_for('medicines'))

# Reports
@app.route('/reports')
def reports():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute('''
        SELECT a.id, p.name as patient_name, d.name as doctor_name, a.appointment_date
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
    ''')
    appointments = cursor.fetchall()

    cursor.execute('''
        SELECT b.id, p.name as patient_name, 
               b.total_amount, 
               b.paid_amount, 
               b.balance
        FROM billing b
        JOIN patients p ON b.patient_id = p.id
    ''')
    billing = cursor.fetchall()

    connection.close()
    return render_template('reports.html', appointments=appointments, billing=billing)

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)