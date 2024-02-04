from gebruikers import *
from evenementen import *
import json

# alle functies die te maken hebben met het ophalen, aanmaken, wijzigen en verwijderen van data in de json files

def alle_gebruikers_informatie_ophalen():

    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)
        return data
    
def bezoekers_registratie_informatie_ophalen():
     
     with open("json/identificators.json", "r") as json_file:
        data = json.load(json_file)
        return data

def account_aanmaken_in_json(nieuwe_gebruiker):
    # de nieuwe gebruiker wordt toegevoegd aan de json file    
    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)
        # de unieke ID van de gebruiker wordt gebruikt als key in de dictionary van de json file    
        data[nieuwe_gebruiker.unieke_ID] = nieuwe_gebruiker.info_to_dict()
                
    with open("json/bezoekers.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

def gebruiker_informatie_zoeken(zoekterm):

    data = alle_gebruikers_informatie_ophalen()

    gevonden_data = {}

    # deze loop zoekt door alle mogelijke data van de gebruikers
    # en vergelijkt deze met de zoekterm, als de zoekterm gevonden wordt
    # wordt de data van de gebruiker toegevoegd aan de gevonden_data dictionary
    # hierdoor wordt uiteindelijk door de pagina alleen de gebruikers met relevante data getoond
    for gebruiker in data:
        for info in data[gebruiker]:
            if data[gebruiker][info] is not None and zoekterm in data[gebruiker][info]:
                gevonden_data[gebruiker] = data[gebruiker]
                break

    return gevonden_data


def account_informatie_vinden_in_json(unieke_code):
# de informatie van de gebruiker wordt gevonden in de json file met de unieke code als key en returned
    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)
        
        return data[unieke_code]
        
def account_informatie_wijzigen_in_json(unieke_code, te_wijzigen_data, verandering):

    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)

        try:
            data[unieke_code][te_wijzigen_data] = verandering
        except KeyError:
            return("Geen beschikbare data meegegeven als tweede argument voor 'account_informatie_wijzigen_in_json")
              
    with open("json/bezoekers.json", "w") as json_file:
        json.dump(data, json_file, indent=4)


def account_password_controle(unieke_ID, ingevoerd_password):

    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)
    # de ingevoerde password wordt vergeleken met het password van de gebruiker in de json file
    if data[unieke_ID]["password"] == ingevoerd_password:
        return True
    else:
        return False


def gebruiker_instance_aanmaken_met_json_data(unieke_code):
    # een nieuwe instance van een gebruiker class wordt aangemaakt met de informatie uit de json file en gereturned
    # dit maakt het mogelijk om de data van de gebruiker te gebruiken in de applicatie
    gebruikers_data = account_informatie_vinden_in_json(unieke_code)
    gebruikers_instance = Gebruiker.info_from_dict(gebruikers_data)
    return gebruikers_instance
    
       
