import json
import gebruikers
    
class Evenement:

    def __init__(self, naam=None, locatie=None, tijd=None, duur=None, presentator=None, bezoekers_limiet=None, event_ID=None, aanmeldingen=None):
        
        self.naam = naam
        self.locatie = locatie
        self.tijd = tijd
        self.duur = duur
        self.presentator = presentator
        self.bezoekers_limiet = int(bezoekers_limiet)
        self.event_ID =  event_ID or self.event_id_generator() 
        self.aanmeldingen = aanmeldingen or {}

        #self.informatie = self.__evenement_informatie_to_dict__() # ?

    def event_id_generator(self):

        event_ID_string = ''

        with open("json/identificators.json", "r") as json_file:
            data = json.load(json_file)
            event_ID_string += "E-" + str(data["evenementen"])
        
        with open("json/identificators.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        return event_ID_string


    def __evenement_informatie_to_dict__(self):
        # verzamel de informatie over het evenement om deze uit te lezen of naar json te verwerken
        informatie = {
            'evenementnaam': self.naam,
            'locatie': self.locatie,
            'tijd': self.tijd,
            'duur': self.duur,
            'presentator': self.presentator,
            'bezoekers_limiet': self.bezoekers_limiet,
            "event_ID":self.event_ID,
            'aanmeldingen': self.aanmeldingen
        }
        
        return informatie
    
    @classmethod
    def info_from_dict(cls, evenement_data):
        return cls(
            evenement_data['evenementnaam'],
            evenement_data['locatie'],
            evenement_data['tijd'],
            evenement_data['duur'],
            evenement_data['presentator'],
            evenement_data['bezoekers_limiet'],
            evenement_data['event_ID'],
            evenement_data['aanmeldingen']
        )

    def check_bezoekers_limiet(self):
        # controleer of er nog plaats is voor bezoekers om deel te nemen
        if len(self.aanmeldingen) < self.bezoekers_limiet:
            return True 
        
    def bezoekers_aanmelding(self, bezoeker):
        
        if self.check_bezoekers_limiet():
            self.aanmeldingen[bezoeker.unieke_ID] = bezoeker.naam
            return True    
        else:
            return False

    def bezoeker_verwijderen(self, bezoeker):
        if bezoeker.unieke_ID in self.aanmeldingen:
            del self.aanmeldingen[bezoeker.unieke_ID]

        
   
        