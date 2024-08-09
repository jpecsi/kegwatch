'''
WatchMy.Beer Server
Version: 0.2
---------------------
Created: 07 AUG 2024
Updated: 09 AUG 2024
Author: Joe Pecsi | Sideline Data, LLC.
'''

# ===== Libraries ===== #
import mysql.connector
import os, json, sys, uuid, re
import time, datetime
from datetime import date
from dateutil.parser import parse
from datetime import date
from datetime import datetime
from uuid import UUID
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
            log(0,'Data Validation Failed: keg_id')
            
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
            validated_data['pour_size'] = d.get('pour_size')
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
            if int(t):
                sql = 'SELECT * from tbl_keg WHERE keg_id = %s'
                values = (t,)
                results = db_query(sql, values, 0)
                log(1,'GET /kegs/'+ str(t))
            else:
                results = "Invalid tap number!"
                log(0,'GET /kegs/'+ str(t) + ' failed - invalid tap number')

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
        data = validate(request.json)
        if data:
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
                    data['keg_name'],
                    data['keg_size'],
                    data['keg_abv'],
                    data['keg_tap'],
                    data['keg_start'],
                    data['keg_size'],
                    int(s)
                )

                # Execute the query
                db_query(sql,values,1)
                log(1,'POST /kegs/create: ' + data['keg_name'])
                return ('Created keg: ' + data['keg_name'])
        else:
            return json.dumps({'response':'Invalid data'})
    # Gracefully handle failure, please :)
    except Exception as e:
        log(0, 'POST /kegs/create failed: ' + str(e))
        return json.dumps({'response':str(e)})
    

# Delete a Keg
@api.route('/kegs/remove', methods=['DELETE'])
def delete_keg():
    try: 
        # Get data from the DELETE request
        data = validate(request.json)

        if data:
            # Build the query
            sql = 'DELETE FROM tbl_keg WHERE keg_id=%s'
            values = (data['keg_id'],)
            
            # Execute the query, make sure it worked...
            if (db_query(sql,values,1)):
                log(1,'Successfully deleted keg: ' + str(data['keg_id']))
                return ('Deleted Keg: ' + data['keg_id'])
            else:
                log(0,'No changes made to keg id: ' + str(data['keg_id']))
                return ('No changes made to keg id: ' + data['keg_id'])
        
        else:
            return json.dumps({'response':'Invalid data'})
    
    # Gracefully handle failure, please :)
    except Exception as e:
        log(0, 'POST /kegs/delete failed: ' + str(e))
        return json.dumps({'response':str(e)})
    

@api.route('/kegs/kick/now', methods=['PUT'])
def put_kick_keg():
    try:
        # Get data from the DELETE request
        data = validate(request.json)

        if data:
            # Kick the keg
            sql = 'UPDATE tbl_keg SET keg_end = %s, keg_remain=0, keg_status=0 WHERE keg_id = %s'
            values = (
                str(date.today()), 
                data['keg_id']
            )

            # Execute the query, make sure it worked...
            if (db_query(sql,values,1)):
                log(1,'Successfully kicked keg: ' + str(data['keg_id']))
                return ('Kicked Keg: ' + data['keg_id'])
            else:
                log(0,'No changes made to keg id: ' + str(data['keg_id']))
                return ('No changes made to keg id: ' + data['keg_id'])
        else:
            return json.dumps({'response':'Invalid data'})

    # Gracefully handle failure, please :)
    except Exception as e:
        log(0, 'POST /kegs/kick/now failed: ' + str(e))
        return json.dumps({'response':str(e)})


# Update a Keg
@api.route('/kegs/update/', methods=['PUT'])
def put_update_keg():
    try:
        # Get data from the POST request
        data = validate(request.json)

        if data:
            # Build the database query
            sql = 'UPDATE tbl_keg SET keg_name=%s, keg_size=%s, keg_abv=%s, keg_tap=%s, keg_start=%s, keg_remain=%s, keg_status=%s WHERE keg_id=%s'
            values = (
                data['keg_name'],
                data['keg_size'],
                data['keg_abv'],
                data['keg_tap'],
                data['keg_start'],
                data['keg_remain'],
                data['keg_status'],
                data['keg_id']     
            )

            # Execute the query, make sure it worked...
            if (db_query(sql,values,1)):
                log(1,'POST /kegs/update/' + str(data['keg_id']))
                return ('Updated keg: ' + str(data['keg_id']))
            else:
                log(0,'No changes made to keg id:' + str(data['keg_id']))
                return ('No changes made to keg id: ' + str(data['keg_id']))
        else:
            return json.dumps({'response':'Invalid data'})
    
    # Gracefully handle failure, please :)
    except Exception as e:
        log(0, 'POST /kegs/update failed: ' + str(e))
        return json.dumps({'response':str(e)})


