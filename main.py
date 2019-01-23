# -*- coding: utf-8 -*-

import os
import ast
# import time
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
    import ssl
    HTTPSConnection = None
    if PY2:
        from httplib import HTTPSConnection
    else:
        from http.client import HTTPSConnection
except ImportError:
    print('= error = HTTPSConnection is not available.')

if not PY2:
    Builder.load_string(open('ui.kv', encoding='utf-8').read())
else:
    Builder.load_file('ui.kv')

class Entry(Screen):
    _app = ObjectProperty()

    def button_clicked(self):
        input_phone = self.ids['field_phone'].text
        print('1 ', input_phone)
        self.ids['phone_label'].text = u"Телефон:  " + input_phone
        # UrlRequest('https://8move.com//api/check_phone/'+input_phone+'/?send_sms=true',
        UrlRequest('https://8move.com/api/check_phone/380675737597/?send_sms=true',
                         on_success=self.got_json,
                         on_error=self.error_json,
                         on_failure=self.error_json,
                         on_progress=self.update_progress,
                         method='GET',
                         req_headers={'User-Agent': 'Mozilla/5.0',
                                      'Content-Type': 'application/json'}
                         )

    def update_progress(self, request, current_size, total_size):
        self.ids['download_progress_bar'].value = current_size / total_size

    def got_json(self, req, result):
        print('req.result =', req.result)
        print('result =', result)
        print('error =', req.error)

        self.ids.result_label.text = "Get:  " + req.result['result']

        user_data = {}
        if req.result['result'] == 'OK':
            user_data = ast.literal_eval(self._app.config.get('General', 'user_data'))
            user_data['driver_phone'] = req.result['driver_phone']
            user_data['manager_phone'] = req.result['manager_phone']
            user_data['first_name'] = req.result['first_name']
            user_data['last_name'] = req.result['last_name']
            user_data['avatar'] = req.result['avatar']
        # user_data = ast.literal_eval(self._app.config.get('General', 'user_data'))
        # for key, value in req.result.items():
        #     print('{}: {}'.format(key, value))
        #     user_data = ast.literal_eval(self._app.config.get('General', 'user_data'))
        self._app.config.set('General', 'user_data', user_data)
        self._app.config.write()
        self._app.screen_manager.current = 'entry_pincode'

    def error_json(self, req, result):
        print('error =', req.error)

class EntryPincode(Screen):
    _app = ObjectProperty()

    def button_clicked(self):
        print('1 ')
        input_phone = self.ids['field_phone'].text
        print('1 ', input_phone)
        self.ids['phone_label'].text = u"Пинкод:  " + input_phone
        user_data = ast.literal_eval(self._app.config.get('General', 'user_data'))
        import json
        req_body = json.dumps({"phone": user_data['driver_phone'], "pin": input_phone})
        UrlRequest('https://8move.com/api/check_pin_auth/',
                         on_success=self.got_json,
                         on_error=self.error_json,
                         on_failure=self.error_json,
                         on_progress=self.update_progress,
                         req_body=req_body,
                         method='POST',
                         req_headers={'User-Agent': 'Mozilla/5.0',
                                      'Content-Type': 'application/json'}
                                      # 'Authorization': self._get_auth()}
        # headers = {'Token': 'tArcrKZYxRTCWPvhTcdBqyydHZnxLCJB'}
                         )
        # req.wait()

    def update_progress(self, request, current_size, total_size):
        self.ids['download_progress_bar'].value = current_size / total_size

    def got_json(self, req, result):
        print('req.result =', req.result)
        print('result =', result)
        print('error =', req.error)

        self.ids.result_label.text = u"Get:  "

        user_data = ast.literal_eval(self._app.config.get('General', 'user_data'))
        for key, value in req.result.items():
            print('{}: {}'.format(key, value))
            user_data[key] = value
        self._app.config.set('General', 'user_data', user_data)
        self._app.config.write()
        UrlRequest('https://8move.com/api/check_authentication/',
                   on_success=self.got_json_act,
                   on_error=self.error_json,
                   on_failure=self.error_json,
                   on_progress=self.update_progress,
                   method='GET',
                   req_headers={'User-Agent': 'Mozilla/5.0',
                                'Content-Type': 'application/json',
                                # 'Authorization': 'Token',
                                'Authorization': 'Token ' + user_data['token']}
                   )

    def error_json(self, req, result):
        print('error =', req.error)

    def got_json_act(self, req, result):
        # print('check_authentication req.result =', req.result)
        print('check_authentication result =', result)
        print('check_authentication error =', req.error)

        self.ids.result_label.text = "OK"

        user_data = ast.literal_eval(self._app.config.get('General', 'user_data'))
        # for key, value in req.result.items():
            # print('{}: {}'.format(key, value))
            # user_data[key] = value.encode('utf-8')
        user_data['first_name'] =  req.result['first_name'].encode('u8')
        user_data['last_name'] =  req.result['last_name'].encode('u8')
        user_data['organization'] =  req.result['organization'].encode('u8')
        user_data['user_id'] =  req.result['user_id']
        user_data['show_move'] =  req.result['show_move']

        self._app.config.set('General', 'user_data', user_data)
        self._app.config.write()
        self._app.screen_manager.current = 'menu'

