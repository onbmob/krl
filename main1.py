#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from __future__ import division
import os
import zipfile
import threading
import time
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest

ZIP_URL = 'https://www.python.org/ftp/python/3.5.1/python-3.5.1-embed-win32.zip'
ZIP_FILENAME = 'Python351.zip'

kv_string = """
<RootWidget>
    BoxLayout:
        orientation: "vertical"
        Button:
            id: download_button
            text: "Download content"
            on_press: self.parent.parent.download_content()
        ProgressBar:
            id: download_progress_bar
            max: 1
            value: 0
"""

Builder.load_string(kv_string)


class RootWidget(BoxLayout):

    stop = threading.Event()    

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

    def download_content(self):
        self.ids["download_button"].disabled = True
        req = UrlRequest(ZIP_URL, on_progress=self.update_progress,
                         chunk_size=1024, on_success=self.unzip_content,
                         file_path=ZIP_FILENAME)

    def update_progress(self, request, current_size, total_size):
        self.ids['download_progress_bar'].value = current_size / total_size

    def unzip_content(self, req, result):
        threading.Thread(target=self.unzip_thread).start()

    def unzip_thread(self):
        print("Unzipping file")
        fh = open(ZIP_FILENAME, 'rb')
        z = zipfile.ZipFile(fh)
        ZIP_EXTRACT_FOLDER = ZIP_FILENAME + '_extracted'
        if not os.path.exists(ZIP_EXTRACT_FOLDER):
            os.makedirs(ZIP_EXTRACT_FOLDER)
        z.extractall(ZIP_EXTRACT_FOLDER)
        fh.close()
        os.remove(ZIP_FILENAME)
        time.sleep(4) # DEBUG: stretch out the unzip method to test threading

        print("Done")


class MyApp(App):

    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        self.root.stop.set()        

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MyApp().run()
