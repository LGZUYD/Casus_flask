from gebruikers import *
from evenementen import *
import json


def alle_gebruikers_informatie_ophalen():

    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)
        return data
    
def bezoekers_registratie_informatie_ophalen():
     
     with open("json/identificators.json", "r") as json_file:
        data = json.load(json_file)
        return data

def account_aanmaken_in_json(nieuwe_gebruiker):
    
    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)    
        data[nieuwe_gebruiker.unieke_ID] = nieuwe_gebruiker.info_to_dict()
                
    with open("json/bezoekers.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

def gebruiker_informatie_zoeken(zoekterm):

    data = alle_gebruikers_informatie_ophalen()

    gevonden_data = {}

    for gebruiker in data:
        for info in data[gebruiker]:
            if data[gebruiker][info] is not None and zoekterm in data[gebruiker][info]:
                gevonden_data[gebruiker] = data[gebruiker]
                break

    return gevonden_data


def account_informatie_vinden_in_json(unieke_code):

    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)
        
        return data[unieke_code]
        
def account_informatie_wijzigen_in_json(unieke_code, te_wijzigen_data, verandering):
      
    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)
        
        try:
            data[unieke_code][te_wijzigen_data] = verandering
        except KeyError:
            print("Geen beschikbare data meegegeven als tweede argument voor 'account_informatie_wijzigen_in_json")
            return
              
    with open("json/bezoekers.json", "w") as json_file:
        json.dump(data, json_file, indent=4)


def account_password_controle(unieke_ID, ingevoerd_password):

    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)
    
    if data[unieke_ID]["password"] == ingevoerd_password:
        return True
    else:
        return False


def gebruiker_instance_aanmaken_met_json_data(unieke_code):

    # gebruikers_data = account_informatie_vinden_in_json(unieke_code)
    # gebruikers_instance = Gebruiker.info_from_dict(gebruikers_data)
    # return gebruikers_instance
    # hieronder doet het zelfde maar korter / minder leesbaar lol
    
    return Gebruiker.info_from_dict(account_informatie_vinden_in_json(unieke_code))
       
def presentator_verificatie_code_opslaan_in_json(presentator_code):
    
    with open("json/identificators.json", "r") as json_file:
        data = json.load(json_file)
        data["presentator_verificatie_code"] = str(presentator_code)       

    with open("json/identificators.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

def huidige_presentator_verificatie_code():
    
    with open("json/identificators.json", "r") as json_file:
        data = json.load(json_file)
        return data["presentator_verificatie_code"]        


def ingevoerde_presentator_code_verifieren(presentator_code):
    
    with open("json/identificators.json", "r") as json_file:
        data = json.load(json_file)

        if presentator_code == data["presentator_verificatie_code"]:
            return True
        else:
            return False

    

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



def tijd_code_converten(tijd_code):

        return{
        'jaar': int(tijd_code[0:4]),
        'maand': int(tijd_code[5:7]),
        'dag': int(tijd_code[8:10]),
        'uur': int(tijd_code[11:13]),
        'minuten': int(tijd_code[14:])
        }


def evenementen_overlapping_controle(te_controleren_starttijd, te_controleren_eindtijd, te_controleren_locatie):
    
    start_tijd = tijd_code_converten(te_controleren_starttijd)
    eind_tijd = tijd_code_converten(te_controleren_eindtijd)

    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)

    for event in data:

        event_locatie = data[event]["locatie"]

        if event_locatie == te_controleren_locatie:
            
            event_start_tijd = tijd_code_converten(data[event]['startTijd'])
            event_eind_tijd = tijd_code_converten(data[event]['eindTijd'])
            
            if (event_eind_tijd['jaar'] == start_tijd['jaar'] and
                event_eind_tijd['maand'] == start_tijd['maand'] and
                event_eind_tijd['dag'] == start_tijd['dag'] and
                ((event_eind_tijd['uur'] > start_tijd['uur']) or
                (event_eind_tijd['uur'] == start_tijd['uur'] and
                event_eind_tijd['minuten'] >= start_tijd['minuten'])) and
                ((event_start_tijd['uur'] < eind_tijd['uur']) or
                (event_start_tijd['uur'] == eind_tijd['uur'] and
                event_start_tijd['minuten'] <= eind_tijd['minuten']))):
                
                return [event, event_locatie, event_start_tijd, event_eind_tijd]

    return False
    

