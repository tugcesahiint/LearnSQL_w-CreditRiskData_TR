import sqlite3

conn = sqlite3.connect("bank_data.db")
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS defaults;
DROP TABLE IF EXISTS payments;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    income REAL,
    credit_score INTEGER,
    city TEXT,
    birth_year INTEGER,
    marital_status TEXT,
    job_title TEXT
);

CREATE TABLE loans (
    loan_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount REAL,
    interest_rate REAL,
    status TEXT,
    start_date TEXT,
    due_date TEXT,
    risk_level TEXT
);

CREATE TABLE defaults (
    default_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    loan_id INTEGER,
    default_date TEXT,
    reason TEXT
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    loan_id INTEGER,
    payment_date TEXT,
    amount_paid REAL,
    payment_method TEXT
);
""")

customers = [
    (1, 'Ahmet Yilmaz', 5000, 650, 'Istanbul', 1985, 'married', 'Engineer'),
    (2, 'Ayse Demir', 8000, 720, 'Ankara', 1990, 'single', 'Doctor'),
    (3, 'Can Kaya', 3000, 580, 'Izmir', 1995, 'single', 'Student'),
    (4, 'Fatma Sahin', 12000, 800, 'Bursa', 1980, 'married', 'Manager'),
    (5, 'Mehmet Acar', 2500, 540, 'Adana', 1975, 'married', 'Retired'),
    (6, 'Elif Öztürk', 7000, 600, 'Istanbul', 1988, 'single', 'Designer'),
    (7, 'Burak Günes', 9500, 720, 'Antalya', 1992, 'single', 'Lawyer'),
    (8, 'Zeynep Kiliç', 6800, 670, 'Ankara', 1984, 'married', 'Nurse'),
    (9, 'Mustafa Karaca', 4000, 590, 'Izmir', 1998, 'single', 'Technician'),
    (10, 'Duygu Eren', 5600, 650, 'Istanbul', 1991, 'single', 'Analyst'),
    (11, 'Kerem Polat', 11000, 780, 'Konya', 1983, 'married', 'Director'),
    (12, 'Selin Aydin', 3200, 610, 'Antalya', 1996, 'single', 'Freelancer'),
    (13, 'Okan Kurt', 4700, 570, 'Bursa', 1989, 'married', 'Technician'),
    (14, 'Nazli Aksoy', 8500, 750, 'Istanbul', 1986, 'single', 'Architect'),
    (15, 'Emre Sezer', 3900, 600, 'Ankara', 1994, 'single', 'Journalist'),
]

loans = [
    (1, 1, 10000, 18.5, 'paid', '2023-01-10', '2023-07-10', 'medium'),
    (2, 2, 15000, 22.0, 'unpaid', '2023-02-15', '2023-08-15', 'high'),
    (3, 3, 8000, 19.0, 'unpaid', '2023-03-20', '2023-09-20', 'high'),
    (4, 4, 5000, 12.0, 'paid', '2023-01-05', '2023-06-05', 'low'),
    (5, 5, 12000, 25.0, 'late', '2023-04-10', '2023-10-10', 'high'),
    (6, 6, 7000, 16.0, 'paid', '2023-03-01', '2023-09-01', 'medium'),
    (7, 7, 16000, 20.0, 'unpaid', '2023-05-15', '2023-11-15', 'medium'),
    (8, 8, 9000, 15.0, 'paid', '2023-06-01', '2023-12-01', 'medium'),
    (9, 9, 3000, 24.0, 'unpaid', '2023-07-10', '2024-01-10', 'high'),
    (10, 10, 6000, 13.0, 'paid', '2023-08-01', '2024-02-01', 'low'),
    (11, 11, 11000, 11.5, 'paid', '2022-12-01', '2023-06-01', 'low'),
    (12, 12, 4000, 21.0, 'late', '2023-09-01', '2024-03-01', 'medium'),
    (13, 13, 4500, 19.0, 'unpaid', '2023-10-01', '2024-04-01', 'high'),
    (14, 14, 13000, 12.5, 'paid', '2023-11-01', '2024-05-01', 'low'),
    (15, 15, 5000, 18.0, 'unpaid', '2024-01-01', '2024-07-01', 'medium'),
]

defaults = [
    (1, 2, 2, '2023-09-01', 'missed multiple payments'),
    (2, 3, 3, '2023-10-01', 'job loss'),
    (3, 5, 5, '2023-11-15', 'financial hardship'),
    (4, 13, 13, '2024-03-01', 'bankruptcy'),
]

payments = [
    (1, 1, '2023-02-10', 3000, 'bank'),
    (2, 1, '2023-04-10', 4000, 'bank'),
    (3, 1, '2023-06-10', 3000, 'cash'),
    (4, 4, '2023-02-05', 2500, 'mobile'),
    (5, 4, '2023-05-05', 2500, 'mobile'),
    (6, 6, '2023-04-01', 3500, 'cash'),
    (7, 6, '2023-08-01', 3500, 'cash'),
    (8, 10, '2023-09-01', 3000, 'bank'),
    (9, 10, '2024-01-01', 3000, 'bank'),
    (10, 11, '2023-03-01', 11000, 'bank'),
]

cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?);", customers)
cursor.executemany("INSERT INTO loans VALUES (?, ?, ?, ?, ?, ?, ?, ?);", loans)
cursor.executemany("INSERT INTO defaults VALUES (?, ?, ?, ?, ?);", defaults)
cursor.executemany("INSERT INTO payments VALUES (?, ?, ?, ?, ?);", payments)

conn.commit()
conn.close()

print("Veritabanı başarıyla oluşturuldu.")
