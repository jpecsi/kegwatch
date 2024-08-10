'''
Server Support Functions
[WatchMy.Beer Server]
---------------------
Created: 10 AUG 2024
Updated: 10 AUG 2024
Author: Joe Pecsi | Sideline Data, LLC.
'''

# ===== Libraries ===== #
import mysql.connector
import os, re
import time, datetime
from dateutil.parser import parse
from datetime import datetime
from uuid import UUID
from decimal import *
# ===================== #


# ===== Database Setup ===== #
db_host = os.getenv("DB_HOST", "<blank>")   # Database Host
db_user = os.getenv("DB_USER", "<blank>")   # Database User
db_pass = os.getenv("DB_PASS", "<blank>")   # Database Password
db_name = os.getenv("DB_NAME", "<blank>")   # Database Name
db_port = os.getenv("DB_PORT", "<blank>")   # Database Port
logging = os.getenv("CONSOLE_LOG")          # Logging to the console (True/False)
# ========================== #


# ===== Support Functions ===== #
# Formatted logging to the console (if enabeld)
def log(t,m):
    # Make sure console logging is enabled...
    if logging:
        if t == 0:
            # Failure
            print(str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')) + " [ERROR] " + m)

        elif t == 1:
            # Success
            print(str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')) + " [STATUS] " + m)


# Database queries
def db_query(q,v,m):
    # Connect to the datbase
    db = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_pass,
            database=db_name
        )

    # Open a cursor
    cursor = db.cursor()

    # Execute request (check for values)
    if v:
        cursor.execute(q,v)
    else:
        cursor.execute(q)

    # If query is a SELECT...
    if m == 0:
        # Get the results
        results = cursor.fetchall()
        
        # Clear the cursor and close connection
        cursor.close()
        db.close()
        
        # Return results
        return results

    # If query is an INSERT/UPDATE...
    elif m == 1:
        # Commit the changes and close the connection
        db.commit()
        cursor.close()
        db.close()

        # Returns the number of rows modified in the transaction
        return cursor.rowcount


# Data Validation
def validate(d):
    # Variables
    validated_data = {}         # Holds validated data
    failed_validation = 0       # Couner for failed data input

    # Check all of the data and make sure it is clean
    if d.get('keg_id'):
        try:
            uuid_obj = UUID(d.get('keg_id'), version=4)
            validated_data['keg_id'] = d.get('keg_id')
        except Exception:
            failed_validation += 1
            log(0,'Data Validation Failed: keg_id')

    if d.get('keg_name'):
        if (re.fullmatch(re.compile(r"[0-9a-zA-Z\s']+"),d.get('keg_name'))):
            validated_data['keg_name'] = d.get('keg_name')
        else:
            failed_validation += 1
            log(0,'Data Validation Failed: keg_name')
            
    if d.get('keg_size'):
        try:
            float(d.get('keg_size'))
            validated_data['keg_size'] = d.get('keg_size')
        except Exception:
            failed_validation += 1
            log(0,'Data Validation Failed: keg_size')

    if d.get('keg_abv'):
        try:
            float(d.get('keg_abv'))
            validated_data['keg_abv'] = d.get('keg_abv')
        except Exception:
            failed_validation += 1
            log(0,'Data Validation Failed: keg_abv')

    if d.get('keg_tap'):
        try:
            int(d.get('keg_tap'))
            validated_data['keg_tap'] = d.get('keg_tap')
        except Exception:
            failed_validation += 1
            log(0,'Data Validation Failed: keg_tap')

    if d.get('keg_start'):
        try:
            parse(d.get('keg_start'))
            validated_data['keg_start'] = d.get('keg_start')
        except Exception:
            failed_validation += 1
            log(0,'Data Validation Failed: keg_start')

    if d.get('keg_end'):
        try:
            parse(d.get('keg_end'))
            validated_data['keg_end'] = d.get('keg_end')
        except Exception:
            failed_validation += 1
            log(0,'Data Validation Failed: keg_end')

    if d.get('keg_remain'):
        try:
            Decimal(d.get('keg_remain'))
            validated_data['keg_remain'] = d.get('keg_remain')
        except Exception:
            failed_validation += 1
            log(0,'Data Validation Failed: keg_remain')

    if d.get('keg_status'):
        try:
            int(d.get('keg_status'))
            validated_data['keg_status'] = d.get('keg_status')
        except Exception:
            failed_validation += 1
            log(0,'Data Validation Failed: keg_status')

    if d.get('pour_time'):
        try:
            parse(d.get('pour_time'))
            validated_data['pour_time'] = d.get('pour_time')
        except Exception:
            failed_validation += 1
            log(0,'Data Validation Failed: pour_time')

    if d.get('pour_size'):
        try:
            Decimal(d.get('pour_size'))
            if d.get('pour_size') > 9999:
                failed_validation += 1
                log(0,'Data Validation Failed: pour_size')
            else:
                validated_data['pour_size'] = round(d.get('pour_size'),4)
        except Exception:
            failed_validation += 1
            log(0,'Data Validation Failed: pour_size')

    if d.get('pour_user'):
        if (re.fullmatch(re.compile(r"[a-zA-Z\s']+"),d.get('pour_user'))):
            validated_data['pour_user'] = d.get('pour_user')
        else:
            failed_validation += 1
            log(0,'Data Validation Failed: pour_user')

    # Check to see if anything failed #
    if failed_validation == 0:
        log(1, 'All data passed validation')
        return validated_data
    else:
        return False
    
# ============================= #