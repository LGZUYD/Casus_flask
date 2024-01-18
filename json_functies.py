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
       


def evenement_aanmaken_in_json(nieuw_evenement):
   
    with open("json/identificators.json", "r") as json_file:
        ID_data = json.load(json_file)
        ID_data["evenementen"] += 1
                
    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)

        # Nieuw event aangemaakt met ID code om te zoeken
        # ID code van dat evenement wordt opgeslagen in event data zelf,
        # zodat je niet alleen op ID kunt zoeken, maar bv. op naam/presentator

        data[nieuw_evenement.event_ID] = nieuw_evenement.__evenement_informatie_to_dict__()
        # dit zorgt ervoor dat de key van de dictionary van het event hetzelfde als de "event_ID" is,
        # zodat het makkelijker te zoeken is. zelfde als bij bezoekers
        
    with open("json/evenementen.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    with open("json/identificators.json", "w") as json_file:
        json.dump(ID_data, json_file, indent=4)


def evenement_informatie_vinden_in_json(event_ID):

    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)
        
        return data[event_ID]
        

def evenement_instance_aanmaken_met_json_data(event_ID):
    # hetzelfde als bij gebruiker_instance_aanmaken_met_json_data(), daar uitgelegd
    return Evenement.info_from_dict(evenement_informatie_vinden_in_json(event_ID))


def evenement_informatie_wijzigen_in_json_data(event_ID, verander_data):
    
    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)
        
    for i in verander_data:
        data[event_ID][i] = verander_data[i]

    with open("json/evenementen.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    

def bezoeker_inschrijven_evenement_in_json(evenement_ID, bezoeker_ID):

    event_instance = evenement_instance_aanmaken_met_json_data(evenement_ID)
    gebruiker_instance = gebruiker_instance_aanmaken_met_json_data(bezoeker_ID)

    # gebruiker inschrijven in evenement object, als dit kan:
    if event_instance.bezoekers_aanmelding(gebruiker_instance):
        # evenement inschrijven in gebruiker object
        gebruiker_instance.__registreer_evenement__(event_instance)

    # gebruikers data naar json schrijven
    with open("json/bezoekers.json", "r") as gebruiker_file:
        gebruiker_data = json.load(gebruiker_file)
        gebruiker_data[gebruiker_instance.unieke_ID] = gebruiker_instance.info_to_dict()
    
    with open("json/bezoekers.json", "w") as gebruiker_file:
        json.dump(gebruiker_data, gebruiker_file, indent=4)
    
    
    # evenement data naar json schrijven
    with open("json/evenementen.json", "r") as event_file:
        event_data = json.load(event_file)
        event_data[event_instance.event_ID] = event_instance.__evenement_informatie_to_dict__()

    with open("json/evenementen.json", "w") as event_file:
        json.dump(event_data, event_file, indent=4)


def bezoeker_uitschrijven_evenement_in_json(evenement_ID, bezoeker_ID):

    event_instance = evenement_instance_aanmaken_met_json_data(evenement_ID)
    gebruiker_instance = gebruiker_instance_aanmaken_met_json_data(bezoeker_ID)

    # gebruiker inschrijven in evenement object
    event_instance.bezoeker_verwijderen(gebruiker_instance)
    # evenement uitschrijven bij gebruiker object
    gebruiker_instance.uitschrijven_evenement(event_instance)

    # gebruikers data naar json schrijven
    with open("json/bezoekers.json", "r") as gebruiker_file:
        gebruiker_data = json.load(gebruiker_file)
        gebruiker_data[gebruiker_instance.unieke_ID] = gebruiker_instance.info_to_dict()
    
    with open("json/bezoekers.json", "w") as gebruiker_file:
        json.dump(gebruiker_data, gebruiker_file, indent=4)
    
    
    # evenement data naar json schrijven
    with open("json/evenementen.json", "r") as event_file:
        event_data = json.load(event_file)
        event_data[event_instance.event_ID] = event_instance.__evenement_informatie_to_dict__()

    with open("json/evenementen.json", "w") as event_file:
        json.dump(event_data, event_file, indent=4)
    