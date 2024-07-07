'''
KegWatch API Server (Dev)
Version: 0.2
---------------------------
Modified: 15 NOV 2023
Author: Joe Pecsi
'''


# ===== LIBRARIES ===== #
import mysql.connector
import os, json, sys, uuid
import time, datetime
from datetime import date
from datetime import datetime
from flask import Flask, request
from waitress import serve
from flask_cors import CORS
# ===================== #





# ===== SUPPORT FUNCTIONS ===== #
# Formatted logging to the console (if enabeld)
def log(t,m):
    if logging:
        now = str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        if t == 0:
            # Failure
            print(now + " [ERROR] " + m)

        elif t == 1:
            # Success
            print(now + " [STATUS] " + m)

# Database queries
def db_query(q,v,m):
    # Connect to the datbase
    db = mysql.connector.connect(
            host=db_host,
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
# ============================= #




# ===== API ===== #
# Setup
api = Flask(__name__)

# Status Check
@api.route('/alive', methods=['GET'])
def status_check():
    log(1,'GET /alive - health check requested')
    return json.dumps({"success": True}), 201

# KEG MANAGEMENT
# Return active kegs from 'keg_log' table
@api.route('/kegs/active', methods=['GET'])
def kegs_return_active():
    # Check for arguments in 'GET' request
    args = request.args
    if args.get("tap"):
        sql = 'SELECT * FROM keg_log WHERE status=1 AND tap=%s'
        val = (args.get("tap"),)
        results = db_query(sql,val,0)
    else:
        results = db_query('SELECT * FROM keg_log WHERE status=1', None, 0)

    # Log and return the data
    log(1,'Returning list of active kegs')
    return results

# Return all kegs from 'keg_log' table
@api.route('/kegs/all', methods=['GET'])
def kegs_return_all():
    log(1,'Returning list of all kegs')
    results = db_query('SELECT * FROM keg_log', None, 0)
    return results

# Create a new keg in the 'keg_log' table
@api.route('/kegs/create', methods=['POST'])
def kegs_create_new():
    try:
        # Get the data from the 'POST' request
        data = request.json
        sql = 'INSERT INTO keg_log (id,name,tap,abv,capacity,remaining,date_tapped,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        val = (
            str(uuid.uuid4()),
            data.get('name'),
            data.get('tap'),
            data.get('abv'),
            data.get('capacity'),
            data.get('capacity'),
            data.get('date_tapped'),
            1
        )
        # Execute the query and return 'success'
        db_query(sql,val,1)
        log(1,'Successfully created a new keg')
        return json.dumps({"success": True}), 201

    # Catch any issues with the request
    except Exception as e:
        log(0,('Failed to create a new keg: ' + str(e)))
        return json.dumps({"success": False}), 500

# Kick an existing, active keg in the 'keg_log' table
@api.route('/kegs/kick', methods=['POST'])
def kegs_kick_existing():
    try:
        # Get data from the 'POST' request
        data = request.json
        
        # Get data from the existing keg to properly kick and record time/days to consume
        fetch_sql = 'SELECT * FROM keg_log WHERE id=%s'
        fetch_val = (data.get('keg_id'),)
        result = db_query(fetch_sql,fetch_val,0)

        # Figure out how many days it took to consume the keg
        dt = datetime.strptime(result[0][6], '%Y-%m-%d')
        dk = datetime.strptime(str(date.today()), '%Y-%m-%d')
        dtc = dk-dt

        # Kick the keg!
        update_sql = 'UPDATE keg_log SET date_kicked = %s, days_to_consume = %s, status = 0 WHERE id = %s'
        update_val = (
            str(date.today()),
            int(dtc.days),
            data.get('keg_id')
        )

        db_query(update_sql,update_val,1)

        # Log and return 'success'
        log(1,'Successfully kicked keg')
        return json.dumps({"success": True}), 201

    # Catch any issues with the request
    except Exception as e:
        log(0,('Failed to kick keg: ' + str(e)))
        return json.dumps({"success": False}), 500



# USER MANAGEMENT
# Return a list of users from the 'consumers' table
@api.route('/users/list', methods=['GET'])
def users_list_all():
    # Get all users from the database
    results = db_query('SELECT * FROM consumers', None, 0)

    # Log and return the results
    log(1,'Returning list of users')
    return results

# Remove an existing user from the 'consumers' table
@api.route('/users/remove', methods=['POST'])
def users_remove_existing():
    try:
        # Get data from the 'POST' request
        data = request.json

        # Remove the user from the database
        sql = 'DELETE FROM consumers WHERE id=%s'
        val = (data.get('user_id'),)
        db_query(sql,val,1)

        # Log and return success
        log(1,'Successfully removed user')
        return json.dumps({"success": True}), 201

    # Catch any issues with the request
    except Exception as e:
        log(0,('Failed to remove user: ' + str(e)))
        return json.dumps({"success": False}), 500

# Create a new user in the 'consumers' table
@api.route('/users/create', methods=['POST'])
def users_add_new():
    try:
        # Get data from the 'POST' request
        data = request.json

        # Build the query
        sql = 'INSERT INTO consumers (name, weight, gender) VALUES (%s,%s,%s)'
        val = (
            data.get('name'),
            data.get('weight'),
            data.get('gender')
        )

        # Execute the query
        db_query(sql,val,1)

        # Log and return success
        log(1,'Successfully created user')
        return json.dumps({"success": True}), 201
    
    # Catch any issues with the request
    except Exception as e:
        log(0,('Failed to create a new user: ' + str(e)))
        return json.dumps({"success": False}), 500   

