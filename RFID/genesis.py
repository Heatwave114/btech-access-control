#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
from datetime import datetime
from mfrc522 import SimpleMFRC522
from typing import Union


#GPIO.setwarnings(False)

reader = SimpleMFRC522()

granted_led_pin = 12
denied_led_pin = 18
buzzer_pin = 16

# GPIO.setmode(GPIO.BCM)
GPIO.setup(granted_led_pin, GPIO.OUT)
GPIO.setup(denied_led_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)

# try:
#         id, text = reader.read()
#         print(id)
#         print(text)
# finally:
#         GPIO.cleanup()

# _database = pass

_control = {
    "allowed_ranks": ["1", "2", "3", "4"],
    "block_all_doors": False,
    "blocked_ids": [],
}

_access_list = {
    "63554175774": {
    "name": "Katrina Whitley",
    "access": [
      4,
      4,
      1
    ],
    "rank": 2
  },
  "bafd2fa9-f997-56da-b7c4-713431f0d49f": {
    "name": "Karla Ratliff",
    "access": [
      4
    ],
    "rank": 3
  },
  "743de31f-7d7b-5bc8-a10f-a127dfb3f3b6": {
    "name": "Peck Dodson",
    "access": [
      1,
      4,
      4
    ],
    "rank": 3
  },
}


_current_door = {
    "id": 3
}

default_reason = "In allowed list" # default reason to give access
_reasons = [default_reason]
def control_check(id: str) -> bool:
    check_status = True
    control_reasons = []
    if id not in _access_list:
        check_status = False
        control_reasons.append("Unknown Id")
    else:
        if _access_list[id]["rank"] not in _control["allowed_ranks"]:
            check_status = False
            control_reasons.append("Rank restricted")

    if id in _control["blocked_ids"]:
        check_status = False
        control_reasons.append("In blocked list")
    if _control["block_all_doors"]:
        check_status = False
        control_reasons.append("All doors blocked")
    

    if control_reasons:
        _reasons = control_reasons
    return check_status

def read():
        id, _ = reader.read()
        id = str(id)
        print("RFID", id)
        if control_check(id):
            write_to_log(id, "granted")
            system_behaviour_granted(id)
        else:
            write_to_log(id, "denied")
            system_behaviour_denied(id)


ON = True; OFF = False; # for readability when switching
def switch(level: bool, pin: int):
    if level:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)

def system_behaviour_granted(id: str):
    write_to_log(id, "granted")
    switch(ON, granted_led_pin)
    for _ in range(3):
        switch(ON, buzzer_pin)
        time.sleep(.3)
        switch(OFF, buzzer_pin)
    switch(OFF, granted_led_pin)

def system_behaviour_denied(id: str):
    write_to_log(id, "denied")
    switch(ON, denied_led_pin)
    switch(ON, buzzer_pin)
    time.sleep(1)
    switch(OFF, buzzer_pin)
    switch(OFF, denied_led_pin)

def write_to_log(id: str, access_permission: str):
    entity = _access_list[id]
    current_door_id = _current_door["id"]
    log = {
        "time": datetime.now().strftime(r"%Y:%m:%d::%H:%M:%S:%f"),
        "door": current_door_id,
        "permission": access_permission,
        "name": entity["name"],
        "id": id,
        "rank": entity["rank"],
        "reasons": _reasons,
    }
    print(log)
    # _database.path_to_log.write(log)

try:
    read()
finally:
    GPIO.cleanup()

        


# _access_list = {
#     "5e5894d5-04e1-5057-807a-60cf660936f0": {
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
#   "1098348e-bd20-5c0d-8dac-a9001b7be74a": {
#     "name": "Pat Fuentes",
#     "access": [
#       4,
#       1,
#       4
#     ],
#     "rank": 2
#   },
#   "e1007fc0-89ee-5979-814d-f54c25686d19": {
#     "name": "Roxie Beard",
#     "access": [
#       1
#     ],
#     "rank": 3
#   },
#   "374689a1-fbd0-52b4-88ac-5831f1f474d1": {
#     "name": "Molly Gates",
#     "access": [
#       1,
#       4,
#       4,
#       1
#     ],
#     "rank": 2
#   },
#   "a6738d84-21ea-55f5-a2dd-4e89b9df3059": {
#     "name": "Keith Rivera",
#     "access": [
#       4,
#       1,
#       1
#     ],
#     "rank": 2
#   },
#   "38f96874-816e-57aa-8704-147868198705": {
#     "name": "Perez Tillman",
#     "access": [
#       1
#     ],
#     "rank": 2
#   },
#   "a58e13d0-51e9-525c-a2c8-631abd076334": {
#     "name": "Copeland Burt",
#     "access": [
#       4,
#       1
#     ],
#     "rank": 1
#   },
#   "39bb960a-2d69-59c0-afee-5b44a3a5d5e7": {
#     "name": "Burt Romero",
#     "access": [
#       1,
#       4,
#       4
#     ],
#     "rank": 3
#   }
# }