## README

### Overview

This repo is just a place to store scripts written for testing, verification, etc.


### API Testing Scripts

##### Pour Simulator (pour_sim.py)

This script is used to check logging pours and kicking kegs. After providing the tap, number of pours, and (optional) consumer name the script will check to see if the keg is active, log the pour, and report back how much is remaining in the keg. Pour amounts are randomly generated float values. Syntax/usage below

    # Usage
    python3 pour_sim.py -t <tap id> -n <num pours> -c <optional 'Consumer'>
        
    # Example
    python3 pour_sim.py -t 2 -n 3 -c 'Samuel Adams'
          
    # Output
    [TAP 2] Beer found: Dev Lite
    [TAP 2] Simulating 3 pours...
    [TAP 2] Poured: 11.660940015130478 oz. | Remaining: 834.237
    [TAP 2] Poured: 5.7958188984179015 oz. | Remaining: 828.441
    [TAP 2] Poured: 2.398526531956308 oz. | Remaining: 826.042
          

If you do not provide a consumer it will use "Pour Simulator" by default. If you send `-1` as the number of pours, it will kick the beer.

Be sure to update the script to provide the URL to your local API server!