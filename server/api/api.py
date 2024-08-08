'''
WatchMy.Beer Server
Version: 0.1
---------------------
Created: 08 AUG 2024
Author: Joe Pecsi | Sideline Data, LLC.
'''

# ===== Libraries ===== #
import mysql.connector
import os, json, sys, uuid
import time, datetime
from datetime import date
from datetime import datetime
from flask import Flask, request
from waitress import serve
from flask_cors import CORS
from decimal import *
# ===================== #



# ===== Support ===== #
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

# =================== #



# ===== API ===== #

# Create the API object
api = Flask(__name__)

# == Keg Management == #
# Return Kegs
@api.route('/kegs/list/<t>', methods=['GET'])
def get_kegs(t):
    try:
        # Return either all active kegs, inactive kegs, all kegs, or keg by ID
        if t == 'active':
            results = db_query('SELECT * FROM tbl_keg WHERE keg_status=1', None, 0)
            log(1,'GET /kegs/active')

        elif t == 'inactive':
            results = db_query('SELECT * FROM tbl_keg WHERE keg_status=0', None, 0)
            log(1,'GET /kegs/inactive')

        elif t == 'all':
            results = db_query('SELECT * FROM tbl_keg', None, 0)
            log(1,'GET /kegs/all')

        else:
            sql = 'SELECT * from tbl_keg WHERE keg_id = %s'
            values = (t,)
            results = db_query(sql, values, 0)
            log(1,'GET /kegs/'+ str(t))

        # Log and return the results
        return results

    # Gracefully handle failure, please :)
    except Exception as e:
        log(0, 'GET /kegs/active failed: ' + str(e))
        return json.dumps({'response':str(e)})

# Create a Keg
@api.route('/kegs/create/<s>', methods=['POST'])
def post_new_keg(s):
    try:
        # Get data from the POST request
        data = request.json

        # Check to make sure there isn't already an active keg on the tap...
        check_sql = 'SELECT keg_id FROM tbl_keg WHERE keg_tap=%s AND keg_status=1'
        check_val = (
            data.get('keg_tap'),
        )

        check_query = db_query(check_sql,check_val,0)

        # If an active keg on the desired tap exists...
        if check_query:
            log(0, 'POST /kegs/create/ FAILED! Tap already has an active keg!')
            return('Failed to create keg; tap already has an active keg!')
        
        # Looks like no keg is on this tap, LET'S GOOOOO
        else:
            # String validation to make sure only a 1 or 0 is passed (1 = active, 0 = inactive)
            if not s.isdigit() or int(s) != 1:
                s = 0

            # Build the database query
            sql = 'INSERT INTO tbl_keg (keg_id, keg_name, keg_size, keg_abv, keg_tap, keg_start, keg_remain, keg_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
            values = (
                str(uuid.uuid4()),
                data.get('keg_name'),
                data.get('keg_size'),
                data.get('keg_abv'),
                data.get('keg_tap'),
                data.get('keg_start'),
                data.get('keg_size'),
                int(s)
            )

            # Execute the query
            db_query(sql,values,1)
            log(1,'POST /kegs/create: ' + data.get('keg_name'))
            return ('Created keg: ' + data.get('keg_name'))
        
    # Gracefully handle failure, please :)
    except Exception as e:
        log(0, 'POST /kegs/create failed: ' + str(e))
        return json.dumps({'response':str(e)})
    

# Delete a Keg
@api.route('/kegs/remove', methods=['DELETE'])
def delete_keg():
    try: 
        # Get data from the DELETE request
        data = request.json

        # Build the query
        sql = 'DELETE FROM tbl_keg WHERE keg_id=%s'
        values = (data.get('keg_id'),)
        
        # Execute the query, make sure it worked...
        if (db_query(sql,values,1)):
            log(1,'Successfully deleted keg: ' + str(data.get('keg_id')))
            return ('Deleted Keg: ' + data.get('keg_id'))
        else:
            log(0,'No changes made to keg id: ' + str(data.get('keg_id')))
            return ('No changes made to keg id: ' + data.get('keg_id'))
    
    # Gracefully handle failure, please :)
    except Exception as e:
        log(0, 'POST /kegs/delete failed: ' + str(e))
        return json.dumps({'response':str(e)})
    

