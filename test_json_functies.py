import unittest
import json
from json_functies import *
from gebruikers import Gebruiker

    # test of de parkeerplaatsen.json file wordt gelezen en de data wordt teruggegeven
def test_gebruiker_informatie_zoeken():
    zoekterm = "A-0"
    verwachte_data = {"A-0": {"naam": "ADMIN", "password": "test", "parkeerplaats": "A1", "evenementen": ["E-0", "E-1"], "bevoegdheid": "beheerder", "unieke_ID": "A-0"}}
    assert gebruiker_informatie_zoeken(zoekterm) == verwachte_data

# test of de account informatie wordt gevonden in de json file
def test_account_informatie_vinden_in_json():
    unieke_code = "A-0"
    verwachte_data = {"naam": "ADMIN", "password": "test", "parkeerplaats": "A1", "evenementen": ["E-0", "E-1"], "bevoegdheid": "beheerder", "unieke_ID": "A-0"}
    assert account_informatie_vinden_in_json(unieke_code) == verwachte_data

# test of de account informatie wordt gewijzigd in de json file
def test_account_informatie_wijzigen_in_json():
    unieke_code = "T-0"
    te_wijzigen_data = {"naam": "TEST"}
    verandering = {"naam": "verandering"}
    assert account_informatie_wijzigen_in_json(unieke_code, te_wijzigen_data, verandering) == "Geen beschikbare data meegegeven als tweede argument voor 'account_informatie_wijzigen_in_json"

# controleer of de ingevoerder wachtwoord overeenkomt met de wachtwoord in de json file
def test_account_password_controle():
    unieke_code = "A-0"
    password = "test"
    assert account_password_controle(unieke_code, password) == True

# test of de gebruiker instance correct wordt aangemaakt met de json data
def test_gebruiker_instance_aanmaken_met_json_data():
    unieke_code = "A-0"
    test_gebruikers_instance = gebruiker_instance_aanmaken_met_json_data(unieke_code)
    assert test_gebruikers_instance.naam == "ADMIN"

# test of de huidge presentator verificatie code wordt gevonden in de json file
def test_huidige_presentator_verificatie_code():

    with open("json/identificators.json", "r") as json_file:
        data = json.load(json_file)

    assert huidige_presentator_verificatie_code() == data["presentator_verificatie_code"]

# test of de ingevoerde presentator code wordt gecontroleerd
def test_ingevoerde_presentator_code_verifieren():
    unieke_code = "fadsfsadfsadf"
    assert ingevoerde_presentator_code_verifieren(unieke_code) == False

# test of de identificator informatie wordt opgehaald uit de json file
def test_identificator_informatie_ophalen():
    
    with open("json/identificators.json", "r") as json_file:
        data = json.load(json_file)

    assert(identificator_informatie_ophalen() == data)

# test of de tijd code correct wordt omgezet naar een dictionary en de juiste informatie wordt teruggegeven
def test_tijd_code_converten():
    tijd = "2023-12-31T23:59"
    assert tijd_code_converten(tijd)["jaar"] == 2023
    assert tijd_code_converten(tijd)["maand"] == 12
    assert tijd_code_converten(tijd)["dag"] == 31
    assert tijd_code_converten(tijd)["uur"] == 23
    assert tijd_code_converten(tijd)["minuten"] == 59


# test of de evenement informatie wordt gevonden in de json file
def test_evenement_informatie_vinden_in_json():
    event_ID = "E-0"
    verwachte_data = {
        "evenementnaam": "TestEvenement1",
        "locatie": "TestLocatie1",
        "startTijd": "2024-01-01T12:00",
        "eindTijd": "2024-01-01T13:00",
        "presentator": {
            "P-0": "PRESENTATOR"
        },
        "bezoekers_limiet": 10,
        "event_ID": "E-0",
        "aanmeldingen": {
            "A-0": "ADMIN",
            "G-0": "BEZOEKER"
        },
        "beschrijving": "TestBeschrijving1"
    }
            
    assert evenement_informatie_vinden_in_json(event_ID) == verwachte_data        


def test_evenement_instance_aanmaken_met_json_data():
    # test of de evenement instance correct wordt aangemaakt met de json data
    event_ID = "E-0"
    test_evenement_instance = evenement_instance_aanmaken_met_json_data(event_ID)
    # door .naam te testen, controleert deze test of de instance correct is aangemaakt
    assert test_evenement_instance.naam == "TestEvenement1"

def test_evenement_informatie_zoeken_in_json():
# test of de evenement informatie wordt gevonden met ingevoerde zoekterm in de json file
    zoekterm = "TestEvenement1"

    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)
    
    verwachte_data = [data["E-0"]]

    assert evenement_informatie_zoeken_in_json(zoekterm) == verwachte_data


def test_evenementen_ingeschreven_zoeken_in_json():
    unieke_code = "A-0"
    # test of de evenementen waar de gebruiker is ingeschreven worden gevonden met het doorgeven van zijn unieke code    
    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)

    verwachte_data = [data["E-0"], data["E-1"]]

    assert evenementen_ingeschreven_zoeken_in_json(unieke_code) == verwachte_data


def test_presentator_lijst_uit_json_maken():
    # test of de presentator lijst correct wordt gemaakt van de json file
    with open("json/bezoekers.json", "r") as json_file:
        data = json.load(json_file)

    verwachte_data = [{"P-0":"PRESENTATOR"}]

    assert presentator_lijst_uit_json_maken() == verwachte_data
