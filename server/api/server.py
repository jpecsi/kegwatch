'''
WatchMy.Beer Server
Version: 0.3
---------------------
Created: 07 AUG 2024
Updated: 10 AUG 2024
Author: Joe Pecsi | Sideline Data, LLC.
'''

# ===== Libraries ===== #
import sys
from support import *
from kegs import kegs_api
from pours import pours_api
from flask import Flask, request
from waitress import serve
from flask_cors import CORS
# ===================== #


# ===== API ===== #
# Create the API object
api = Flask(__name__)
api.register_blueprint(kegs_api, url_prefix='/kegs')
api.register_blueprint(pours_api, url_prefix='/pours')

# Catch-All
@api.route("/")
def catch_all():
    return 'WatchMy.Beer Server | Version 0.3'
# =============== #


# ===== Main ===== #
if __name__ == '__main__':
    # Display initial message (title/version/db info) to the console
    print("WatchMy.Beer API Server (v0.3)\n==============================")
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