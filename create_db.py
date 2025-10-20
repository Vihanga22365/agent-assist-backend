import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("customer_data.db")
cursor = conn.cursor()

# Drop old tables
cursor.executescript("""
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_interactions;
DROP TABLE IF EXISTS user_transactions;
DROP TABLE IF EXISTS credit_card_details;
DROP TABLE IF EXISTS credit_card_late_fee_wave_off;
DROP TABLE IF EXISTS credit_card_late_fee_payment;
""")

# Create new tables
cursor.executescript("""
CREATE TABLE user (
    UserID TEXT PRIMARY KEY,
    Name TEXT,
    Address TEXT,
    AccountBalance REAL,
    AccountTypes TEXT
);

CREATE TABLE user_interactions (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID TEXT,
    Channel TEXT,
    Interaction TEXT,
    FOREIGN KEY (UserID) REFERENCES user(UserID)
);

CREATE TABLE user_transactions (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID TEXT,
    Type TEXT,
    Amount REAL,
    Date TEXT,
    Counterparty TEXT,
    AccountNumber TEXT,
    Description TEXT,
    FOREIGN KEY (UserID) REFERENCES user(UserID)
);

CREATE TABLE credit_card_details (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID TEXT,
    CreditCard TEXT,
    Last4Numbers TEXT,
    CreditLimit REAL,
    AvailableLimit REAL,
    AnnualFee REAL,
    FOREIGN KEY (UserID) REFERENCES user(UserID)
);

CREATE TABLE credit_card_late_fee_wave_off (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID TEXT,
    Last4Numbers TEXT,
    CreditCardID INTEGER,
    WaveOffMonth INTEGER,
    WaveOffYear INTEGER,
    Reason TEXT,
    FOREIGN KEY (UserID) REFERENCES user(UserID),
    FOREIGN KEY (CreditCardID) REFERENCES credit_card_details(ID)
);

CREATE TABLE credit_card_late_fee_payment (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID TEXT,
    CreditCardID TEXT,
    latePaymentMonth INTEGER,
    latePaymentYear INTEGER,
    latePaymentFee REAL,
    minimumPayment REAL,
    dueDate TEXT,
    FOREIGN KEY (UserID) REFERENCES user(UserID)
);
""")

# Insert Users
cursor.execute("""INSERT INTO user VALUES ('U001', 'Chathusha Wijenayake', '922 Michelle Junctions Apt. 072, Murrayton, NY', 41587.72, 'Savings, Credit Card')""")

# Insert Interactions
# === User U001 Interactions (7 rows) ===
cursor.execute("""INSERT INTO user_interactions (UserID, Channel, Interaction) VALUES ('U001', 'Mobile App', 'Searched for travel credit cards')""")
cursor.execute("""INSERT INTO user_interactions (UserID, Channel, Interaction) VALUES ('U001', 'Mobile App', 'Viewed Chase Sapphire card benefits')""")
cursor.execute("""INSERT INTO user_interactions (UserID, Channel, Interaction) VALUES ('U001', 'Mobile App', 'Compared credit card rewards')""")
cursor.execute("""INSERT INTO user_interactions (UserID, Channel, Interaction) VALUES ('U001', 'Agent', 'Spoke with agent about credit card options')""")
cursor.execute("""INSERT INTO user_interactions (UserID, Channel, Interaction) VALUES ('U001', 'Agent', 'Discussed travel benefits of credit cards')""")
cursor.execute("""INSERT INTO user_interactions (UserID, Channel, Interaction) VALUES ('U001', 'Mobile App', 'Checked credit card application status')""")
cursor.execute("""INSERT INTO user_interactions (UserID, Channel, Interaction) VALUES ('U001', 'Mobile App', 'Viewed credit card terms and conditions')""")


# Insert transactions (no loops, each query separately written)

# === Transactions for User U001 (35 rows for 6 months) ===
# Month 1 - December 2024
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'CR', 2000.00, '2024-12-05', 'Payroll', '1111222233334444', 'Monthly salary')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 120.00, '2024-12-06', 'Netflix', '1111222233335555', 'Streaming subscription')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 85.00, '2024-12-10', 'Amazon', '1111222233335555', 'Online shopping')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 1500.00, '2024-12-15', 'NYU', '1111222233334444', 'Monthly tuition payment')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 45.00, '2024-12-20', 'Spotify', '1111222233335555', 'Music subscription')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'CR', 500.00, '2024-12-25', 'Freelance', '1111222233334444', 'Part-time work')""")

# Month 2 - January 2025
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'CR', 2000.00, '2025-01-05', 'Payroll', '1111222233334444', 'Monthly salary')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 120.00, '2025-01-06', 'Netflix', '1111222233335555', 'Streaming subscription')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 1500.00, '2025-01-15', 'NYU', '1111222233334444', 'Monthly tuition payment')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 95.00, '2025-01-18', 'Walmart', '1111222233335555', 'Groceries')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 200.00, '2025-01-20', 'Delta Airlines', '1111222233335555', 'Flight booking')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'CR', 300.00, '2025-01-25', 'Freelance', '1111222233334444', 'Project completion')""")