def evenement_informatie_vinden_in_json(event_ID):

    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)
        
        return data[event_ID]
        

def evenement_instance_aanmaken_met_json_data(event_ID):
    # hetzelfde als bij gebruiker_instance_aanmaken_met_json_data(), daar uitgelegd
    return Evenement.info_from_dict(evenement_informatie_vinden_in_json(event_ID))

def evenement_verwijderen_in_json(event_ID):

    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)
        data.pop(event_ID)

    with open("json/evenementen.json", "w") as json_file:
        json.dump(data, json_file, indent=4)


    with open("json/bezoekers.json", "r") as bezoeker_file:
        bezoeker_data = json.load(bezoeker_file)

        for gebruiker in bezoeker_data:
            if event_ID in bezoeker_data[gebruiker]["evenementen"]:
                bezoeker_data[gebruiker]["evenementen"].remove(event_ID)

    with open("json/bezoekers.json", "w") as bezoeker_file:
        json.dump(bezoeker_data, bezoeker_file, indent=4)

    with open("json/identificators.json", "r") as json_file:
        data = json.load(json_file)
        data["evenementen"] -= 1

    with open("json/identificators.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

def evenement_informatie_wijzigen_in_json_data(event_ID, verander_data):
    
    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)
        
    for i in verander_data:
        data[event_ID][i] = verander_data[i]

    with open("json/evenementen.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
        
def evenement_informatie_zoeken_in_json(zoekterm):

    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)
    
    gevonden_evenementen_info = []

    def dict_unpacker_helper(data, zoekterm):
        for key, value in data.items():
            if zoekterm in (key, value):
                return True
        return False

    for event in data:
        for info in data[event]:

            if type(data[event][info]) == int:
                continue

            if isinstance(data[event][info], dict):
                if dict_unpacker_helper(data[event][info], zoekterm):
                    gevonden_evenementen_info.append(data[event])
                    break

            if zoekterm in data[event][info]:
                gevonden_evenementen_info.append(data[event])
                break

    return gevonden_evenementen_info                
            

def evenementen_ingeschreven_zoeken_in_json(unieke_ID):
    
    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)    

    gevonden_events = []

    for event in data:
        if unieke_ID in data[event]["aanmeldingen"]:
            gevonden_events.append(data[event])

    return gevonden_events


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

    # gebruiker uitschrijven in evenement object
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


def bezoeker_verwijderen_in_json(unieke_code):
    
    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)
        
    with open("json/bezoekers.json", "w") as json_file:
        del data[unieke_code]
        json.dump(data, json_file,indent=4)

    with open("json/identificators.json", "r") as json_file:
        data = json.load(json_file)

    data["unieke_registraties_totaal"] -= 1
    
    if "A" in unieke_code:
        data["aantal_organisators_registraties"] -= 1
    elif "P" in unieke_code:
        data["aantal_presentators_registraties"] -= 1
    elif "G" in unieke_code:
        data["aantal_bezoekers_registraties"] -= 1

    with open("json/identificators.json", "w") as json_file:
        json.dump(data, json_file, indent=4)


def registratie_aantal_update_bij_bevoegdheid_wijziging(bevoegdheid):

    with open("json/identificators.json", "r") as json_file:
        data = json.load(json_file)

    data["unieke_registraties_totaal"] -= 1

    if "A" in bevoegdheid:
        data["aantal_organisators_registraties"] -= 1
    elif "P" in bevoegdheid:
        data["aantal_presentators_registraties"] -= 1
    elif "G" in bevoegdheid:
        data["aantal_bezoekers_registraties"] -= 1
        
    with open("json/identificators.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    
     
def bezoeker_informatie_wijzigen_in_json_data(bezoeker_ID, verander_data):
    
    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)
    
    nieuwe_unieke_ID = None

    for i in verander_data:
        
        data[bezoeker_ID][i] = verander_data[i]
            
        if i == "unieke_ID":
            nieuwe_unieke_ID = verander_data[i]

    if nieuwe_unieke_ID:
        data[nieuwe_unieke_ID] = data.pop(bezoeker_ID)

    with open("json/bezoekers.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    
                  
def presentator_lijst_uit_json_maken():

    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)
        
        presentator_lijst = []

        for bezoeker in data:
            if data[bezoeker]["bevoegdheid"] == 'presentator':
                presentator_lijst.append( { bezoeker:data[bezoeker]["naam"] } )
    
    return presentator_lijst
        
