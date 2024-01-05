from gebruikers import *
from evenementen import *
import json


def account_aanmaken_in_json(nieuwe_gebruiker):
    
    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)
        data[nieuwe_gebruiker.unieke_ID] = nieuwe_gebruiker.info_to_dict()
            
    with open("json/bezoekers.json", "w") as json_file:
        json.dump(data, json_file, indent=4)


def account_informatie_vinden_in_json(unieke_code):

    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)
        
        return data[unieke_code]
        

def gebruiker_instance_aanmaken_met_json_data(unieke_code):

    # gebruikers_data = account_informatie_vinden_in_json(unieke_code)
    # gebruikers_instance = Gebruiker.info_from_dict(gebruikers_data)
    # return gebruikers_instance
    # hieronder doet het zelfde maar korter / minder leesbaar lol
    
    return Gebruiker.info_from_dict(account_informatie_vinden_in_json(unieke_code))
    
    