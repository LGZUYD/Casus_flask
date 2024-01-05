import json
import unieke_identificator_generator
import parkeerplaatsen

class Gebruiker:

    def __init__(self, naam, parkeerplaats=None, evenementen=None, bevoegdheid="", unieke_code=None):
        
        self.naam = naam
        self.parkeerplaats = parkeerplaats
        self.geregistreerde_evenementen = evenementen or []
        self.bevoegdheid = bevoegdheid
        
        self.unieke_ID = unieke_code or unieke_identificator_generator.unieke_registratie_code_generator(self.bevoegdheid)
        # dit zorgt ervoor dat bij het aanmaken van de instance een unieke code wordt gegenereerd,
        # omdat er geen argument wordt meegegeven de eerste keer,
        # als de instance daarna opnieuw wordt aan watever

         
    def __parkeerplaats_reserveren__(self):
        if self.parkeerplaats == None:
            self.parkeerplaats = parkeerplaatsen.parkeerplaats_reserveren(self.unieke_ID)
        return
            
    
    def __parkeerplaats_naam__(self):
        if self.parkeerplaats:
            print(f"Uw parkeerplaats is {self.parkeerplaats}. ")
        else:
            print("U heeft geen parkeerplaats gereserveerd.")
        # dit interacteert nog niet met frontend


    def __registreer_evenement__(self, evenement):
        
        # controleert of er nog plek is in het evenement om deel te nemen
        if evenement.check_bezoekers_limiet():
            self.geregistreerde_evenementen.append(evenement.informatie)
            evenement.bezoekers_aanmelding(self)
            # werkt self hier?
            # waarschijnlijk betere manier te vinden
        else:
            pass
            # kijken wat makkelijker is, waarschijnlijk print()-placeholder-
            # statements van bezoekers_aanmelding() hier doen
            
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


class Bezoeker(Gebruiker):

    def __init__(self, naam, parkeerplaats =""):
        super().__init__(naam, parkeerplaats)


class Presentator(Gebruiker):

    def __init__(self, naam, parkeerplaats =""):
        super().__init__(naam, parkeerplaats)


class Beheerder(Gebruiker):

    def __init__(self, naam, parkeerplaats =""):
        super().__init__(naam, parkeerplaats)


