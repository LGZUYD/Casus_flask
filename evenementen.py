import json
import gebruikers
    
class Evenementen:

    def __init__(self, naam, locatie, tijd, duur, presentator, bezoekers_limiet):
        
        self.naam = naam
        self.locatie = locatie
        self.tijd = tijd
        self.duur = duur
        self.presentator = presentator
        self.bezoekers_limiet = bezoekers_limiet
        self.aanmeldingen = {}

        self.informatie = self.__evenement_informatie__() # ?

    def __evenement_informatie__(self):
        # verzamel de informatie over het evenement om deze uit te lezen of naar json te verwerken
        informatie = {
            'evenementnaam': self.naam,
            'locatie': self.locatie,
            'tijd': self.tijd,
            'duur': self.duur,
            'presentator': self.presentator,
            'bezoekers limiet': self.bezoekers_limiet,
            'aanmeldingen': self.aanmeldingen
        }
        
        return informatie
    
    @classmethod
    def info_from_dict(cls, evenement_data):
        return cls(
            evenement_data['naam'],
            evenement_data['locatie'],
            evenement_data['tijd'],
            evenement_data['duur'],
            evenement_data['presentator'],
            evenement_data['bezoekers limiet'],
            evenement_data['aanmeldingen']
        )

    def check_bezoekers_limiet(self):
        # controleer of er nog plaats is voor bezoekers om deel te nemen
        if len(self.aanmeldingen) < self.bezoekers_limiet:
            return True 
        
    def bezoekers_aanmelding(self, bezoeker):

        if self.check_bezoekers_limiet():
        
            self.aanmeldingen[bezoeker.unieke_ID] = bezoeker.naam
    
            # print("Beste {}, u bent aangemeldt voor '{}'.".format(bezoeker.naam, self.naam))
            # stuur bevestiging etc
        else:
            pass
            # stuur bericht wanneer het limiet is bereikt
            # print("{}, Het bezoekers aantal limiet voor dit evenement is bereikt.".format(bezoeker.naam))

    def bezoeker_verwijderen(self, bezoeker):
        # bezoeker uit self.aanmeldingen verwijderen
        # in json van evenementen en bezoekers verwijderen
        pass
   
        