import unittest
from unittest.mock import patch, Mock
from gebruikers import *

class TestGebruiker(unittest.TestCase):

    def setUp(self):
        self.dummy_user = Gebruiker("TestGebruiker", "wachtwoord123")

    @patch("parkeerplaats_functies.parkeerplaats_reserveren")
    def test_parkeerplaats_reserveren(self, mock_reserveren):
        # Mocken van het reserveren van parkeerplaatsen om een vaste waarde terug te geven
        mock_reserveren.return_value = "Parkeerplaats 1"
        
        # Aanmaken van een dummy gebruiker
   
        # Set parkeerplaats op None om te simuleren dat de gebruiker nog geen parkeerplaats heeft
        self.dummy_user.parkeerplaats = None
        
        # Uitvoeren van de te testen functie
        self.dummy_user.__parkeerplaats_reserveren__()
        
        # Verifiëren of de parkeerplaats van de gebruiker correct is bijgewerkt
        self.assertEqual(self.dummy_user.parkeerplaats, "Parkeerplaats 1")

    def test_registreer_evenement(self):
            # test of de gebruiker wordt toegevoegd aan de geregistreerde evenementen
            evenement = Mock(event_ID=1)
            self.dummy_user.__registreer_evenement__(evenement)
            self.assertIn(1, self.dummy_user.geregistreerde_evenementen)

    def test_uitschrijven_evenement(self):
            # test of de gebruiker wordt verwijderd uit de geregistreerde evenementen
            evenement = Mock(event_ID=1)
            self.dummy_user.geregistreerde_evenementen = [1, 2, 3]
            self.dummy_user.uitschrijven_evenement(evenement)
            self.assertNotIn(1, self.dummy_user.geregistreerde_evenementen)

class TestBezoeker(unittest.TestCase):

    def test_init(self):
        bezoeker = Gebruiker("TestBezoeker", "wachtwoord123")
        self.assertEqual(bezoeker.bevoegdheid, "bezoeker")

class TestPresentator(unittest.TestCase):

    def test_init(self):
        presentator = Gebruiker("TestPresentator", "wachtwoord123")
        self.assertEqual(presentator.bevoegdheid, "bezoeker")

class TestBeheerder(unittest.TestCase):

    def test_init(self):
        beheerder = Gebruiker("TestBeheerder", "wachtwoord123")
        beheerder.bevoegdheid = "beheerder"
        self.assertEqual(beheerder.bevoegdheid, "beheerder")

if __name__ == '__main__':
    unittest.main()
