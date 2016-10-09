import urllib.parse
import requests
import gzip
import sys
from os import path
import xml.etree.ElementTree as ET

import appdirs

class TWData(object):
    
    def download_data(path, url):
        villages_url = url + "/map/village.txt.gz"
        players_url = url + "/map/player.txt.gz"
        config_url = url + "/interface.php?func=get_config"
        url = url.replace("https://", "")

        """Village data"""
        villages_save = path + "\\" + "village.txt.gz"
        with open(villages_save, "wb") as f:
            response = requests.get(villages_url, stream=True)
            response.raise_for_status()
            if not response.ok:
                pass
            for block in response.iter_content(1024):
                f.write(block)

        """Player data"""
        players_save = path + "\\" + "player.txt.gz"
        with open(players_save, "wb") as f:
            response = requests.get(players_url, stream=True)
            response.raise_for_status()
            if not response.ok:
                pass
            for block in response.iter_content(1024):
                f.write(block)

        """Config"""
        config_save = path + "\\" + "config.xml"
        with open(config_save, "wb") as f:
            response = requests.get(config_url, stream=True)
            response.raise_for_status()
            if not response.ok:
                pass
            for block in response.iter_content(1024):
                f.write(block)

    def get_speed_data(xml_file):
        servers = ET.parse(xml_file).getroot()
        world_speed = servers.find(".//speed").text
        unit_speed = servers.find(".//unit_speed").text
        return [world_speed, unit_speed]

    def get_villages_dict(villages_data):
        # Villages dict to be returned
        villages_dict = {}

        # Opens the data file (.txt.gz) and splits it into an array based on
        # each line
        with gzip.open(villages_data) as f:
            data = f.read()
            villages_list = data.splitlines()

            # Each line in the array has data about the villages in the format:
            # "id, name, x, y, player, points"
            for village in villages_list:
                # Decodes each line and splits the data into an array
                village_decoded = village.decode("utf-8")
                village_array = village_decoded.split(",")

                village_id = village_array[0]
                village_name = village_array[1]
                village_name = urllib.parse.unquote_plus(village_name)
                village_x = village_array[2]
                village_y = village_array[3]
                village_player_id = village_array[4]
                village_points = village_array[5]

                # Array which consists of a villages data
                village_array = [
                    village_id,
                    village_name,
                    village_x,
                    village_y,
                    village_player_id,
                    village_points]
                # Adds each village to the villages dict
                villages_dict[int(village_id)] = village_array
        return villages_dict

    def get_players_dict(players_data):
        players_dict = {}

        with gzip.open(players_data) as f:
            data = f.read()
            players_list = data.splitlines()

            for player in players_list:
                player_decoded = player.decode("utf-8")
                player_array = player_decoded.split(",")

                player_id = player_array[0]
                player_name = player_array[1]
                player_name = urllib.parse.unquote_plus(player_name)
                player_ally_id = player_array[2]
                player_villages = player_array[3]
                player_points = player_array[4]
                player_rank = player_array[5]

                player_array = [
                    player_id,
                    player_name,
                    player_ally_id,
                    player_villages,
                    player_points,
                    player_rank]
                players_dict[int(player_id)] = player_array
        return players_dict
