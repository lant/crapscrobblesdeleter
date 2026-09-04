#!/usr/bin/python

import argparse
import hashlib
import json
import sys
import time
import os
import requests
from rich.console import Console
from rich.prompt import Confirm
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

api_key = os.getenv("LAST_API")
username = os.getenv("LAST_USERNAME")

BASE_URL="https://ws.audioscrobbler.com/2.0/"
ENDPOINT="?method=user.getrecenttracks&user="+username+"&api_key="+api_key+"&format=json"

def build_delete_url(artist):
    return "http://www.last.fm/user/"+username+"/library/music/"+artist.replace(' ','+')

with open("whitelist.json", "r") as file:
    whitelisted_artists = json.load(file)

with open("blacklist.json", "r") as file:
    blacklisted_artists = json.load(file)

to_delete_urls = set()
console = Console()

current_page = 0
next_one = Confirm.ask("Should we go for page: "+str(current_page) + " ? ")

while next_one:
    endpoint = ""
    if current_page == 0:
        endpoint = BASE_URL+ENDPOINT
    else:
        endpoint = BASE_URL+ENDPOINT+"&page="+str(current_page)

    r = requests.get(endpoint)
    r.raise_for_status()

    tracks = r.json()['recenttracks']['track']
    page = r.json()['recenttracks']['@attr']['page']

    for track in tracks:
        artist = track['artist']['#text']
        if artist in whitelisted_artists:
            console.print("[green]"+artist + " is whitelisted, all good[/green]")
        elif artist in blacklisted_artists:
            st = artist + " is blacklisted, adding it to the crap to delete"
            console.print(st)
            to_delete_urls.add(build_delete_url(artist))
        else:
            good = Confirm.ask("Is '" + artist + "' good?")
            if good:
                whitelisted_artists.append(artist)
                with open("whitelist.json", "w") as file:
                    json.dump(whitelisted_artists, file)
            else:
                blacklisted_artists.append(artist)
                to_delete_urls.add(build_delete_url(artist))
                with open("blacklist.json", "w") as file:
                    json.dump(blacklisted_artists, file)

    current_page = current_page + 1
    next_one = Confirm.ask("Should we go for page: "+str(current_page) + " ? ")


with open("to_delete.txt", "w") as file:
    for crap in to_delete_urls:
        file.write(f"{crap}\n")


console.print("...Done")