@api.route('/kegs/kick/now', methods=['PUT'])
def put_kick_keg():
    try:
        # Get data from the DELETE request
        data = request.json

        # Kick the keg
        sql = 'UPDATE tbl_keg SET keg_end = %s, keg_remain=0, keg_status=0 WHERE keg_id = %s'
        values = (
            str(date.today()), 
            data.get('keg_id')
        )

        # Execute the query, make sure it worked...
        if (db_query(sql,values,1)):
            log(1,'Successfully kicked keg: ' + str(data.get('keg_id')))
            return ('Kicked Keg: ' + data.get('keg_id'))
        else:
            log(0,'No changes made to keg id: ' + str(data.get('keg_id')))
            return ('No changes made to keg id: ' + data.get('keg_id'))
    

    # Gracefully handle failure, please :)
    except Exception as e:
        log(0, 'POST /kegs/kick/now failed: ' + str(e))
        return json.dumps({'response':str(e)})


# Update a Keg
@api.route('/kegs/update/<k>', methods=['PUT'])
def put_update_keg(k):
    try:
        # Get data from the POST request
        data = request.json

        # Build the database query
        sql = 'UPDATE tbl_keg SET keg_name=%s, keg_size=%s, keg_abv=%s, keg_tap=%s, keg_start=%s, keg_remain=%s, keg_status=%s WHERE keg_id=%s'
        values = (
            data.get('keg_name'),
            data.get('keg_size'),
            data.get('keg_abv'),
            data.get('keg_tap'),
            data.get('keg_start'),
            data.get('keg_remain'),
            data.get('keg_status'),
            k
        )

        # Execute the query, make sure it worked...
        if (db_query(sql,values,1)):
            log(1,'POST /kegs/update/' + str(k))
            return ('Updated keg: ' + str(k))
        else:
            log(0,'No changes made to keg id:' + str(k))
            return ('No changes made to keg id: ' + str(k))
    
    # Gracefully handle failure, please :)
    except Exception as e:
        log(0, 'POST /kegs/update failed: ' + str(e))
        return json.dumps({'response':str(e)})


# == Pour Management == #
# List the pours (all or by keg/tap)
@api.route('/pours/list/<select>/<id>', methods=['GET'])
def get_pours(select,id):
    try:
        # List all pours
        if select == 'all':
            results = db_query('SELECT * FROM tbl_pour LIMIT 100', None, 0)
            log(1,'GET /pours/list/all')
        
        # List pours by a specific tap
        elif select == 'tap':
            sql = 'SELECT * FROM tbl_pour WHERE keg_tap = %s'
            values = (id,)
            results = db_query(sql, values, 0)
            log(1,'GET /pours/list/' + str(id))
        
        # List pours by a specific keg
        elif select == 'keg':
            sql = 'SELECT * FROM tbl_pour WHERE keg_id = %s'
            values = (id,)
            results = db_query(sql, values, 0)
            log(1,'GET /pours/list/' + str(id))

        # Log and return the results
        return results

    # Gracefully handle failure, please :)
    except Exception as e:
        log(0, 'GET /pours/list/ failed: ' + str(e))
        return json.dumps({'response':str(e)})


