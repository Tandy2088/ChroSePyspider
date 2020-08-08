# -*- coding: utf-8 -*-
"""
selenium web driver for js fetcher

"""

import json
import time
import datetime
from flask import Flask, request

import sys 
sys.path.append("F:\GitHub\lib_ChromeReuse") # specify the location of ReUseForChrome.py
from ReUseForChrome import ReUse


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def handle_post():
    if request.method == 'GET':
        body = "method not allowed!"
        headers = {
            'Cache': 'no-cache',
            'Content-Length': len(body)
        }
        return body, 403, headers
    else:
        start_time = datetime.datetime.now()
        raw_data = request.get_data()
        fetch = json.loads(raw_data, encoding='utf-8')
        print('fetch=', fetch)

        result = {'orig_url': fetch['url'],
                  'status_code': 200,
                  'error': '',
                  'content': '',
                  'headers': {},
                  'url': '',
                  'cookies': {},
                  'time': 0,
                  'js_script_result': '',
                  'save': '' if fetch.get('save') is None else fetch.get('save')
                  }

        driver = InitWebDriver.get_web_driver(fetch)
        try:
            InitWebDriver.init_extra(fetch)
            if fetch.get('js_script') is not None :
                if fetch.get('js_script').get('1') is not None :
                    exec(fetch['js_script']['1'])

            driver.get(fetch['url'])

            if fetch.get('js_script') is not None :            
                if fetch.get('js_script').get('2') is not None :
                    exec(fetch['js_script']['2'])                

            time.sleep(2)
            result['url'] = driver.current_url
            result['content'] = driver.page_source
            result['cookies'] = _parse_cookie(driver.get_cookies())
        except Exception as e:
            result['error'] = str(e)
            result['status_code'] = 599
            print 'error'

        end_time = datetime.datetime.now()
        result['time'] = (end_time - start_time).seconds

        print('result=', result['url'])
        return json.dumps(result), 200, {
            'Cache': 'no-cache',
            'Content-Type': 'application/json',
        }


def _parse_cookie(cookie_list):
    if cookie_list:
        cookie_dict = dict()
        for item in cookie_list:
            cookie_dict[item['name']] = item['value']
        return cookie_dict
    return {}


class InitWebDriver(object):
    _web_driver = None

    @staticmethod
    def _init_web_driver(fetch):
        if InitWebDriver._web_driver is None:
            InitWebDriver._web_driver = ReUse()
            
    @staticmethod
    def get_web_driver(fetch):
        if InitWebDriver._web_driver is None:
            InitWebDriver._init_web_driver(fetch)
        return InitWebDriver._web_driver

    @staticmethod
    def init_extra(fetch):
        driver = InitWebDriver._web_driver
        if fetch.get('timeout'):
            driver.set_page_load_timeout(fetch.get('timeout'))
            driver.set_script_timeout(fetch.get('timeout'))
        else:
            driver.set_page_load_timeout(20)
            driver.set_script_timeout(20)


    @staticmethod
    def quit_web_driver():
        if InitWebDriver._web_driver is not None:
            InitWebDriver._web_driver.quit()


if __name__ == '__main__':
    app.run('0.0.0.0', 9000)
    InitWebDriver.quit_web_driver()
