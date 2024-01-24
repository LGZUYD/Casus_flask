import json
import math

def parkeerplaats_reserveren(unieke_code):

    with open('json/parkeerplaatsen.json', 'r') as json_file:
        bestaande_data = json.load(json_file)

    vrije_plaatsen = bestaande_data["totaal_parkeerplaatsen_gereserveerd"]
    parkeer_secties = []

    # 100 is hard coded, maar zou dus het aantal plaatsen per sectie moeten zijn
    aantal_plaatsen_per_sectie = 100

    parkeer_secties_index = math.floor(vrije_plaatsen / aantal_plaatsen_per_sectie)

    # alle mogelijke secties worden uit de json in list geplaatst zodat ze gebruikt kunnen worden
    for sectie in bestaande_data["secties"].keys():
        parkeer_secties.append(sectie)

    gereserveerde_plek_in_sectie = bestaande_data["totaal_parkeerplaatsen_gereserveerd"] % aantal_plaatsen_per_sectie
 
    # unieke gebruikers ID wordt toegewezen aan de parkeerplaats
    bestaande_data["secties"][parkeer_secties[parkeer_secties_index]][gereserveerde_plek_in_sectie] = unieke_code  
    
    bestaande_data["totaal_parkeerplaatsen_gereserveerd"] += 1

    with open('json/parkeerplaatsen.json', 'w') as json_file:
        json.dump(bestaande_data, json_file, indent=4)
    
    return f"{parkeer_secties[parkeer_secties_index]}{gereserveerde_plek_in_sectie}"

def parkeerplaats_vinden_op_unieke_code(unieke_code):

    with open('json/parkeerplaatsen.json', 'r') as json_file:
        bestaande_data = json.load(json_file)

    # iterate door secties
    for sectie in bestaande_data["secties"]:
        #iterate door parkeerplaatsen in secties
        for parkeerplaats in bestaande_data["secties"][sectie]:
            # als parkeerplaats houder overeenkomt met unieke_code, print de sectie + parkeernummer
            if bestaande_data["secties"][sectie][parkeerplaats] == unieke_code:
                return f"{sectie}{parkeerplaats}"
    
    return "Geen parkeerplaats gevonden voor deze ID code"
            
