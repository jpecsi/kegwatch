'''
API Routes: pours
[WatchMy.Beer Server]
---------------------
Created: 10 AUG 2024
Updated: 10 AUG 2024
Author: Joe Pecsi | Sideline Data, LLC.
'''

# ===== Libraries ===== #
import json,datetime
from support import *
from datetime import datetime
from uuid import UUID
from flask import Blueprint, request
from decimal import *
# ===================== #


# ===== API Registration ===== #
pours_api = Blueprint('pours_api', __name__)
# ============================ #


# ===== API Routes ===== #
# List the pours (all or by keg/tap)
@pours_api.route('/list/<select>/<id>', methods=['GET'])
def get_pours(select,id):
    try:
        # List all pours
        if select == 'all':
            results = db_query('SELECT * FROM tbl_pour LIMIT 100', None, 0)
            log(1,'GET /pours/list/all')
            return results
        
        else:
            # List pours by a specific tap
            if select == 'tap':
                if int(id):
                    sql = 'SELECT * FROM tbl_pour WHERE keg_tap = %s'
                    values = (id,)
                    results = db_query(sql, values, 0)
                    log(1,'GET /pours/list/' + str(id))
                    return results
                else:
                    log(0, 'GET /pours/list/keg/ ' + str(id) + '- Failed, invalid data')
                    return json.dumps({'response':'Invalid data'})
            
            # List pours by a specific keg
            elif select == 'keg':
                if UUID(id, version=4):
                    sql = 'SELECT * FROM tbl_pour WHERE keg_id = %s'
                    values = (id,)
                    results = db_query(sql, values, 0)
                    log(1,'GET /pours/list/' + str(id))
                    return results
                else:
                    log(0, 'GET /pours/list/keg/ ' + str(id) + '- Failed, invalid data')
                    return json.dumps({'response':'Invalid data'})
            else:
                return json.dumps({'response':'Invalid data'})

    # Gracefully handle failure, please :)
    except Exception as e:
        log(0, 'GET /pours/list/ failed: ' + str(e))
        return json.dumps({'response':str(e)})


# Create a new pour
@pours_api.route('/create/', methods=['POST'])
def post_new_pour():
    # Make sure a valid tap number was provided
    data = validate(request.json)

    # Make sure all required info was sent
    if data and data['keg_tap'] and data['pour_size'] and data['pour_user']:
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
            log(0, 'Invalid request, data did not pass validation')
            return json.dumps({'response':'Invalid request - data did not pass validation'})
        
    # Scold the user for providing an invalid tap
    else:
        log(0, 'POST /pours/create/ failed - invalid data')
        return json.dumps({'response':'Invalid data'})


# Modify/delete an existing pour
@pours_api.route('/modify', methods=['PUT','DELETE'])
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
    
# ====================== #

