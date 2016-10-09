import sys
from datetime import datetime
from os import path, environ, makedirs
from time import mktime, localtime
import requests
import json
from distutils.version import StrictVersion

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return path.join(sys._MEIPASS, relative_path)
    return path.join(path.abspath("."), relative_path)

def modified_time(file):
    mod_time = localtime(path.getmtime(file))
    return datetime.fromtimestamp(mktime(mod_time))

def app_data():
    """Creates APPDATA folder and returns the path
    """
    app_name = "ZeZes TWTools"
    if sys.platform == 'win32':
        app_data_path = path.join(environ['APPDATA'], app_name)
    else:
        app_data_path = appdirs.user_data_dir(app_name, "", roaming=True)
        #app_data_path = path.expanduser(path.join("~", "." + app_name))
    if not path.exists(app_data_path):
        makedirs(app_data_path)
    return app_data_path

def world_dir(app_data_path, url):
    url = url.replace("https://", "")
    world_directory = path.join(app_data_path, url)
    if not path.exists(world_directory):
        makedirs(world_directory)
    return world_directory

def update_needed(current_version):
    try:
        r = requests.get("https://api.github.com/repos/ZeX2/TWTools/releases/latest")
    except requests.exceptions.RequestException as e:
        print(e)
        return False

    json_data = json.loads(r.text)
    tag_name = json_data["tag_name"]
    latest_version = tag_name.replace("v", "")
    return StrictVersion(current_version) < StrictVersion(latest_version)
