'''
API Routes: kegs
[WatchMy.Beer Server]
---------------------
Created: 10 AUG 2024
Updated: 10 AUG 2024
Author: Joe Pecsi | Sideline Data, LLC.
'''

# ===== Libraries ===== #
from support import *
import json, uuid
from datetime import date
from flask import Blueprint, request
# ===================== #


# ===== API Registration ===== #
kegs_api = Blueprint('kegs_api', __name__)
# ============================ #


# ===== API Routes ===== #
# Return Kegs
@kegs_api.route('/list/<t>', methods=['GET'])
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

        # Log and return the results
        return results

    # Gracefully handle failure, please :)
    except Exception as e:
        log(0, 'GET /kegs/active failed: ' + str(e))
        return json.dumps({'response':str(e)})

# Create a Keg
@kegs_api.route('/create/<s>', methods=['POST'])
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
@kegs_api.route('/remove', methods=['DELETE'])
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
    

@kegs_api.route('/kick/now', methods=['PUT'])
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
@kegs_api.route('/update/', methods=['PUT'])
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

# ====================== #