class ShowUserData(Screen):

    def on_enter(self):
        
        user_data = ast.literal_eval(App.get_running_app().config.get('General', 'user_data'))
    #     for f, d in sorted(data_foods.items(), key=lambda x: x[1]):
            # fd = f.decode('u8') + ' ' + (datetime.fromtimestamp(d).strftime('%Y-%m-%d'))

        # for f, d in user_data.items():
        #     fd = f + ' = ' + d.decode('u8')
        #     print (str(fd))
        #     data = {'viewclass': 'Button', 'text': fd}
        #     if data not in self.ids.rv.data:
        #         self.ids.rv.data.append({'viewclass': 'Button', 'text': fd})
        if 'user_id' in user_data:
            self.ids.rv.data.append({'viewclass': 'Button', 'text': u'ID водителя '+ str(user_data['user_id'])})
            self.ids.rv.data.append({'viewclass': 'Button', 'text': u'Организация '+ user_data['organization'].decode('u8')})
            self.ids.rv.data.append({'viewclass': 'Button', 'text': u'Имя водителя '+ user_data['first_name'].decode('u8') + user_data['last_name'].decode('u8')})
            self.ids.rv.data.append({'viewclass': 'Button', 'text': u'Телефон '+ user_data['driver_phone']})



# class Pref():
#
#     def __init__(self):
#         self.data = ast.literal_eval(App.get_running_app().config.get('General', 'user_data'))
#
#     def get_data(self, key):
#         return self.data[key]
#
#     def set_data(self, key, val):
#         self.data[key] = val
#
#     def save(self):
#         self._app.config.set('General', 'user_data', self.data)
#         self._app.config.write()
#
#     def refresh(self):
#         self.data = ast.literal_eval(App.get_running_app().config.get('General', 'user_data'))

class RouteListApp(App):


    def __init__(self, **kvargs):
        super(RouteListApp, self).__init__(**kvargs)
        self.config = ConfigParser()
        self.screen_manager = Factory.ManagerScreens()
        # self.user_data = {}

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'user_data', '{}')

    # def set_value_from_config(self):
    #     self.config.read(os.path.join(self.directory, '%(appname)s.ini'))
    #     self.user_data = ast.literal_eval(self.config.get('General', 'user_data'))

    def get_application_config(self, **kwargs):
        from kivy.utils import platform
        if platform == 'android':
            config_path = os.path.join(os.environ['ANDROID_PRIVATE'], "%(appname)s.ini")
            return config_path
        return super(RouteListApp, self).get_application_config('{}/%(appname)s.ini'.format(self.directory))

    def build(self):
        # self.pref = Pref()
        return self.screen_manager


# class AddFood(Screen):
#     _app = ObjectProperty()
#
#     def set_user_data(self, input_food):
#         self._app.user_data = ast.literal_eval(self._app.config.get('General', 'user_data'))
#         self._app.user_data[input_food.encode('u8')] = int(time.time())
#
#     def save_user_data(self):
#         self._app.config.set('General', 'user_data', self._app.user_data)
#         self._app.config.write()
#
#     def set_new_food(self, name_food):
#         if not PY2:
        # self.ids.result_label.text = "Последнее добавленное:  " + name_food
        # else:
        #     self.ids.result_label.text = \
        #         u"Последнее добавленное:  " + name_food
    #
    # def button_clicked(self, input_food):
    #     self.set_user_data(input_food)
    #     self.save_user_data()
    #     self.set_new_food(input_food)

if __name__ == '__main__':
    RouteListApp().run()
