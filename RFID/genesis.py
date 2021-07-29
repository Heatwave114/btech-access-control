#!/usr/bin/env python

import sys
import time
import RPi.GPIO as GPIO
from datetime import datetime
from mfrc522 import SimpleMFRC522

# local
from firebase import Database

reader = SimpleMFRC522()
#GPIO.setwarnings(False)
granted_led_pin = 12
denied_led_pin = 18
buzzer_pin = 16

# GPIO.setmode(GPIO.BCM)
GPIO.setup(granted_led_pin, GPIO.OUT)
GPIO.setup(denied_led_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)

# _control = {
#     "allowed_ranks": [1, 2, 3, 4],
#     "block_all_doors": False,
#     "blocked_ids": [],
# }

# _access_list = {
#     "63554175774": {
#     "name": "Katrina Whitley",
#     "access": [
#       4,
#       4,
#       1
#     ],
#     "rank": 2
#   },
#   "bafd2fa9-f997-56da-b7c4-713431f0d49f": {
#     "name": "Karla Ratliff",
#     "access": [
#       4
#     ],
#     "rank": 3
#   },
#   "743de31f-7d7b-5bc8-a10f-a127dfb3f3b6": {
#     "name": "Peck Dodson",
#     "access": [
#       1,
#       4,
#       4
#     ],
#     "rank": 3
#   },
# }


# _door = {
#     "id": 3
# }

database = Database()

def __access_list():
    return database.return_access_list()

def __control():
    return database.return_control()

def __door():
    return database.return_door()

default_reason = "Passed condition check" # default reason to give access
_reasons = [default_reason]
def control_check(id: str) -> bool:
    _access_list = __access_list()
    _control = __control()
    _door = __door()
    global _reasons
    check_status = True
    control_reasons = []
    
    if id not in _access_list:
        check_status = False
        control_reasons.append("Unknown Id")
    else:
        if _access_list[id]["rank"] not in _control["allowed_ranks"]:
            check_status = False
            control_reasons.append("Rank restricted")
        if _door["id"] not in _access_list[id]["access"]:
            check_status = False
            control_reasons.append(f"No rights to door {_door['id']}")

    if id in _control["blocked_ids"]:
        check_status = False
        control_reasons.append("In blocked list")

    if _control["block_all_doors"]:
        check_status = False
        control_reasons.append("All doors blocked")

    if not check_status:
        _reasons = control_reasons

    return check_status

def read():
    try:
        id, _ = reader.read()
        id = str(id)
        print("RFID", id)
        if control_check(id):
            system_behaviour_granted(id)
        else:
            system_behaviour_denied(id)
    # finally:
    #     GPIO.cleanup()
    except KeyboardInterrupt:
        sys.exit()
    global _reasons
    _reasons = default_reason
    read()


ON = True; OFF = False; # for readability when switching
def switch(level: bool, pin: int):
    if level:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)

def started_reading_behaviour():
    for _ in range(5):
        switch(ON, granted_led_pin)
        switch(OFF, denied_led_pin)
        time.sleep(.1)
        switch(OFF, granted_led_pin)
        switch(ON, denied_led_pin)
        time.sleep(.1)
    switch(OFF, denied_led_pin)

def system_behaviour_granted(id: str):
    write_to_log(id, "granted")
    switch(ON, granted_led_pin)
    for _ in range(3):
        switch(ON, buzzer_pin)
        time.sleep(.1)
        switch(OFF, buzzer_pin)
        time.sleep(.1)
    switch(OFF, granted_led_pin)

def system_behaviour_denied(id: str):
    write_to_log(id, "denied")
    switch(ON, denied_led_pin)
    switch(ON, buzzer_pin)
    time.sleep(1)
    switch(OFF, buzzer_pin)
    switch(OFF, denied_led_pin)

def write_to_log(id: str, access_permission: str):
    _access_list = __access_list()
    _door = __door()
    if id in _access_list:
        entity = _access_list[id]
        current_door_id = _door["id"]
        log = {
            "time": datetime.now().strftime(r"%Y:%m:%d::%H:%M:%S:%f"),
            "door": current_door_id,
            "permission": access_permission,
            "name": entity["name"],
            "id": id,
            "rank": entity["rank"],
            "reasons": _reasons,
        }
    else:
        current_door_id = _door["id"]
        log = {
            "time": datetime.now().strftime(r"%Y:%m:%d::%H:%M:%S:%f"),
            "door": current_door_id,
            "permission": access_permission,
            "name": "Null",
            "id": id,
            "rank": "Null",
            "reasons": _reasons,
        }
    database.write_to_logs(log)
    print(log)
    # _database.path_to_log.write(log)

started_reading_behaviour()
read()
