import requests
import time
from .ExceptionFile import *


def api_request(httpmethod, key, method, p=None, timeout=3, files=None):
    from .Bot_Class import print_time
    while True:
        try:
            if httpmethod == "GET":
                data = requests.get("https://api.telegram.org/bot"+key+"/"+method, params=p, timeout=timeout)
            else:
                data = requests.post("https://api.telegram.org/bot"+key+"/"+method, params=p, files=files, timeout=timeout)
        except Exception as e:
            print(print_time() + 'API_Request - Requests error: Retry')
            time.sleep(0.5)
            continue
        status_code = data.status_code
        try:
            data = data.json()
        except:
            print(print_time() + "API_Request - JSON Error: Retry")
            print(data)
            continue
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
    from .Bot_Class import print_time
    error_description = ''
    try:
        error_description = data['description']
    except KeyError:
        pass
    if code == 400:
        print(print_time() + 'API_Request - BadRequest Error ' + error_description)
        return 'continue', 400
    elif code == 401:
        print(print_time() + 'API_Request - BotKey Error ' + error_description)
        return 'stop', 'API_Request - BotKey Error ' + error_description
    elif code == 403:
        print(print_time() + 'API_Request - Privacy Error ' + error_description)
        return 'continue', 403
    elif code == 404:
        print(print_time() + 'API_Request - NotFound Error ' + error_description)
        return 'continue', 404
    elif code == 409:
        print(print_time() + 'API_Request - AnotherInstance Error - Retry in 3s')
        return 'retry', 3
    elif code == 420:
        second = error_description.split('_')[2]  # FLOOD_WAIT_X
        print(print_time() + 'API_Request - TooMuchMessage Error - Retry in ' + second)
        return 'retry ', int(second)
    elif code == 500:
        print(print_time() + 'API_Request - TelegramInternal Error')
        return 'continue', 500
    else:
        print(print_time() + 'API_Request - ' + error_description)
        return 'continue', code
