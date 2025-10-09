import sqlite3
from typing import List, Dict, Any


def get_user_transactions(user_identifier: str) -> List[Dict[str, Any]]:
    """
    Retrieve all transactions for a specific user by ID or partial name.
    
    Args:
        user_identifier (str): The ID or partial name of the user to retrieve transactions for
        
    Returns:
        List[Dict[str, Any]]: List of dictionaries containing transaction data
        Each dictionary contains: ID, UserID, Type, Amount, Date, Counterparty, 
        AccountNumber, and Description
    """
    try:
        conn = sqlite3.connect("customer_data.db")
        cursor = conn.cursor()

        print("Connecting to the database to retrieve user transactions...")
        print(f"User Identifier: {user_identifier}")
        print("Executing query to fetch transactions...")
        
        # Query to get all transactions for the specified user
        query = """
        SELECT ut.ID, ut.UserID, ut.Type, ut.Amount, ut.Date, ut.Counterparty, ut.AccountNumber, ut.Description 
        FROM user_transactions ut
        JOIN user u ON ut.UserID = u.UserID
        WHERE ut.UserID = ? OR u.Name LIKE ?
        ORDER BY ut.Date
        """
        
        # Add wildcards for partial name matching
        name_pattern = f"%{user_identifier}%"
        cursor.execute(query, (user_identifier, name_pattern))
        transactions = cursor.fetchall()
        
        # Convert the results to a list of dictionaries
        result = []
        for transaction in transactions:
            result.append({
                'ID': transaction[0],
                'UserID': transaction[1],
                'Type': transaction[2],
                'Amount': transaction[3],
                'Date': transaction[4],
                'Counterparty': transaction[5],
                'AccountNumber': transaction[6],
                'Description': transaction[7]
            })
        
        return result
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_basic_account_information(user_identifier: str) -> List[Dict[str, Any]]:
    """
    Retrieve basic account information for a specific user by ID or partial name.
    
    Args:
        user_identifier (str): The ID or partial name of the user to retrieve information for
        
    Returns:
        List[Dict[str, Any]]: List of dictionaries containing user basic information
        Each dictionary contains: UserID, Name, Address, AccountBalance, and AccountTypes
    """
    try:
        conn = sqlite3.connect("customer_data.db")
        cursor = conn.cursor()
        
        # Query to get basic account information for the specified user
        query = """
        SELECT UserID, Name, Address, AccountBalance, AccountTypes 
        FROM user
        WHERE UserID = ? OR Name LIKE ?
        """
        
        # Add wildcards for partial name matching
        name_pattern = f"%{user_identifier}%"
        cursor.execute(query, (user_identifier, name_pattern))
        users = cursor.fetchall()
        
        # Convert the results to a list of dictionaries
        result = []
        for user in users:
            result.append({
                'UserID': user[0],
                'Name': user[1],
                'Address': user[2],
                'AccountBalance': user[3],
                'AccountTypes': user[4]
            })
        
        return result
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_credit_card_details(user_identifier: str) -> List[Dict[str, Any]]:
    """
    Retrieve credit card details for a specific user by ID or partial name.
    
    Args:
        user_identifier (str): The ID or partial name of the user to retrieve credit card details for
        
    Returns:
        List[Dict[str, Any]]: List of dictionaries containing credit card data
        Each dictionary contains: ID, UserID, CreditCard, Last4Numbers, CreditLimit, 
        AvailableLimit, and AnnualFee
    """
    try:
        conn = sqlite3.connect("customer_data.db")
        cursor = conn.cursor()

        print("Connecting to the database to retrieve credit card details...")
        print(f"User Identifier: {user_identifier}")
        print("Executing query to fetch credit card details...")
        
        # Query to get all credit cards for the specified user
        query = """
        SELECT cc.ID, cc.UserID, cc.CreditCard, cc.Last4Numbers, cc.CreditLimit, cc.AvailableLimit, cc.AnnualFee 
        FROM credit_card_details cc
        JOIN user u ON cc.UserID = u.UserID
        WHERE cc.UserID = ? OR u.Name LIKE ?
        ORDER BY cc.ID
        """
        
        print("Query:")
        print(query)
        
        # Add wildcards for partial name matching
        name_pattern = f"%{user_identifier}%"
        cursor.execute(query, (user_identifier, name_pattern))
        credit_cards = cursor.fetchall()
        
        print("Credit Cards:")
        print(credit_cards)
        
        # Convert the results to a list of dictionaries
        result = []
        for card in credit_cards:
            result.append({
                'ID': card[0],
                'UserID': card[1],
                'CreditCard': card[2],
                'Last4Numbers': card[3],
                'CreditLimit': card[4],
                'AvailableLimit': card[5],
                'AnnualFee': card[6]
            })
        
        print("Result:")    
        print(result)
        
        return result
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_credit_card_late_fee_waive_off(user_identifier: str, last_4_digits: str) -> List[Dict[str, Any]]:
    """
    Retrieve credit card late fee waive off details for a specific user by ID or partial name,
    optionally filtered by credit card last 4 digits.
    
    Args:
        user_identifier (str): The ID or partial name of the user to retrieve waive off details for
        last_4_digits (str, optional): The last 4 digits of the credit card to filter by
        
    Returns:
        List[Dict[str, Any]]: List of dictionaries containing late fee waive off data
        Each dictionary contains: ID, UserID, Last4Numbers, CreditCardID, WaveOffMonth, 
        WaveOffYear, and Reason
    """
    try:
        conn = sqlite3.connect("customer_data.db")
        cursor = conn.cursor()

        print("Connecting to the database to retrieve credit card late fee waive off details...")
        print(f"User Identifier: {user_identifier}")
        if last_4_digits:
            print(f"Credit Card Last 4 Digits: {last_4_digits}")
        print("Executing query to fetch late fee waive off details...")
        
        # Query to get late fee waive offs for the specified user and optionally credit card
        if last_4_digits:
            query = """
            SELECT lfw.ID, lfw.UserID, lfw.Last4Numbers, lfw.CreditCardID, lfw.WaveOffMonth, lfw.WaveOffYear, lfw.Reason 
            FROM credit_card_late_fee_wave_off lfw
            JOIN user u ON lfw.UserID = u.UserID
            WHERE (lfw.UserID = ? OR u.Name LIKE ?) AND lfw.Last4Numbers = ?
            ORDER BY lfw.WaveOffYear DESC, lfw.WaveOffMonth DESC
            """
            cursor.execute(query, (user_identifier, f"%{user_identifier}%", last_4_digits))
        else:
            query = """
            SELECT lfw.ID, lfw.UserID, lfw.Last4Numbers, lfw.CreditCardID, lfw.WaveOffMonth, lfw.WaveOffYear, lfw.Reason 
            FROM credit_card_late_fee_wave_off lfw
            JOIN user u ON lfw.UserID = u.UserID
            WHERE lfw.UserID = ? OR u.Name LIKE ?
            ORDER BY lfw.WaveOffYear DESC, lfw.WaveOffMonth DESC
            """
            cursor.execute(query, (user_identifier, f"%{user_identifier}%"))
        
        waive_offs = cursor.fetchall()
        
        # Convert the results to a list of dictionaries
        result = []
        for waive_off in waive_offs:
            result.append({
                'ID': waive_off[0],
                'UserID': waive_off[1],
                'Last4Numbers': waive_off[2],
                'CreditCardID': waive_off[3],
                'WaveOffMonth': waive_off[4],
                'WaveOffYear': waive_off[5],
                'Reason': waive_off[6]
            })
        
        return result
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            conn.close()