# Month 3 - February 2025
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'CR', 2000.00, '2025-02-05', 'Payroll', '1111222233334444', 'Monthly salary')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 120.00, '2025-02-06', 'Netflix', '1111222233335555', 'Streaming subscription')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 1500.00, '2025-02-15', 'NYU', '1111222233334444', 'Monthly tuition payment')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 75.00, '2025-02-22', 'Target', '1111222233335555', 'Household items')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 150.00, '2025-02-25', 'Marriott', '1111222233335555', 'Hotel booking')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'CR', 400.00, '2025-02-28', 'Freelance', '1111222233334444', 'Extra project')""")

# Month 4 - March 2025
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'CR', 2000.00, '2025-03-05', 'Payroll', '1111222233334444', 'Monthly salary')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 120.00, '2025-03-06', 'Netflix', '1111222233335555', 'Streaming subscription')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 1500.00, '2025-03-15', 'NYU', '1111222233334444', 'Monthly tuition payment')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 110.00, '2025-03-25', 'Best Buy', '1111222233335555', 'Electronics')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 180.00, '2025-03-28', 'United Airlines', '1111222233335555', 'Flight booking')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'CR', 350.00, '2025-03-30', 'Freelance', '1111222233334444', 'Consulting work')""")

# Month 5 - April 2025
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'CR', 2000.00, '2025-04-05', 'Payroll', '1111222233334444', 'Monthly salary')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 120.00, '2025-04-06', 'Netflix', '1111222233335555', 'Streaming subscription')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 1500.00, '2025-04-15', 'NYU', '1111222233334444', 'Monthly tuition payment')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 150.00, '2025-04-20', 'Amazon', '1111222233335555', 'Holiday shopping')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 200.00, '2025-04-25', 'Hilton', '1111222233335555', 'Hotel booking')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'CR', 450.00, '2025-04-28', 'Freelance', '1111222233334444', 'Project completion')""")

# Month 6 - May 2025
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'CR', 2000.00, '2025-05-05', 'Payroll', '1111222233334444', 'Monthly salary')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 120.00, '2025-05-06', 'Netflix', '1111222233335555', 'Streaming subscription')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 1500.00, '2025-05-15', 'NYU', '1111222233334444', 'Monthly tuition payment')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 90.00, '2025-05-25', 'Walmart', '1111222233335555', 'Monthly groceries')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'DR', 250.00, '2025-05-28', 'American Airlines', '1111222233335555', 'Flight booking')""")
cursor.execute("""INSERT INTO user_transactions (UserID, Type, Amount, Date, Counterparty, AccountNumber, Description) 
VALUES ('U001', 'CR', 500.00, '2025-05-30', 'Freelance', '1111222233334444', 'Year-end project')""")

# Insert Credit Card Details
# === User U001 Credit Cards (2 cards) ===
cursor.execute("""INSERT INTO credit_card_details (UserID, CreditCard, Last4Numbers, CreditLimit, AvailableLimit, AnnualFee) 
VALUES ('U001', 'Chase Sapphire Preferred', '1234', 15000.00, 12500.00, 95.00)""")
cursor.execute("""INSERT INTO credit_card_details (UserID, CreditCard, Last4Numbers, CreditLimit, AvailableLimit, AnnualFee) 
VALUES ('U001', 'Chase Freedom Unlimited', '5678', 8000.00, 7200.00, 0.00)""")


# Insert Credit Card Late Fee Wave Off
# === User U001 Wave Offs (1 wave off) ===
cursor.execute("""INSERT INTO credit_card_late_fee_wave_off (UserID, Last4Numbers, CreditCardID, WaveOffMonth, WaveOffYear, Reason) 
VALUES ('U001', '1234', 1, 3, 2025, 'Customer loyalty program benefit')""")


# Insert Credit Card Late Fee Payments
# === User U001 Late Payments (2 payments) ===
cursor.execute("""INSERT INTO credit_card_late_fee_payment (UserID, CreditCardID, latePaymentMonth, latePaymentYear, latePaymentFee, minimumPayment, dueDate) 
VALUES ('U001', '1234', 3, 2025, 400.00, 150.00, '2025-03-20')""")
cursor.execute("""INSERT INTO credit_card_late_fee_payment (UserID, CreditCardID, latePaymentMonth, latePaymentYear, latePaymentFee, minimumPayment, dueDate) 
VALUES ('U001', '1234', 10, 2025, 375.00, 140.00, '2025-10-20')""")

# Finalize DB
conn.commit()
conn.close()
print("Database 'chase_data.db' created successfully with full dataset.")
