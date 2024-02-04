import json
import unieke_identificator_generator
import parkeerplaats_functies

class Gebruiker:
    # bij de eerste keer aanmaken van een instance van de class wordt door de gebruiker alleen naam en password ingevoerd.
    # de rest van de informatie wordt automatisch gegenereerd of toegevoegd.
    # daarom worden de andere argumenten op None gezet, zodat ze niet verplicht zijn om in te voeren.
    def __init__(self, naam, password, parkeerplaats=None, evenementen=None, bevoegdheid="bezoeker", unieke_code=None):
    
        # alle mogelijke informatie wordt opgeslagen in de instance van de class
        self.naam = naam
        self.password = password
        self.parkeerplaats = parkeerplaats
        self.geregistreerde_evenementen = evenementen or []
        self.bevoegdheid = bevoegdheid
        
        self.unieke_ID = unieke_code or unieke_identificator_generator.unieke_registratie_code_generator(self.bevoegdheid)
        # dit zorgt ervoor dat bij het aanmaken van de instance een unieke code wordt gegenereerd,
        # omdat er geen argument wordt meegegeven de eerste keer,
        # als de instance daarna opnieuw wordt aan gemaakt met een unieke code, wordt deze gebruikt.

         
    def __parkeerplaats_reserveren__(self):
        # als de gebruiker nog geen parkeerplaats heeft, kan deze worden gereserveerd
        if self.parkeerplaats == None:
            self.parkeerplaats = parkeerplaats_functies.parkeerplaats_reserveren(self.unieke_ID)
        return
            
    
    def __registreer_evenement__(self, evenement):
        if evenement.event_ID not in self.geregistreerde_evenementen:
            self.geregistreerde_evenementen.append(evenement.event_ID)

    def uitschrijven_evenement(self, evenement):
        if evenement.event_ID in self.geregistreerde_evenementen:
            self.geregistreerde_evenementen.remove(evenement.event_ID)
        
            
    def info_to_dict(self):
        # alle informatie over de gebruiker wordt verzameld om deze uit te lezen of naar json te verwerken
        return {
            'naam':self.naam,
            'password':self.password,
            'parkeerplaats': self.parkeerplaats,
            'evenementen': self.geregistreerde_evenementen,
            'bevoegdheid': self.bevoegdheid,
            'unieke_ID': self.unieke_ID
            }
        
    # met een @classmethod kan je een instance maken van een class met een dictionary als argument,
    # dit is handig om data uit een json file te halen en om te zetten naar een instance van een class
    @classmethod
    def info_from_dict(cls, user_data):
        return cls(
            user_data['naam'],
            user_data['password'],
            user_data['parkeerplaats'],
            user_data['evenementen'],
            user_data['bevoegdheid'],
            user_data['unieke_ID']
        )


