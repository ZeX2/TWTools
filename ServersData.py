from PySide import QtCore, QtGui
from phpserialize import *
import requests
import json
import collections

servers = [
    "tribalwars.net",
    "die-staemme.de",
    "tribalwars.co.uk",
    "tribalwars.us",
    "tribalwars.se",
    "tribalwarsmasters.net",
    "tribalwars.nl",
    "staemme.ch",
    "plemiona.pl",
    "tribalwars.com.br",
    "tribalwars.com.pt",
    "divokekmeny.cz",
    "triburile.ro",
    "voyna-plemyon.ru",
    "fyletikesmaxes.gr",
    "tribalwars.no.com",
    "divoke-kmene.sk",
    "klanhaboru.hu",
    "tribalwars.dk",
    "tribals.it",
    "klanlar.org",
    "guerretribale.fr",
    "guerrastribales.es",
    "tribalwars.ae",
    "vojnaplemen.si",
    "plemena.com",
    "tribalwars.asia",
    "tribalwars.works"
]

backend = "/backend/get_servers.php"

def convert(data):
    if isinstance(data, bytes):  return data.decode('ascii')
    if isinstance(data, dict):   return collections.OrderedDict(map(convert, data.items()))
    if isinstance(data, tuple):  return map(convert, data)
    return data

class ServersDownloadThread(QtCore.QThread):
    
    def __init__(self, servers_json_path):
        QtCore.QThread.__init__(self)
        self.servers_json_path = servers_json_path

    def __del__(self):
        self.wait()
    
    def run(self):
        servers_dict = {}

        n = 1
        for server in servers:
            server_text = "Fetching " + server + " worlds:"
            self.emit(QtCore.SIGNAL("update_progress_text(PyObject)"), server_text)

            server_backend_url = "https://www." + server + backend

            try:
                r = requests.get(server_backend_url)
                r.raise_for_status()
            except requests.exceptions.ConnectionError:
                error_text = "Please check your internet connection. For further help contact the author. The program will now exit."
                self.emit(QtCore.SIGNAL("download_error(PyObject)"), error_text)
                return
            except requests.exceptions.Timeout:
                error_text = "The connection timed out. Please try again. The program will now exit."
                self.emit(QtCore.SIGNAL("download_error(PyObject)"), error_text)
                return
            except requests.exceptions.HTTPError as e:
                print(e)
                error_text = "An invalid HTTP response occured, check your internet connection. For further help contact the author. The program will now exit."
                self.emit(QtCore.SIGNAL("download_error(PyObject)"), error_text)
                return
            except requests.exceptions.RequestException as e:
                print(e)
                error_text = "An unknown network error occured, contact the author of the program on the Tribal Wars forums. The program will now exit."
                self.emit(QtCore.SIGNAL("download_error(PyObject)"), error_text)
                return

            php_object = loads(dumps(r.text), array_hook=collections.OrderedDict)
            worlds_dict = convert(unserialize(php_object, array_hook=collections.OrderedDict))

            for world_text in worlds_dict.keys():
                self.emit(QtCore.SIGNAL("update_progress_text(PyObject)"), world_text)

            servers_dict[server] = worlds_dict

            self.emit(QtCore.SIGNAL("update_progress_bar(PyObject)"), n)

            n += 1

        with open(self.servers_json_path, 'w') as f:
            json.dump(servers_dict, f, indent=4)
        
        self.emit(QtCore.SIGNAL("update_button()"))
        self.emit(QtCore.SIGNAL("update_progress_text(PyObject)"), "Done")