# Create a new pour
@api.route('/pours/create/<t>', methods=['POST'])
def post_new_pour(t):
    # Make sure a valid tap number was provided
    if t.isdigit():
        data = request.json

        # Build the queries
        insert_sql = 'INSERT INTO tbl_pour (keg_id,keg_tap,pour_time,pour_size,pour_user) VALUES (%s,%s,%s,%s,%s)'
        select_sql = 'SELECT keg_id, keg_remain FROM tbl_keg WHERE keg_tap=%s AND keg_status=1'
        select_val = (t,)

        # Get the keg in question to update the remaining beer
        select_query = db_query(select_sql,select_val,0)

        insert_val = (
            select_query[0][0],
            t,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.get('pour_size'),
            data.get('pour_user')
        )

        # Execute the queries
        if (db_query(insert_sql,insert_val,1)):
            log(1,'POST /pours/create/' + str(t))

            # Update remaining beer
            update_sql = 'UPDATE tbl_keg SET keg_remain=%s WHERE keg_id=%s'
            update_val = (
                select_query[0][1] - Decimal(data.get('pour_size')),
                select_query[0][0]
            )

            # Execute the query, make sure it worked...
            if (db_query(update_sql,update_val,1)):
                remain = select_query[0][1] - Decimal(data.get('pour_size'))
                log(1,'Pour logged for Keg: ' + str(select_query[0][0]) + ' | Beer remaining: ' + str(remain) + ' oz')
            else:
                log(0, 'Failed to update the keg remaining!')
        # Report back if the pour fails to log
        else:
            log(0,'Failed to log new pour')
            return ('Failed to log new pour')
        
    # Scold the user for providing an invalid tap
    else:
        log(0, 'POST /pours/create/' + str(t) + ' failed; invalid tap')
        return json.dumps({'response':'Invalid tap ID'})


# Modify/delete an existing pour
@api.route('/pours/modify', methods=['PUT','DELETE'])
def modify_existing_pour(action):

    # Get request data
    data = request.json

    if request.method == 'PUT':
        # Update existing pour
        update_sql = 'UPDATE tbl_pour SET pour_size=%s, pour_user=%s WHERE pour_time=%s AND keg_id=%s'
        update_val = (
            data.get('pour_size'),
            data.get('pour_user'),
            data.get('pour_time'),
            data.get('keg_id')
        )

        if (db_query(update_sql,update_val,1)):
            log(1,'PUT /pours/modify - Updated the pour')
        else:
            log(0, 'PUT /pours/modify - Failed to update')

    elif request.method == 'DELETE':
        # Delete existing pour
        del_sql = 'DELETE FROM tbl_pour WHERE pour_time=%s AND keg_id=%s'
        del_val = (
            data.get('pour_time'),
            data.get('keg_id')
        )

        if (db_query(del_sql,del_val,1)):
            log(1,'PUT /pours/modify - Deleted the pour')
        else:
            log(0, 'PUT /pours/modify - Failed to delete')
    
# =============== #


# ===== Main ===== #

if __name__ == '__main__':
    # Environment variables for database connection
    db_host = os.getenv("DB_HOST", "<blank>")   # Database Host
    db_user = os.getenv("DB_USER", "<blank>")   # Database User
    db_pass = os.getenv("DB_PASS", "<blank>")   # Database Password
    db_name = os.getenv("DB_NAME", "<blank>")   # Database Name
    db_port = os.getenv("DB_PORT", "<blank>")   # Database Port
    logging = os.getenv("CONSOLE_LOG")          # Logging to the console (True/False)
    
    # Display initial message (title/version/db info) to the console
    print("WatchMy.Beer API Server (v0.1)\n==============================")
    log(1, 'Connecting to database...')
    print("   Host: " + db_host + ":" + str(db_port))
    print("   User: " + db_user)
    print("   Database: " + db_name)

    # Try to connect to the database...
    try:
        # Create database connection and output results
        db_query('SELECT keg_id FROM tbl_keg LIMIT 1', None, 0)
        log(1,'Connected to database')
        log(1, 'Starting API server on 0.0.0.0:25518')

        # Resolve issues with CORS policy for user pass web interface
        CORS(api)

        # Start the API
        serve(api, host="0.0.0.0", port=25518)
    
    # Catch any issues and gracefully exit
    except Exception as e:
        log(0, 'Issues communicating with database - ' + str(e))
        sys.exit(0)

# ================ #