def presentator_verificatie_code_opslaan_in_json(presentator_code):
    # de presentator verificatie code wordt opgeslagen in de json file
    with open("json/identificators.json", "r") as json_file:
        data = json.load(json_file)
        data["presentator_verificatie_code"] = str(presentator_code)       

    with open("json/identificators.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

def huidige_presentator_verificatie_code():
    # de huidige presentator verificatie code wordt opgehaald uit de json file
    with open("json/identificators.json", "r") as json_file:
        data = json.load(json_file)
        return data["presentator_verificatie_code"]        


def ingevoerde_presentator_code_verifieren(presentator_code):
    # de ingevoerde presentator code wordt vergeleken met de huidige presentator code
    with open("json/identificators.json", "r") as json_file:
        data = json.load(json_file)

        if presentator_code == data["presentator_verificatie_code"]:
            return True
        else:
            return False

def identificator_informatie_ophalen():
    # de identificator informatie wordt opgehaald uit de json file
    with open('json/identificators.json', 'r') as json_file:
        data = json.load(json_file)

    return data

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
        
    # deze functie splitst de tijd code string die door HTML gestuurd wordt op en om naar een dictionary.
    # dit maakt het ook mogelijk om de functie aan te roepen en alleen bepaalde delen van de tijd code te gebruiken;
    # door bijvoorbeeld "tijd_code_converten(tijd_code)['uur']" te gebruiken.
    # de structuur van een html tijd code is "YYYY-MM-DDTHH:MM" / "2023-12-31T23:59"
        return{
        'jaar': int(tijd_code[0:4]),
        'maand': int(tijd_code[5:7]),
        'dag': int(tijd_code[8:10]),
        'uur': int(tijd_code[11:13]),
        'minuten': int(tijd_code[14:])
        }


def evenementen_overlapping_controle(te_controleren_starttijd, te_controleren_eindtijd, te_controleren_locatie):
    # de te controleren starttijd en eindtijd worden omgezet naar een dictionary met tijd code_converten()
    start_tijd = tijd_code_converten(te_controleren_starttijd)
    eind_tijd = tijd_code_converten(te_controleren_eindtijd)

    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)
    
    # de loop controleert iedere eventenement in de json file op overlapping
    for event in data:

        event_locatie = data[event]["locatie"]
        # als de te controleeren locatie overeenkomt met de locatie van het event, wordt de tijd gecontroleerd
        if event_locatie == te_controleren_locatie:
            # de start en eind tijd van het evenement dat overeenkomt met het te controleren evenement worden omgezet naar een dictionary met tijd_code_converten()
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
            # dit controleert op een aantal voorwaarden:
            # - het jaar, maand en dag van het te controleren evenement zijn hetzelfde als het event uit de json file
            # - de starttijd van het te controleren evenement is eerder dan de eindtijd van het event uit de json file
            # - de eindtijd van het te controleren evenement is later dan de starttijd van het event uit de json file
            #
            # als aan deze voorwaarden voldaan wordt, is er een overlapping
            # de functie stopt en er wordt een lijst met informatie over het overlappende evenement teruggegeven
            # zodat deze getoond kan worden op de pagina
            # als de functie het gehele bestand heeft doorlopen en geen overlapping heeft gevonden, wordt er "False" teruggegeven, om aan te geven dat er geen overlapping is

    return False
    

def evenement_informatie_vinden_in_json(event_ID):

    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)
        
        return data[event_ID]
        

def evenement_instance_aanmaken_met_json_data(event_ID):
    # een nieuwe instance van een evenement class wordt aangemaakt met de informatie uit de json file en gereturned
    evenement_informatie = evenement_informatie_vinden_in_json(event_ID)
    nieuw_evenement = Evenement.info_from_dict(evenement_informatie)
    return nieuw_evenement

    

def evenement_verwijderen_in_json(event_ID):

    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)
        data.pop(event_ID)

    with open("json/evenementen.json", "w") as json_file:
        json.dump(data, json_file, indent=4)


    with open("json/bezoekers.json", "r") as bezoeker_file:
        bezoeker_data = json.load(bezoeker_file)
        # de loop controleert iedere gebruiker in de bezoekers.json file
        # als de gebruiker is ingeschreven voor het te verwijderen evenement, wordt deze uit de lijst van evenementen van de gebruiker verwijderd
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
    
    # de loop controleert iedere key in de dictionary die wordt meegegeven
    # als de key overeenkomt met een key in de json file, wordt de data van het evenement aangepast
    # de keys in de dictionary die wordt meegegeven komen altijd oveern met de keys in de json file
    # dit vereenvoudigt het aanpassen van de data
        
    for i in verander_data:
        data[event_ID][i] = verander_data[i]

    with open("json/evenementen.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
        
def evenement_informatie_zoeken_in_json(zoekterm):

    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)
    
    gevonden_evenementen_info = []

    # deze functie is een helper functie, die later in de functie gebruikt wordt om door een dictionary te zoeken
    # deze functie wordt alleen binnen de hoofdfunctie gebruikt, en is niet bedoeld om daar buiten te worden aangeroepen
    def dict_unpacker_helper(data, zoekterm):
        for key, value in data.items():
            if zoekterm in (key, value):
                return True
        return False

    # deze loop zoekt door alle mogelijke data van de evenementen
    for event in data:
        for info in data[event]:
            # als de data een integer is, wordt deze overgeslagen
            if type(data[event][info]) == int:
                continue
            # als de data een dictionary is, wordt de helper functie gebruikt om door de dictionary te zoeken
            if isinstance(data[event][info], dict):
                if dict_unpacker_helper(data[event][info], zoekterm):
                # als de helper functie True teruggeeft, wordt de data van het evenement toegevoegd aan de gevonden_evenementen_info lijst
                    gevonden_evenementen_info.append(data[event])
                    break

            if zoekterm in data[event][info]:
            # als de zoekterm in de data van het evenement gevonden wordt, wordt de data van het evenement toegevoegd aan de gevonden_evenementen_info lijst
                gevonden_evenementen_info.append(data[event])
                break

    return gevonden_evenementen_info                
            