# Modify the properties of an existing user in the 'consumers' table
@api.route('/users/modify', methods=['POST'])
def users_modify_existing():
    try:
        # Get the data from the 'POST' request
        data = request.json

        # Build the query
        sql = 'UPDATE consumers SET name=%s,weight=%s,gender=%s WHERE id=%s'
        val = (
            data.get('name'),
            data.get('weight'),
            int(data.get('gender')),
            int(data.get('user_id'))
        )

        # Execute the query
        db_query(sql,val,1)

        # Log and return success
        log(1,'Successfully modified user')
        return json.dumps({"success": True}), 201

    # Catch any issues with the request
    except Exception as e:
        log(0,('Failed to modify a user: ' + str(e)))
        return json.dumps({"success": False}), 500  

# Return user stats (favorite beer, total oz poured) for the 'User Pass' web interface
@api.route('/pass/user', methods=['GET'])
def get_user_stats():
    try:
        # Get arguments from the 'GET' request
        args = request.args
        if args.get("consumer"):
            # Build the query to get total oz poured
            oz_sql = 'SELECT total_poured FROM consumers WHERE name=%s'

            # Build the query to get the favorite beer
            keg_sql = 'SELECT name FROM keg_log WHERE id IN (SELECT keg_id FROM beer_log WHERE consumer=%s GROUP BY keg_id ORDER BY COUNT(keg_id) DESC)'
            
            # Execute queries
            query_val = (args.get("consumer"),)
            total_oz = db_query(oz_sql,query_val,0)
            fav_beer = db_query(keg_sql,query_val,0)
            
            # Log and return the stats
            log(1,('Retrieved user stats (favorite beer and oz poured) for ' + str(args.get('consumer'))))
            return json.dumps({"total_oz":str(round(total_oz[0][0]))+" oz.", "fav_beer":str(fav_beer[0][0])})
        
        # If the user name wasn't actually provided, return 'None' for stats
        else:
            return json.dumps({"total_oz":"None", "fav_beer":"None"})
    except Exception as e:
        log(0,('Failed to get user stats: ' + str(e)))
        return json.dumps({"total_oz":"None", "fav_beer":"None"})
        


# BEER MANAGEMENT
# Log a new pour into the 'beer_log' table
@api.route('/beer/pour', methods=['POST'])
def beer_log_pour():
    try:
        # Get data from the 'POST' request
        data = request.json

        # Build/execute the query for the beer_log entry
        sql_pour = 'INSERT INTO beer_log (time,tap_id,keg_id,consumer,oz_poured) VALUES (%s,%s,%s,%s,%s)'
        val_pour = (
            str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')),
            data.get('tap_id'),
            data.get('keg_id'),
            data.get('consumer'),
            data.get('oz_poured')
        )
        
        # Execute the query
        db_query(sql_pour,val_pour,1)

        # Build/execute the query for the keg_log entry
        sql_keg = 'UPDATE keg_log SET remaining=%s WHERE id=%s'
        val_keg = (
            data.get('oz_remain'),
            data.get('keg_id')
        )

        # Execute the query
        db_query(sql_keg,val_keg,1)

        # Update consumers table
        if db_query('SELECT name FROM consumers WHERE name=%s',(data.get('consumer'),),0):
            # Update the total lifetime oz poured for the consumer
            current_poured = db_query('SELECT total_poured FROM consumers WHERE name=%s',(data.get('consumer'),),0)
            updated_pour = current_poured[0][0] + data.get('oz_poured')
            db_query('UPDATE consumers SET total_poured=%s WHERE name=%s',(updated_pour,data.get('consumer')),1)
        else:
            # Create a new user
            db_query('INSERT INTO consumers (name,weight,gender,total_poured) VALUES (%s,%s,%s,%s)', (data.get('consumer'),0,0,data.get('oz_poured')),1)

        
        # Log and return success
        log(1, 'Added a new pour')
        return json.dumps({"success": True}), 201

    # Catch any issues with the request
    except Exception as e:
        log(0,('Failed to create a new pour: ' + str(e)))
        return json.dumps({"success": False}), 500 
# =============== #





# ===== MAIN ===== #
if __name__ == '__main__':
    # Grab environment variables
    db_host = os.getenv("DB_HOST", "<blank>")   # Database Host
    db_user = os.getenv("DB_USER", "<blank>")   # Database User
    db_pass = os.getenv("DB_PASS", "<blank>")   # Database Password
    db_name = os.getenv("DB_NAME", "<blank>")   # Database Name
    logging = os.getenv("CONSOLE_LOG")          # Logging to the console (True/False)

    # Display initial message (title/version/db info) to the console
    print("KegWatch API Server (v0.2)\n==========================")
    log(1, 'Connecting to database...')
    print("   Host: " + db_host + ":3306")
    print("   User: " + db_user)
    print("   Password: " + db_pass)
    print("   Database: " + db_name)

    # Try to connect to the database...
    try:
        # Create database connection and output results
        db_query('SELECT id FROM keg_log LIMIT 1', None, 0)
        log(1,'Connected to database')
        log(1, 'Starting API server on 0.0.0.0:8335')

        # Resolve issues with CORS policy for user pass web interface
        CORS(api)

        # Start the API
        serve(api, host="0.0.0.0", port=8335)
    
    # Catch any issues and gracefully exit
    except Exception as e:
        log(0, 'Issues communicating with database - ' + str(e))
        sys.exit(0)
# ================ #