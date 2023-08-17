from api import *
import time

def fun_time(data:DSPD): return NumberValue(time.time())

module = {
    "name": "time",
    "functions":{
        "time":[fun_time, []]
    }
}

DSAPI.add_module(module)