def evenementen_ingeschreven_zoeken_in_json(unieke_ID):
    
    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)    

    gevonden_events = []
    # deze loop zoekt door alle evenementen in de json file
    # als de unieke ID van de gebruiker in de lijst van aanmeldingen van het evenement staat, wordt het evenement toegevoegd aan de gevonden_events lijst
    for event in data:
        if unieke_ID in data[event]["aanmeldingen"]:
            gevonden_events.append(data[event])

    return gevonden_events


def bezoeker_inschrijven_evenement_in_json(evenement_ID, bezoeker_ID):
    # de functie maakt een instance van de evenement en gebruiker class aan met de meegegeven ID's
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
    # de functie maakt een instance van de evenement en gebruiker class aan met de meegegeven ID's
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

    # als de bezoeker wordt uitgeschreven, wordt het aantal registraties in de identificators.json file aangepast
    data["unieke_registraties_totaal"] -= 1
    # de bevoegdheid van de gebruiker wordt gebruikt om het aantal registraties van de juiste bevoegdheid aan te passen
    if "A" in unieke_code:
        data["aantal_organisators_registraties"] -= 1
    elif "P" in unieke_code:
        data["aantal_presentators_registraties"] -= 1
    elif "G" in unieke_code:
        data["aantal_bezoekers_registraties"] -= 1

    with open("json/identificators.json", "w") as json_file:
        json.dump(data, json_file, indent=4)


def registratie_aantal_update_bij_bevoegdheid_wijziging(bevoegdheid):
    # als de bezoeker wordt uitgeschreven, wordt het aantal registraties in de identificators.json file aangepast

    with open("json/identificators.json", "r") as json_file:
        data = json.load(json_file)
    
    data["unieke_registraties_totaal"] -= 1

    # de bevoegdheid van de gebruiker wordt gebruikt om het aantal registraties van de juiste bevoegdheid aan te passen
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
    
    # een nieuwe_unieke_ID variabele wordt aangemaakt, die wordt gebruikt om de key van de dictionary van de gebruiker te veranderen
    # deze wordt eerst op None gezet, zodat de key van de dictionary van de gebruiker niet veranderd wordt als de gebruiker zijn bevoegdheid niet verandert
    nieuwe_unieke_ID = None

    # de loop controleert iedere key in de dictionary die wordt meegegeven
    for i in verander_data:
        # als de key overeenkomt met een key in de json file, wordt de data van de gebruiker aangepast
        data[bezoeker_ID][i] = verander_data[i]
            
        if i == "unieke_ID":
            nieuwe_unieke_ID = verander_data[i]
    # dit zorgt ervoor dat de key van de dictionary van de gebruiker hetzelfde als de de nieuwe "unieke_ID" is,
    # wanneer de gebruiker zijn bevoegdheid verandert
    if nieuwe_unieke_ID:
        data[nieuwe_unieke_ID] = data.pop(bezoeker_ID)

    with open("json/bezoekers.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    
                  
def presentator_lijst_uit_json_maken():

    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)
        
        presentator_lijst = []
        # de loop controleert iedere gebruiker in de json file
        # als de gebruiker een presentator is, wordt deze toegevoegd aan de presentator_lijst
        for bezoeker in data:
            if data[bezoeker]["bevoegdheid"] == 'presentator':
                presentator_lijst.append( { bezoeker:data[bezoeker]["naam"] } )
    
    return presentator_lijst
        
