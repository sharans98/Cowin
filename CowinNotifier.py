# sudo pip3 install telegram-send requests cowin==0.0.3 

import telegram_send
import time
from datetime import datetime
from cowin_api import CoWinAPI
import pandas as pd
import requests

def send_telegram(data,time):
    sesh = data['sessions']
    message = "\nPinCode: " + str(data['pincode']) +"\nName: " + str(data['name']) + "\nDate: "+ str(sesh[0]['date']) + "\nAvailable: " + str(sesh[0]['available_capacity']) + "\n\n\nQueried at :" + str(time)
    print(message)
    # telegram_send needs to be configured. Use pypi documentation for help: https://pypi.org/project/telegram-send/
    # telegram_send.send(conf="~/channel.conf",messages=[message])


def send_notification(data):
  # data1 = (str(data).split('{'))
  for i in data:
    time = datetime.now()
    time = time.strftime("%H:%M:%S")
    send_telegram(i,time)

def check_for_vaccine():
    state_id = 'XX' #state id. (for karnatake its '16'
    district_id = 'XXX' # district id. (for BBMP its '294'
    date = datetime.now()
    date = date.strftime("%d-%m-%Y")
    min_age_limit = XX # 18 or 45
    available_centers_data = []
    availability = 0
    cowin = CoWinAPI()
    available_centers = cowin.get_availability_by_district(district_id,date,min_age_limit)
    for center in available_centers['centers']:
        _date_capacity = 0
        available_sessions = []
        for session in center['sessions']:
            if(session['available_capacity'] >= 1):
                _date_capacity = 1
                availability = 1
                available_sessions.append(session)
        if(_date_capacity):
            center['sessions'] = available_sessions
            available_centers_data.append(center)
    if availability == 1:
        send_notification(available_centers_data)


def main():
    print("Checking centers for vaccination..........")
    while(True):
        check_for_vaccine()
        time.sleep(10) #can change this to how often you want to check.

main()
