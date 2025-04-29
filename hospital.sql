-- Create database
CREATE DATABASE hospital_management1;

-- Use the database
USE hospital_management1;

-- Create patients table
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    contact VARCHAR(15),
    address TEXT
);

-- Create doctors table
CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    specialization VARCHAR(100),
    contact VARCHAR(15)
);

-- Create appointments table
CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

-- Create medicines table
CREATE TABLE medicines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    quantity INT,
    price DECIMAL(10, 2)
);

-- Create billing table (updated structure)
CREATE TABLE billing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    total_amount DECIMAL(10, 2),   -- Total bill amount
    paid_amount DECIMAL(10, 2),    -- Amount paid by patient
    balance DECIMAL(10, 2),        -- Remaining balance (total - paid)
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

-- Table to track medicines used in a bill
CREATE TABLE billing_medicines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    billing_id INT,
    medicine_id INT,
    quantity INT,
    FOREIGN KEY (billing_id) REFERENCES billing(id),
    FOREIGN KEY (medicine_id) REFERENCES medicines(id)
);
DESCRIBE billing;