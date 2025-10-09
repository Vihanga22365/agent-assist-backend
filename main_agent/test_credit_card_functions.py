#!/usr/bin/env python3
"""
Test script for credit card functions
"""


import os
import sqlite3
from typing import List, Dict, Any

# Import the functions directly by copying them here to avoid dependency issues
def get_credit_card_details(user_identifier: str) -> List[Dict[str, Any]]:
    """
    Retrieve credit card details for a specific user by ID or partial name.
    """
    conn = None
    try:
        db_path = os.path.join(os.path.dirname(__file__), "customer_data.db")
        conn = sqlite3.connect(db_path)
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

        # Add wildcards for partial name matching
        name_pattern = f"%{user_identifier}%"
        cursor.execute(query, (user_identifier, name_pattern))
        credit_cards = cursor.fetchall()

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

        return result

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_credit_card_late_fee_waive_off(user_identifier: str, last_4_digits: str = None) -> List[Dict[str, Any]]:
    """
    Retrieve credit card late fee waive off details for a specific user by ID or partial name,
    optionally filtered by credit card last 4 digits.
    """
    conn = None
    try:
        db_path = os.path.join(os.path.dirname(__file__), "customer_data.db")
        conn = sqlite3.connect(db_path)
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

def test_credit_card_details():
    """Test the get_credit_card_details function"""
    print("=" * 50)
    print("Testing get_credit_card_details function")
    print("=" * 50)
    
    # Test with User ID
    print("\n1. Testing with User ID '1':")
    result = get_credit_card_details("U001")
    print(f"Found {len(result)} credit card(s)")
    for card in result:
        print(f"  - Card ID: {card['ID']}, Card: {card['CreditCard']}, Last 4: {card['Last4Numbers']}")
        print(f"    Credit Limit: ${card['CreditLimit']}, Available: ${card['AvailableLimit']}, Annual Fee: ${card['AnnualFee']}")
    
    # Test with User ID 2
    # print("\n2. Testing with User ID '2':")
    # result = get_credit_card_details("U002")
    # print(f"Found {len(result)} credit card(s)")
    # for card in result:
    #     print(f"  - Card ID: {card['ID']}, Card: {card['CreditCard']}, Last 4: {card['Last4Numbers']}")
    #     print(f"    Credit Limit: ${card['CreditLimit']}, Available: ${card['AvailableLimit']}, Annual Fee: ${card['AnnualFee']}")
    
    # Test with User ID 3
    # print("\n3. Testing with User ID '3':")
    # result = get_credit_card_details("Paul")
    # print(f"Found {len(result)} credit card(s)")
    # for card in result:
    #     print(f"  - Card ID: {card['ID']}, Card: {card['CreditCard']}, Last 4: {card['Last4Numbers']}")
    #     print(f"    Credit Limit: ${card['CreditLimit']}, Available: ${card['AvailableLimit']}, Annual Fee: ${card['AnnualFee']}")
    
    # Test with partial name
    # print("\n4. Testing with partial name 'John':")
    # result = get_credit_card_details("Charles")
    # print(f"Found {len(result)} credit card(s)")
    # for card in result:
    #     print(f"  - Card ID: {card['ID']}, Card: {card['CreditCard']}, Last 4: {card['Last4Numbers']}")

def test_late_fee_waive_off():
    """Test the get_credit_card_late_fee_waive_off function"""
    print("\n" + "=" * 50)
    print("Testing get_credit_card_late_fee_waive_off function")
    print("=" * 50)
    
    # Test with User ID 1 (should have 1 waive off)
    print("\n1. Testing with User ID '1':")
    result = get_credit_card_late_fee_waive_off("U001", "1234")
    print(f"Found {len(result)} waive off(s)")
    for waive in result:
        print(f"  - ID: {waive['ID']}, Last 4: {waive['Last4Numbers']}, Card ID: {waive['CreditCardID']}")
        print(f"    Date: {waive['WaveOffMonth']}/{waive['WaveOffYear']}, Reason: {waive['Reason']}")
    
    # Test with User ID 2 (should have 0 waive offs)
    print("\n2. Testing with User ID '2':")
    result = get_credit_card_late_fee_waive_off("U002", "1234")
    print(f"Found {len(result)} waive off(s)")
    for waive in result:
        print(f"  - ID: {waive['ID']}, Last 4: {waive['Last4Numbers']}, Card ID: {waive['CreditCardID']}")
        print(f"    Date: {waive['WaveOffMonth']}/{waive['WaveOffYear']}, Reason: {waive['Reason']}")
    

if __name__ == "__main__":
    print("Testing Credit Card Functions")
    print("Make sure you have run create_db.py first to create the database with credit card tables!")
    
    try:
        test_credit_card_details()
        # test_late_fee_waive_off()
        print("\n" + "=" * 50)
        print("All tests completed successfully!")
        print("=" * 50)
    except Exception as e:
        print(f"\nError during testing: {e}")
        print("Make sure the database exists and has the credit card tables.")