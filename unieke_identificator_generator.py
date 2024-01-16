import json

def unieke_registratie_code_generator(bevoegdheid):

    with open('json/identificators.json', 'r') as json_file:
        bestaande_data = json.load(json_file)

    unieke_gebruikers_bevoegdheid_code = ""
    
    # iedere keer als functie geroepen wordt gaat het totaal aantal registraties van alle aanwezigen +1
    bestaande_data['unieke_registraties_totaal'] += 1

    match bevoegdheid:
        
        case "bezoeker":
            # 'G' voor guest
            unieke_gebruikers_bevoegdheid_code = "G-"
            unieke_gebruikers_bevoegdheid_code += str(bestaande_data['aantal_bezoekers_registraties'])
            bestaande_data['aantal_bezoekers_registraties'] +=1
        case "presentator":
            # 'P' voor presentator
            unieke_gebruikers_bevoegdheid_code = "P-"
            unieke_gebruikers_bevoegdheid_code += str(bestaande_data['aantal_presentators_registraties'])
            bestaande_data['aantal_presentators_registraties'] +=1
        case "beheerder":
            # 'A' for administrator
            unieke_gebruikers_bevoegdheid_code = "A-"
            unieke_gebruikers_bevoegdheid_code += str(bestaande_data['aantal_organisators_registraties'])
            bestaande_data['aantal_organisators_registraties'] += 1
        
    # 'match - case' is een andere manier van 'if'-statements schrijven, dat voor dit geval makkelijker te lezen is;
    # hieronder staat hoe je deze code zou schrijven als je 'if'-statements zou gebruiken, maar de werking is precies hetzelfde. 
    # -----------------
    # if bevoegdheid == "bezoeker":
    #    # 'G' voor guest
    #    unieke_gebruikers_bevoegdheid_code = "G-"
    #    /etc.../
    # elif bevoegheid == "presentator":
    #   # 'P' voor presentator
    #    unieke_gebruikers_bevoegdheid_code = "P-"
    #   /etc.../
    # elif bevoegdheid == "beheerder":
    #   # 'A' for administrator
    #   unieke_gebruikers_bevoegdheid_code = "A-"
    #   /etc.../
    # -------------------

    with open('json/identificators.json', 'w') as json_file:
        json.dump(bestaande_data, json_file, indent=4)

    return unieke_gebruikers_bevoegdheid_code

    

