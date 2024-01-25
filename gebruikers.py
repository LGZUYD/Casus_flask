import json
import unieke_identificator_generator
import parkeerplaats_functies

class Gebruiker:

    def __init__(self, naam, parkeerplaats=None, evenementen=None, bevoegdheid="bezoeker", unieke_code=None):
        
        self.naam = naam
        # self.password = password
        self.parkeerplaats = parkeerplaats
        self.geregistreerde_evenementen = evenementen or []
        self.bevoegdheid = bevoegdheid
        
        self.unieke_ID = unieke_code or unieke_identificator_generator.unieke_registratie_code_generator(self.bevoegdheid)
        # dit zorgt ervoor dat bij het aanmaken van de instance een unieke code wordt gegenereerd,
        # omdat er geen argument wordt meegegeven de eerste keer,
        # als de instance daarna opnieuw wordt aan watever

         
    def __parkeerplaats_reserveren__(self):
        if self.parkeerplaats == None:
            self.parkeerplaats = parkeerplaats_functies.parkeerplaats_reserveren(self.unieke_ID)
        return
            
    
    def __parkeerplaats_naam__(self):
        if self.parkeerplaats:
            print(f"Uw parkeerplaats is {self.parkeerplaats}. ")
        else:
            print("U heeft geen parkeerplaats gereserveerd.")
        # dit interacteert nog niet met frontend,
        # geen idee of dit uberhaupt erin blijft


    def __registreer_evenement__(self, evenement):
        if evenement.event_ID not in self.geregistreerde_evenementen:
            self.geregistreerde_evenementen.append(evenement.event_ID)

    def uitschrijven_evenement(self, evenement):
        if evenement.event_ID in self.geregistreerde_evenementen:
            self.geregistreerde_evenementen.remove(evenement.event_ID)
        
            
    def info_to_dict(self):
        return {
            'naam':self.naam,
            'parkeerplaats': self.parkeerplaats,
            'evenementen': self.geregistreerde_evenementen,
            'bevoegdheid': self.bevoegdheid,
            'unieke_ID': self.unieke_ID
            }
        
    
    @classmethod
    def info_from_dict(cls, user_data):
        return cls(
            user_data['naam'],
            user_data['parkeerplaats'],
            user_data['evenementen'],
            user_data['bevoegdheid'],
            user_data['unieke_ID']
        )

# deze is misschien niet nodig
# dit kan allemaal weg
class Bezoeker(Gebruiker):

    def __init__(self, naam, parkeerplaats =""):
        super().__init__(naam, parkeerplaats)



class Presentator(Gebruiker):

    def __init__(self, naam, parkeerplaats =""):
        super().__init__(naam, parkeerplaats)



class Beheerder(Gebruiker):

    def __init__(self, naam, parkeerplaats=None, evenementen=None, bevoegdheid="beheerder", unieke_code=None):
        super().__init__(naam, parkeerplaats, evenementen)
        self.bevoegdheid = bevoegdheid
        self.unieke_ID = unieke_code or unieke_identificator_generator.unieke_registratie_code_generator(self.bevoegdheid)






