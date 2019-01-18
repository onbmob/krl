# -*- coding: utf-8 -*-

import os
import ast
import time

# from datetime import datetime

from kivy.app import App
from kivy import PY2
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.config import ConfigParser
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.network.urlrequest import UrlRequest
try:
    print('1====== result =import HTTPSConnection.')
    import ssl
    print('2====== result =import HTTPSConnection.')
    HTTPSConnection = None
    print('3====== result =import HTTPSConnection.')
    if PY2:
        from httplib import HTTPSConnection
    else:
        from http.client import HTTPSConnection
    print('4====== result =import HTTPSConnection.')
except ImportError:
    # depending the platform, if openssl support wasn't compiled before python,
    # this class is not available.
    print('====== result = HTTPSConnection is not available.')

if not PY2:
    Builder.load_string(open('ui.kv', encoding='utf-8').read())
else:
    Builder.load_file('ui.kv')

# def got_json(req, result):
#     str = ''
#     for key, value in result.items():
#         print('{}: {}'.format(key, value))
#         str+= '{}: {}'.format(key, value)
#   -----  Entry.ids.result_label.text = "Get:  " + str



class Entry(Screen):
    _app = ObjectProperty()

    def button_clicked(self, input_phone):
        print('1 '+input_phone)
        # req = UrlRequest('https://8move.com/api/check_phone/380675737597/?send_sms=true')
        # req = UrlRequest('https://8move.com//api/check_phone/'+input_phone+'/?send_sms=true')
        # req = UrlRequest('http://onbmob.com/check.txt',
        req = UrlRequest('https://8move.com/api/check_phone/380675737597/?send_sms=true',
                         on_success=self.got_json,
                         on_error=self.error_json,
                         on_failure=self.error_json,
                         on_progress=self.update_progress,
                         # req_body={"search_text": search_text, "num_results": 1},
                         method='GET',
                         req_headers={'User-Agent': 'Mozilla/5.0',
                                      'Content-Type': 'application/json'}
                                      # 'Authorization': self._get_auth()}
        # headers = {'Token': 'tArcrKZYxRTCWPvhTcdBqyydHZnxLCJB'}
                         )
        # req.wait()

    def update_progress(self, request, current_size, total_size):
        self.ids['download_progress_bar'].value = current_size / total_size

    def got_json(self, req, result):
        # print('2 result =', req.result)
        print('2 result =', req.result)
        print('3 error =', req.error)

        self.ids.result_label.text = "Get:  " + req.result['result']

        self._app.check_phone = ast.literal_eval(self._app.config.get('General', 'user_data'))
        for key, value in req.result.items():
            print('{}: {}'.format(key, value))
            self._app.check_phone[key] = value
        self._app.config.set('General', 'user_data', self._app.check_phone)
        self._app.config.write()


    def error_json(self, req, result):
        print('3 error =', req.error)

    # def search(self, search_text):
    #     header = {'Content-Type': 'application/json'}
    #     req = UrlRequest('http://127.0.0.1:5000/search',
    #                      req_body={"search_text": search_text, "num_results": 1},
    #                      on_success=Entry.got_json,
    #                      req_headers=header)
    #     print("Search method called")

class SortedListRoute(Screen):
    pass
    # def on_enter(self):
    #     data_foods = ast.literal_eval(
    #         App.get_running_app().config.get('General', 'user_data'))
    #     self.set_list_foods(data_foods)

    # def set_list_foods(self, data_foods):
    #     for f, d in sorted(data_foods.items(), key=lambda x: x[1]):
    #         fd = f.decode('u8') + ' ' + (datetime.fromtimestamp(d).strftime(
    #             '%Y-%m-%d'))
    #         data = {'viewclass': 'Button', 'text': fd}
    #         if data not in self.ids.rv.data:
    #             self.ids.rv.data.append({'viewclass': 'Button', 'text': fd})


class AddFood(Screen):
    _app = ObjectProperty()

    def set_user_data(self, input_food):
        self._app.user_data = ast.literal_eval(self._app.config.get('General', 'user_data'))
        self._app.user_data[input_food.encode('u8')] = int(time.time())

    def save_user_data(self):
        self._app.config.set('General', 'user_data', self._app.user_data)
        self._app.config.write()

    def set_new_food(self, name_food):
        # if not PY2:
        self.ids.result_label.text = "Последнее добавленное:  " + name_food
        # else:
        #     self.ids.result_label.text = \
        #         u"Последнее добавленное:  " + name_food

    def button_clicked(self, input_food):
        self.set_user_data(input_food)
        self.save_user_data()
        self.set_new_food(input_food)


class RouteListApp(App):
    def __init__(self, **kvargs):
        super(RouteListApp, self).__init__(**kvargs)

        self.config = ConfigParser()
        self.screen_manager = Factory.ManagerScreens()
        self.user_data = {}

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'user_data', '{}')

    def set_value_from_config(self):
        self.config.read(os.path.join(self.directory, '%(appname)s.ini'))
        self.user_data = ast.literal_eval(self.config.get(
            'General', 'user_data'))

    # def get_application_config(self, **kwargs):
    #     return super(RouteListApp, self).get_application_config(
    #         '{}/%(appname)s.ini'.format(self.directory))

    def get_application_config(self, **kwargs):
        from kivy.utils import platform
        if platform == 'android':
            config_path = os.path.join(os.environ['ANDROID_PRIVATE'], "%(appname)s.ini")
            return config_path
        return super(RouteListApp, self).get_application_config('{}/%(appname)s.ini'.format(self.directory))

    # def get_application_config(self, defaultpath="c:/temp/%(appname)s.ini"):
    #     from kivy.utils import platform
    #     from os.path import sep, expanduser
    #
    #     if platform == 'android':
    #         defaultpath = '/sdcard/.%(appname)s.ini'
    #     elif platform == 'ios':
    #         defaultpath = '~/Documents/%(appname)s.ini'
    #     elif platform == 'win':
    #         defaultpath = defaultpath.replace('/', sep)
    #
    #     return os.path.expanduser(defaultpath) % {
    #         'appname': self.name, 'appdir': self.directory}

    def build(self):
        return self.screen_manager


if __name__ == '__main__':
    RouteListApp().run()
