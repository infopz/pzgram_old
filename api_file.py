import requests
import time
from .ExceptionFile import *


def api_request(key, method, p=None, timeout=3):
    while True:
        try:
            data = requests.get("https://api.telegram.org/bot"+key+"/"+method, params=p,timeout=timeout)
        except Exception as e:
            print('API_Request - Requests error: Retry')
            time.sleep(0.5)
            continue
        status_code = data.status_code
        data = data.json()
        if status_code == 200:
            return data
        else:
            action, rdata = recognize_error(status_code, data)
            if action == 'continue':
                return "apiError"+str(rdata)
            elif action == 'stop':
                raise StopBot(rdata)
            elif action == 'retry':
                time.sleep(rdata)


def recognize_error(code, data):
    error_description = ''
    try:
        error_description = data['description']
    except KeyError:
        pass
    if code == 400:
        print('API_Request - BadRequest Error ' + error_description)
        return 'continue', 400
    elif code == 401:
        print('API_Request - BotKey Error ' + error_description)
        return 'stop', 'API_Request - BotKey Error ' + error_description
    elif code == 403:
        print('API_Request - Privacy Error ' + error_description)
        return 'continue', 403
    elif code == 404:
        print('API_Request - NotFound Error ' + error_description)
        return 'continue', 404
    elif code == 409:
        print('API_Request - AnotherInstance Error - Retry in 3s')
        return 'retry', 3
    elif code == 420:
        second = error_description.split('_')[2]  # FLOOD_WAIT_X
        print('API_Request - TooMuchMessage Error - Retry in ' + second)
        return 'retry ', int(second)
    elif code == 500:
        print('API_Request - TelegramInternal Error')
        return 'continue', 500
    else:
        print('API_Request - ' + error_description)
        return 'continue', code
