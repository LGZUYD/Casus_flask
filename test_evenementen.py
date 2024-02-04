import unittest
from unittest.mock import patch, Mock
from evenementen import *

class TestEvenement(unittest.TestCase):

    def setUp(self):
        # aanmaken van een dummy evenement
        # de aanmeldingen worden opgezet om te testen of de bezoeker correct wordt toegevoegd en verwijderd
        # de bezoekers limiet wordt op 100 gezet om te testen of de limiet wordt gecontroleerd
        self.dummy_event = Evenement("TestEvenement", "TestLocatie", "2023-12-31T22:00", "2023-12-31T23:00", "TestPresentator", 100, "E-0")
        self.dummy_event.aanmeldingen = {"A-0": "ADMIN", "G-0": "BEZOEKER"}
        self.dummy_event.beschrijving = "TestBeschrijving"

        self.dummy_gebruiker = Mock(unieke_ID="G-0")
    
    def test_check_bezoekers_limiet(self):
        # test of de bezoekers limiet wordt gecontroleerd
        self.assertEqual(self.dummy_event.check_bezoekers_limiet(), True)

    def test_evenement_informatie_to_dict(self):
        # test of de informatie van het evenement wordt omgezet naar een dictionary
        verwachte_data = {
            "evenementnaam": "TestEvenement",
            "locatie": "TestLocatie",
            "startTijd": "2023-12-31T22:00",
            "eindTijd": "2023-12-31T23:00",
            "presentator": "TestPresentator",
            "bezoekers_limiet": 100,
            "event_ID": "E-0",
            "aanmeldingen": {"A-0": "ADMIN", "G-0": "BEZOEKER"},
            "beschrijving": "TestBeschrijving"
        }
        self.assertEqual(self.dummy_event.__evenement_informatie_to_dict__(), verwachte_data)

    def test_bezoekers_aanmelding(self):
        # test of de bezoeker wordt toegevoegd aan de aanmeldingen
        self.assertEqual(self.dummy_event.bezoekers_aanmelding(self.dummy_gebruiker), True)

    def test_bezoekers_aanmelding_limiet_bereikt(self):
        # test of de bezoeker niet wordt toegevoegd aan de aanmeldingen
        self.dummy_event.bezoekers_limiet = 1
        self.assertEqual(self.dummy_event.bezoekers_aanmelding(self.dummy_gebruiker), False)

    def test_bezoeker_verwijderen(self):
        # test verwijderen van een bezoeker uit de aanmeldingen
        self.dummy_event.bezoeker_verwijderen(self.dummy_gebruiker)
        self.assertNotIn("G-0", self.dummy_event.aanmeldingen)