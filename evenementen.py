import json
import gebruikers
    
class Evenement:
    # class voor het aanmaken van een evenement
    # alle informatie over het evenement wordt opgeslagen in de instance van de class
    # deze worden eerst op None gezet, zodat ze niet verplicht zijn om in te voeren.
    def __init__(self, naam=None, locatie=None, startTijd=None, eindTijd=None, presentator=None, bezoekers_limiet=None, event_ID=None, aanmeldingen=None, beschrijving=None):
        
        self.naam = naam
        self.locatie = locatie
        self.startTijd = startTijd
        self.eindTijd = eindTijd
        self.presentator = presentator
        self.bezoekers_limiet = int(bezoekers_limiet)
        self.event_ID =  event_ID or self.event_id_generator() 
        self.aanmeldingen = aanmeldingen or {}
        self.beschrijving = beschrijving


    def event_id_generator(self):
        # genereer een unieke event ID
        event_ID_string = ''

        with open("json/identificators.json", "r") as json_file:
            data = json.load(json_file)
            event_ID_string += "E-" + str(data["evenementen"])
            # evenement ID begint altijd met "E-"
        
        with open("json/identificators.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        return event_ID_string


    def __evenement_informatie_to_dict__(self):
        # verzamel de informatie over het evenement om deze uit te lezen of naar json te verwerken
        informatie = {
            'evenementnaam': self.naam,
            'locatie': self.locatie,
            'startTijd': self.startTijd,
            'eindTijd': self.eindTijd,
            'presentator': self.presentator,
            'bezoekers_limiet': self.bezoekers_limiet,
            "event_ID":self.event_ID,
            'aanmeldingen': self.aanmeldingen,
            'beschrijving':self.beschrijving
        }
        
        return informatie
     
    # met een @classmethod kan je een instance maken van een class met een dictionary als argument,
    # dit is handig om data uit een json file te halen en om te zetten naar een instance van een class
    @classmethod
    def info_from_dict(cls, evenement_data):
        return cls(
            evenement_data['evenementnaam'],
            evenement_data['locatie'],
            evenement_data['startTijd'],
            evenement_data['eindTijd'],
            evenement_data['presentator'],
            evenement_data['bezoekers_limiet'],
            evenement_data['event_ID'],
            evenement_data['aanmeldingen'],
            evenement_data['beschrijving']
        )

    def check_bezoekers_limiet(self):
        # controleer of er nog plaats is voor bezoekers om deel te nemen
        if len(self.aanmeldingen) < self.bezoekers_limiet:
            return True 
        
    def bezoekers_aanmelding(self, bezoeker):
        # roept eerst de methode aan om te controleren of de limiet is bereikt
        if self.check_bezoekers_limiet():
            # zo niet, wordt de bezoeker toegevoegd aan de aanmeldingen
            self.aanmeldingen[bezoeker.unieke_ID] = bezoeker.naam
            return True    
        else:
            # anders wordt de bezoeker niet toegevoegd
            return False

    def bezoeker_verwijderen(self, bezoeker):
    # dit controleert of een bezoeker is aangemeld en verwijdert daarna de bezoeker uit de aanmeldingen
        if bezoeker.unieke_ID in self.aanmeldingen:
            del self.aanmeldingen[bezoeker.unieke_ID]

        
   
        