# == Pour Management == #
# List the pours (all or by keg/tap)
@api.route('/pours/list/<select>', methods=['GET'])
def get_pours(select):
    try:
        # List all pours
        if select == 'all':
            results = db_query('SELECT * FROM tbl_pour LIMIT 100', None, 0)
            log(1,'GET /pours/list/all')
            return results
        
        else:
            data = validate(request.json)
            if data:
                # List pours by a specific tap
                if select == 'tap':
                    sql = 'SELECT * FROM tbl_pour WHERE keg_tap = %s'
                    values = (data['id'],)
                    results = db_query(sql, values, 0)
                    log(1,'GET /pours/list/' + str(data['id']))
                
                # List pours by a specific keg
                elif select == 'keg':
                    sql = 'SELECT * FROM tbl_pour WHERE keg_id = %s'
                    values = (data['id'],)
                    results = db_query(sql, values, 0)
                    log(1,'GET /pours/list/' + str(data['id']))
                
                return results
            else:
                return json.dumps({'response':'Invalid data'})

    # Gracefully handle failure, please :)
    except Exception as e:
        log(0, 'GET /pours/list/ failed: ' + str(e))
        return json.dumps({'response':str(e)})


# Create a new pour
@api.route('/pours/create/', methods=['POST'])
def post_new_pour():
    # Make sure a valid tap number was provided
    data = validate(request.json)

    if data:
        # Build the queries
        insert_sql = 'INSERT INTO tbl_pour (keg_id,keg_tap,pour_time,pour_size,pour_user) VALUES (%s,%s,%s,%s,%s)'
        select_sql = 'SELECT keg_id, keg_remain FROM tbl_keg WHERE keg_tap=%s AND keg_status=1'
        select_val = (data['keg_tap'],)

        # Get the keg in question to update the remaining beer
        select_query = db_query(select_sql,select_val,0)
        if select_query:
            insert_val = (
                select_query[0][0],
                data['keg_tap'],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                data['pour_size'],
                data['pour_user']
            )

            # Execute the queries
            if (db_query(insert_sql,insert_val,1)):
                log(1,'POST /pours/create/' + str(data['keg_tap']))

                # Update remaining beer
                update_sql = 'UPDATE tbl_keg SET keg_remain=%s WHERE keg_id=%s'
                update_val = (
                    select_query[0][1] - Decimal(data['pour_size']),
                    select_query[0][0]
                )

                # Execute the query, make sure it worked...
                if (db_query(update_sql,update_val,1)):
                    remain = select_query[0][1] - Decimal(data['pour_size'])
                    log(1,'Pour logged for Keg: ' + str(select_query[0][0]) + ' | Beer remaining: ' + str(remain) + ' oz')
                    return json.dumps({'response':'Successfully added pour!'})
                else:
                    log(0, 'Failed to update the keg remaining!')

            # Report back if the pour fails to log
            else:
                log(0,'Failed to log new pour')
                return ('Failed to log new pour')
            
        else:
            log(0, 'Keg not found on tap')
            return json.dumps({'response':'Keg not found on tap'})
        
    # Scold the user for providing an invalid tap
    else:
        log(0, 'POST /pours/create/ failed - invalid data')
        return json.dumps({'response':'Invalid data'})


# Modify/delete an existing pour
@api.route('/pours/modify', methods=['PUT','DELETE'])
def modify_existing_pour(action):

    # Get request data
    data = validate(request.json)
    if data:
        if request.method == 'PUT':
            # Update existing pour
            update_sql = 'UPDATE tbl_pour SET pour_size=%s, pour_user=%s WHERE pour_time=%s AND keg_id=%s'
            update_val = (
                data['pour_size'],
                data['pour_user'],
                data['pour_time'],
                data['keg_id']
            )

            if (db_query(update_sql,update_val,1)):
                log(1,'PUT /pours/modify - Updated the pour')
            else:
                log(0, 'PUT /pours/modify - Failed to update')

        elif request.method == 'DELETE':
            # Delete existing pour
            del_sql = 'DELETE FROM tbl_pour WHERE pour_time=%s AND keg_id=%s'
            del_val = (
                data['pour_time'],
                data['keg_id']
            )

            if (db_query(del_sql,del_val,1)):
                log(1,'PUT /pours/modify - Deleted the pour')
            else:
                log(0, 'PUT /pours/modify - Failed to delete')
    else:
        return json.dumps({'response':'Invalid data'})
    
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
    print("WatchMy.Beer API Server (v0.2)\n==============================")
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