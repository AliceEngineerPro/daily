# coding: utf8
""" 
@File: watchdog_file.py
@Author: Alice(From Chengdu.China)
@HomePage: https://github.com/AliceEngineerPro
@CreatedTime: 2022/9/4 18:57
"""
import time
import os
from watchdog.events import *
from watchdog.observers import Observer


SRC_PATH = r''
TAG_PATH = r''


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_created(self, event):
        if event.is_directory:
            pass
        else:
            path = os.path.abspath(event.src_path)
            print(f'mv {path} {TAG_PATH}')


if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, SRC_PATH, True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
