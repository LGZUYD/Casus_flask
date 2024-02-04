from flask import Flask, render_template, request, redirect, url_for, session
from gebruikers import *
from json_functies import *
import unieke_identificator_generator
import parkeerplaats_functies
# alle functies en nodige functionaliteiten van Flask worden geimporteerd

# de Flask applicatie wordt geinitialiseerd
app = Flask(__name__)
# de secret_key wordt geinitialiseerd, deze wordt gebruikt om de sessie te beveiligen
app.secret_key = "abcdefg1234567"

# de route voor de homepagina wordt aangemaakt
@app.route("/")
def hello_world():
    # de homepagina wordt gerenderd
    # de homepagina is de eerste pagina die de gebruiker ziet, daarom wordt dit in app.rout met ("/") aangegeven
    return render_template("index.html")

# de route voor het aanmaken van een account wordt aangemaakt
@app.route('/account_aanmaken', methods=['GET', 'POST'])
def aanmeld_submit():
    
    # deze functie wordt aangeroepen als de gebruiker een account aanmaakt
    if request.method == 'POST':
        # de gebruiker wordt eerst geinitialiseerd als bezoeker
        bevoegdheid = "bezoeker"
        # als de verificatie code is ingevuld, wordt deze gecontroleerd
        if request.form["verificatie"] != "":
            # als de verificatie code klopt, wordt de gebruiker geinitialiseerd als presentator
            if ingevoerde_presentator_code_verifieren(request.form["verificatie"]):
                bevoegdheid = "presentator"
            else:
                # als de verificatie code niet klopt, krijgt de gebruiker een error melding
                return render_template("account_aanmaken.html", error=True)
            
        # een nieuwe gebruiker wordt geinitialiseerd met de ingevoerde gegevens
        nieuwe_gebruiker = Gebruiker(request.form['name'], request.form['password'], bevoegdheid=bevoegdheid)
        # daarna wordt de nieuwe gebruiker in de json file opgeslagen
        account_aanmaken_in_json(nieuwe_gebruiker)
        # de gebruiker wordt doorgestuurd naar de bevestigingspagina
        return redirect(url_for("unieke_ID_bevestigen", unieke_ID=nieuwe_gebruiker.unieke_ID))
    
    # als de gebruiker nog geen account heeft aangemaakt, wordt de pagina gerenderd
    return render_template("account_aanmaken.html")

# de route voor het bevestigen van de unieke ID wordt aangemaakt
@app.route('/account_aanmaken/ID_bevestigen')
def unieke_ID_bevestigen():
    
    # als account aangemaakt wordt, wordt huidige gebruiker uitgelogd,
    # dit is om te voorkomen dat de gebruiker meteen inlogt met de nieuwe unieke_ID zonder bevestiging
    session.pop("unieke_ID", None)
    unieke_ID = request.args.get("unieke_ID")    
    # de unieke ID wordt op de bevestigingspagina weergegeven
    return render_template("account_aanmaken_ID_bevestigen.html", unieke_ID=unieke_ID)
  
# de route voor het inloggen wordt aangemaakt
@app.route('/inloggen', methods=['GET', 'POST'])
def inlog_submit():

    # als de gebruiker een account heeft aangemaakt, wordt deze functie aangeroepen
    if request.method == 'POST':
        # de unieke code wordt opgevraagd op basis van de ingevoerde gegevens
        inlog_code = request.form["unieke_code"]
        # de ingevoerde gegevens worden gecontroleerd
        try:
            # de account data wordt opgevraagd op basis van de ingevoerde unieke code
            account_data = account_informatie_vinden_in_json(inlog_code)
        except:
            # als de ingevoerde gegevens niet kloppen, krijgt de gebruiker een error melding
            return render_template("inloggen.html", error=True)
        
        if account_data["password"] != request.form["password"]:
            # als de ingevoerde gegevens niet kloppen, krijgt de gebruiker een error melding
            return render_template("inloggen.html", error=True)
        
        session["unieke_ID"] = inlog_code
        # De huidige gebruiker wordt opgeslagen in de session functionaliteit van Flask
        # Dit is om de gebruiker te onthouden en te kunnen gebruiken in de applicatie
        # De gebruiker wordt daarna doorgestuurd naar de homepagina    
        return redirect(url_for("gebruiker_home", unieke_ID=inlog_code))
    
    else:
        # het systeem controleert of de gebruiker al is ingelogd, door te controleren of de unieke_ID in de session is opgeslagen
        if "unieke_ID" in session:
            inlog_code = session["unieke_ID"]
            return redirect(url_for("gebruiker_home", unieke_ID=inlog_code))
            # als de gebruiker al is ingelogd, wordt de gebruiker doorgestuurd naar de homepagina
        
    # als de gebruiker nog niet is ingelogd, wordt de inlogpagina gerenderd
        return render_template("inloggen.html")
    
# de route voor het uitloggen wordt aangemaakt
@app.route("/logout")
def log_uit():
    session.pop("unieke_ID", None)
    return redirect(url_for("hello_world"))
    # de gebruiker wordt uitgelogd in de session door de unieke_ID te verwijderen en doorgestuurd naar de startpagina

#  de route voor het weergeven van de pagina voor toegang geweigerd wordt aangemaakt
@app.route("/toegang_geweigerd")
def toegang_geweigerd_functie():
    # het systeem controleert of de gebruiker al is ingelogd, door te controleren of de unieke_ID in de session is opgeslagen
    # als dit zo is, wordt de gebruiker doorgestuurd naar een pagina waarop staat dat de gebruiker geen toegang heeft, die de basis template van de homepagina gebruikt
    if session["unieke_ID"]:
        return render_template("toegang_geweigerd.html", base=True)
    # als de gebruiker niet  wordt de gebruiker doorgestuurd naar de start pagina, en wordt de basis template van de startpagina gebruikt
    else:
        return render_template("toegang_geweigerd.html", base=False)


# de route voor het weergeven van de homepagina wordt aangemaakt
@app.route("/home")
def gebruiker_home():
    # het systeem controleert of de gebruiker al is ingelogd, door te controleren of de unieke_ID in de session is opgeslagen
    # zo niet, wordt de gebruiker doorverwezen naar de pagina voor toegang geweigerd
    if "unieke_ID" not in session and session["unieke_ID"] != request.args.get("unieke_ID"):
            return render_template("toegang_geweigerd.html")
    
    else:
        # als de gebruiker wel is ingelogd, wordt de gebruiker doorgestuurd naar de homepagina    
        # het systeem controleert of de gebruiker al is ingelogd, door te controleren of de unieke_ID in de session is opgeslagen
        # anders wordt de gebruiker unieke_ID opgevraagd uit de html request
        huidige_gebruiker_ID = session["unieke_ID"] or request.args.get("unieke_ID")
        # de account data wordt opgevraagd op basis van de ingevoerde unieke code
        account_instance = gebruiker_instance_aanmaken_met_json_data(huidige_gebruiker_ID)
        # de homepagina wordt gerenderd, en de account data wordt meegegeven zodat deze gerendered kan worden in de html
        return render_template("home.html", account_instance=account_instance)

# de route voor het aanmaken van een evenement wordt aangemaakt
@app.route('/evenement_aanmaken', methods=['GET', 'POST'])
def evenement_aanmaken():

    if "A" not in session["unieke_ID"] and "P" not in session["unieke_ID"]:
        # als de gebruiker niet de juiste bevoegdheid heeft, wordt de gebruiker doorgestuurd naar de pagina voor toegang geweigerd
        return render_template("toegang_geweigerd.html")
    
    huidige_presentator = False
    # de huidige presentator wordt eerst als False geinitialiseerd
    if "P" in session["unieke_ID"]:
        # als de huidige gebruiker een presentator is, wordt de huidige presentator geinitialiseerd als True
        presentator_gebruiker_info = account_informatie_vinden_in_json(session["unieke_ID"])
        huidige_presentator = True

    # de presentator lijst wordt opgevraagd uit de json file
    presentator_lijst = presentator_lijst_uit_json_maken()

    if request.method == 'POST':
        # als de gebruiker een evenement aanmaakt, wordt deze functie aangeroepen
        # alle ingevoerde informatie wordt opgeslagen
        startTijd = request.form['startTijd']
        eindTijd = request.form['eindTijd']
        locatie = request.form['locatie']

        # er wordt door het systeem gecontroleerd of er overlapping plaatstvindt
        overlapping = evenementen_overlapping_controle(startTijd, eindTijd, locatie)

        if overlapping != False:
            # als er overlapping plaatsvindt, krijgt de gebruiker een error melding
            error_message = f'Overlapping gevonden met evenement {overlapping[0]} op locatie {overlapping[1]}. <br>Starttijd: {overlapping[2]["uur"]:02d}:{overlapping[2]["minuten"]:02d} <br>Eindtijd: {overlapping[3]["uur"]:02d}:{overlapping[3]["minuten"]:02d}'          
            return render_template("evenement_aanmaken.html", error_message=error_message, huidige_presentator=huidige_presentator) 

        # De 'presentator' invul optie op de pagina wordt alleen maar weergegeven bij beheerders die een evenement aanmaken,
        # Als een presentator een evenement aanmaakt, wordt dit veld automatisch als presentator ingevuld.
        try:
            presentator_naam = account_informatie_vinden_in_json(request.form["presentator"])["naam"]
            presentator = {request.form["presentator"] : presentator_naam}
        except:
            presentator = {session["unieke_ID"] : presentator_gebruiker_info["naam"]} 
        
        # een nieuw evenement Class wordt aangemaakt met de ingevoerde gegevens
        nieuw_evenement = Evenement(
        naam=request.form['evenementnaam'],
        locatie=request.form['locatie'],
        startTijd=startTijd,
        eindTijd=eindTijd,
        presentator=presentator,
        bezoekers_limiet=request.form['bezoekers_limiet'],
        beschrijving=request.form['beschrijving'])
        # het nieuwe evenement wordt opgeslagen in de json file
        evenement_aanmaken_in_json(nieuw_evenement)
        # de gebruiker wordt doorgestuurd naar de evenementen pagina
        return redirect(url_for("evenementen_bekijken"))
    # als de gebruiker nog geen evenement heeft aangemaakt, wordt de evenement aanmaak pagina gerenderd met de relevante presentator informatie 
    return render_template("evenement_aanmaken.html", huidige_presentator=huidige_presentator, presentator_lijst=presentator_lijst) 


# de route voor het weergeven van de evenementen pagina wordt aangemaakt
@app.route('/evenementen', methods=['GET', 'POST'])
def evenementen_bekijken():
    # evenementen data worden opgevraagd uit de json file
    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)
    # de huidige gebruiker data wordt opgevraagd uit de session
    session_gebruiker = session["unieke_ID"]
    session_acc_bevoegdheid = account_informatie_vinden_in_json(session_gebruiker)["bevoegdheid"]
    # een lege list wordt aangemaakt om de evenementen data in op te slaan
    eventlist = []
    
    for event in data:
        # de evenementen data uit json wordt in de list opgeslagen
        eventlist.append(data[event])
        
    if request.method == 'POST':
        # als de gebruiker informatie invoert, wordt deze functie aangeroepen
        if "Inschrijven" in request.form:
            # als de gebruiker zich inschrijft voor een evenement, wordt opgehaald welk evenement dit is
            event_ID_voor_inschrijven = eventlist[int(request.form["index"])]["event_ID"]
            # de bezoekeer wordt ingeschreven voor het evenement
            # dit wordt opgeslagen in zowel de evenementen data als de gebruiker data
            bezoeker_inschrijven_evenement_in_json(event_ID_voor_inschrijven, session_gebruiker)
            return redirect(url_for("evenementen_bekijken"))             
            
            
        elif "Uitschrijven" in request.form:
            # als de gebruiker zich uitschrijft voor een evenement, wordt opgehaald welk evenement dit is
            event_ID_voor_uitschrijven = eventlist[int(request.form["index"])]["event_ID"]
            # de bezoekeer wordt uitgeschreven voor het evenement, dit gebeurt zowel in de evenementen data als de gebruiker data
            bezoeker_uitschrijven_evenement_in_json(event_ID_voor_uitschrijven, session_gebruiker)
            
            return redirect(url_for("evenementen_bekijken"))
        
        elif "Verwijderen" in request.form:
            # als de beheerder een evenement verwijdert, wordt opgehaald welk evenement dit is uit de ingevoerde informatie
            event_ID_voor_uitschrijven = eventlist[int(request.form["event_ID"])]["event_ID"]
            gebruiker_id_voor_uitschrijven = request.form["unieke_ID"]

            bezoeker_uitschrijven_evenement_in_json(event_ID_voor_uitschrijven, gebruiker_id_voor_uitschrijven) 
            # het evenement wordt verwijderd uit de evenementen data
            return redirect(url_for("evenementen_bekijken"))

        elif "Wijzigen" in request.form:
            # als de beheerder een evenement wijzigt, wordt opgehaald welk evenement dit is uit de ingevoerde informatie
            event_ID_voor_wijzigen = eventlist[int(request.form["index"])]["event_ID"]
            # de gebruiker wordt doorgestuurd naar de evenement wijzigen pagina
            return redirect(url_for("evenement_wijzigen", event_ID_voor_wijzigen=event_ID_voor_wijzigen))
        
        elif "evenement_zoeken" in request.form:
            # als de gebruiker een zoekterm invoert, wordt deze functie aangeroepen
            zoekterm = request.form["evenement_zoeken"]
            # de ingevoerde zoekterm wordt opgezocht in de evenementen data
            gevonden_evenementen = evenement_informatie_zoeken_in_json(zoekterm)

            # de gevonden evenementen worden gerenderd op de evenementen pagina, met informatie over de evenementen en de bevoegdheid van de huidige gebruiker
            return render_template("evenementen.html", len=len(gevonden_evenementen), eventlist=gevonden_evenementen, bevoegdheid=session_acc_bevoegdheid, session_gebruiker=session_gebruiker)
        
        elif "Aangemelde_Evenement_tonen" in request.form:
            # als de gebruiker op de knop drukt om de evenementen te tonen waarvoor hij is ingeschreven,
            # zoekt deze functie naar alle evenementen waarvoor de gebruiker is ingeschreven
            ingeschreven_evenementen = evenementen_ingeschreven_zoeken_in_json(session_gebruiker)

            return render_template("evenementen.html", len=len(ingeschreven_evenementen), eventlist=ingeschreven_evenementen, bevoegdheid=session_acc_bevoegdheid, session_gebruiker=session_gebruiker)
    # als de gebruiker nog geen evenement heeft aangemaakt, wordt de evenementen pagina gerenderd met de evenementen data en de bevoegdheid van de huidige gebruiker            
    return render_template("evenementen.html", len=len(eventlist), eventlist=eventlist, bevoegdheid=session_acc_bevoegdheid, session_gebruiker=session_gebruiker)

@app.route("/evenement_wijzigen", methods=['GET', 'POST'])
def evenement_wijzigen():
    # het systeem controleert of de gebruiker al is ingelogd, door te controleren of de unieke_ID in de session is opgeslagen
    if "A" not in session["unieke_ID"] and "P" not in session["unieke_ID"]:
        return render_template("toegang_geweigerd.html")
    
    event_ID_voor_wijzigen = request.args.get("event_ID_voor_wijzigen")
    # Het evenement om te wijzigen wordt opgevraagd uit de html pagina
    event_info = evenement_informatie_vinden_in_json(event_ID_voor_wijzigen)
    # de presentator lijst wordt opgevraagd uit de json file
    presentator_lijst = presentator_lijst_uit_json_maken()
    
    if request.method == 'POST':
        # als de gebruiker informatie invoert, wordt deze functie aangeroepen
        if "Wijzigen" in request.form:
            # als eerst wordt een lege dictionary aangemaakt om de ingevoerde informatie in op te slaan
            data_om_te_veranderen = {}
            # deze aanpak zorgt ervoor dat alle mogelijke ingevoerde informatie wordt opgevangen,
            # zodat er niet voor iedere mogelijke input een aparte if statement hoeft te worden geschreven
            # voor de invoeringen die apparte behandeling nodig hebben, worden dan wel aparte if statement geschreven
            for data in request.form:
                if request.form[data] != '' and data != "Wijzigen":

                    if data == "presentator":     
                        presentator_naam = account_informatie_vinden_in_json(request.form[data])["naam"]
                        data_om_te_veranderen[data] = {request.form[data] : presentator_naam}
                    else:
                        data_om_te_veranderen[data] = request.form[data]
            # als er geen data is ingevoerd, wordt de gebruiker teruggestuurd naar de evenementen pagina
            if len(data_om_te_veranderen) == 0:
                return redirect(url_for("evenementen_bekijken"))
            
            # dit controleert op alle mogelijke combinaties van informatie die betrekking hebben op overlappingsmogelijkheid      
            # om op overlapping te controleren als er maar een van de drie mogelijke veranderingen wordt doorgevoerd,
            # wordt er uit de json de aanvullende informatie opgevraagd die niet door de gebruiker wordt veranderd 
            # bij iedere conditie is aangegeven welke informatie wordt veranderd en welke niet

            overlapping = False        
            # locatie True && eindTijd False && startTijd False 
            if 'locatie' in data_om_te_veranderen and 'eindTijd' not in data_om_te_veranderen and 'startTijd' not in data_om_te_veranderen:
                overlapping = evenementen_overlapping_controle(event_info['startTijd'], event_info['eindTijd'], data_om_te_veranderen["locatie"])
            
            # locatie True && eindTijd True && startTijd False
            elif 'locatie' in data_om_te_veranderen and 'eindTijd' in data_om_te_veranderen and 'startTijd' not in data_om_te_veranderen:
                overlapping = evenementen_overlapping_controle(event_info['startTijd'], data_om_te_veranderen['eindTijd'], data_om_te_veranderen["locatie"])
            
            # locatie True && eindTijd False && startTijd True
            elif 'locatie' in data_om_te_veranderen and 'eindTijd' not in data_om_te_veranderen and 'startTijd' in data_om_te_veranderen:
                overlapping = evenementen_overlapping_controle(data_om_te_veranderen['startTijd'], event_info['eindTijd'], data_om_te_veranderen["locatie"])

            # locatie True && startTijd True && eindTijd True
            elif 'startTijd' in data_om_te_veranderen and 'eindTijd' in data_om_te_veranderen and 'locatie' in data_om_te_veranderen:    
                overlapping = evenementen_overlapping_controle(data_om_te_veranderen['startTijd'], data_om_te_veranderen['eindTijd'], event_info["locatie"])
            
            # locatie False && startTijd True && eindTijd False
            elif 'startTijd' in data_om_te_veranderen and 'eindTijd' not in data_om_te_veranderen and 'locatie' not in data_om_te_veranderen:
                overlapping = evenementen_overlapping_controle(data_om_te_veranderen['startTijd'], event_info['eindTijd'], event_info["locatie"])
            
            # locatie False && startTijd False && eindTijd True
            elif 'startTijd' not in data_om_te_veranderen and 'eindTijd' in data_om_te_veranderen and 'locatie' not in data_om_te_veranderen:        
                overlapping = evenementen_overlapping_controle(event_info['startTijd'], data_om_te_veranderen['eindTijd'], event_info["locatie"])

            # als er een overlapping is gedetecteerd, krijgt de gebruiker een foutmelding
            if overlapping != False:
                error_message = f'Overlapping gevonden met evenement {overlapping[0]} op locatie {overlapping[1]}. <br>Starttijd: {overlapping[2]["uur"]:02d}:{overlapping[2]["minuten"]:02d} <br>Eindtijd: {overlapping[3]["uur"]:02d}:{overlapping[3]["minuten"]:02d}'
                return render_template("evenement_wijzigen.html", event_info=event_info, error_message=error_message)
            
            # als er geen overlapping is gedetecteerd, wordt de ingevoerde informatie opgeslagen in de evenementen data
            else:
                evenement_informatie_wijzigen_in_json_data(event_ID_voor_wijzigen, data_om_te_veranderen)

                return redirect(url_for("evenementen_bekijken"))
            
        
        elif "Verwijderen" in request.form:
            # als de gebruiker een evenement verwijdert, wordt opgehaald welk evenement dit is uit de ingevoerde informatie
            evenement_verwijderen_in_json(event_ID_voor_wijzigen)
            return redirect(url_for("evenementen_bekijken"))
        
        
    return render_template("evenement_wijzigen.html", event_info=event_info, presentator_lijst=presentator_lijst, session_gebruiker=session["unieke_ID"])

@app.route("/parkeerplaatsen", methods=["GET", "POST"])
def parkeerplaatsen():
    # het systeem controleert of de gebruiker een parkeerplaats heeft gereserveerd
    session_gebruiker = account_informatie_vinden_in_json(session["unieke_ID"])
   
   # als de gebruiker een parkeerplaats heeft gereserveerd, wordt er doorgegeven dat de parkeerplaats pagina niet de "Reserveren" knop moet weergeven
    if session_gebruiker["parkeerplaats"]:
        plaats_gereserveerd = True
    else:
        plaats_gereserveerd = False

    # het systeem controleert of er nog parkeerplaatsen beschikbaar zijn om te reserveren
    if parkeerplaats_functies.parkeerplaatsen_limiet_controleren():
        return render_template("parkeerplaatsen.html", plaats_gereserveerd=plaats_gereserveerd, reservering_limiet=True)
    
    if request.method == 'POST':

        if "Reserveren" in request.form:
            # als de gebruiker een parkeerplaats reserveert, wordt een parkeerplaats gereserveerd uit de json            
            gereserveerde_parkeerplaats = parkeerplaats_functies.parkeerplaats_reserveren(session["unieke_ID"])
            account_informatie_wijzigen_in_json(session["unieke_ID"], "parkeerplaats", gereserveerde_parkeerplaats)

            plaats_gereserveerd = True

            return render_template("parkeerplaatsen.html", plaats_gereserveerd=plaats_gereserveerd)

        elif "Annuleren" in request.form:
            # als een gebruiker zijn parkeerplaats annuleert, wordt de annulering verwerkt in de json
            parkeerplaats_functies.parkeerplaats_verwijderen(session_gebruiker["parkeerplaats"])
            account_informatie_wijzigen_in_json(session["unieke_ID"], "parkeerplaats", None)

            plaats_gereserveerd = False

            return render_template("parkeerplaatsen.html", plaats_gereserveerd=plaats_gereserveerd)
        
    return render_template("parkeerplaatsen.html", plaats_gereserveerd=plaats_gereserveerd)

@app.route("/gebruikers", methods=['GET', 'POST'])
def gebruikers_beheren():

    if "A" not in session["unieke_ID"]:
        return render_template("toegang_geweigerd.html")
    # deze pagina is alleen beschikbaar voor beheerders, als de gebruiker geen beheerder is, wordt de gebruiker doorgestuurd naar de pagina voor toegang geweigerd
    # het systeem controleert of de huidige gebruiker de "A" voor beheerder in zijn unieke_ID heeft
    identificator_informatie = identificator_informatie_ophalen()

    users = alle_gebruikers_informatie_ophalen()

    if request.method == 'POST':
        # als de gebruiker informatie invoert, wordt gecontroleerd welke informatie is doorgestuurd
        if "presentator_code" in request.form:
            # als de beheerder een presentator code invoert, wordt deze functie aangeroepen
            presentator_code = request.form["presentator_code"]
            # de presentator code wordt opgeslagen in de json file
            presentator_verificatie_code_opslaan_in_json(presentator_code)
            # alle informatie over identificators wordt opgevraagd uit de json file, zodat deze gerenderd kan worden in de html
            identificator_informatie = identificator_informatie_ophalen()

            return render_template("gebruikers.html", users=users, identificator_informatie=identificator_informatie)
 
        if "gebruiker_zoeken" in request.form:
            # als de beheerder een zoekterm invoert, wordt deze functie aangeroepen
            zoekterm = request.form["gebruiker_zoeken"]
            # de ingevoerde zoekterm wordt opgezocht in de gebruikers data
            gevonden_gebruiker_informatie = gebruiker_informatie_zoeken(zoekterm)
            # alle gebruikers die de zoekterm bevatten in hun informatie worden gerenderd op de gebruikers pagina
            return render_template("gebruikers.html", users=gevonden_gebruiker_informatie, identificator_informatie=identificator_informatie)
    
        
        if "Verwijderen" in request.form:
            # als de beheerder een gebruiker verwijdert, wordt opgehaald welke gebruiker dit is uit de ingevoerde informatie
            gebruiker_ID_voor_wijzigen = request.form["unieke_ID"]

            if session["unieke_ID"] == gebruiker_ID_voor_wijzigen:
                # als de beheerder zijn eigen account probeert te verwijderen, wordt deze naast de verwijdering van zijn account ook uitgelogd en uit de session verwijderd
                if users[gebruiker_ID_voor_wijzigen]["parkeerplaats"]:
                    
                    parkeerplaats_om_te_verwijderen = parkeerplaats_functies.parkeerplaats_vinden_op_unieke_code(gebruiker_ID_voor_wijzigen)
                    parkeerplaats_functies.parkeerplaats_verwijderen(parkeerplaats_om_te_verwijderen)

                bezoeker_verwijderen_in_json(gebruiker_ID_voor_wijzigen)
                session.pop("unieke_ID", None)
                return redirect(url_for("log_uit"))
            
            else:
                # er wordt gecontroleerd op alle mogelijke informatie die aangepast moet worden als een gebruiker wordt verwijderd  
                if users[gebruiker_ID_voor_wijzigen]["parkeerplaats"]:

                    parkeerplaats_om_te_verwijderen = parkeerplaats_functies.parkeerplaats_vinden_op_unieke_code(gebruiker_ID_voor_wijzigen)
                    parkeerplaats_functies.parkeerplaats_verwijderen(parkeerplaats_om_te_verwijderen)

                bezoeker_verwijderen_in_json(gebruiker_ID_voor_wijzigen)
                users = alle_gebruikers_informatie_ophalen()
                identificator_informatie = identificator_informatie_ophalen()

                return render_template("gebruikers.html", users=users, identificator_informatie=identificator_informatie)
        
        if "Wijzigen" in request.form:

            gebruiker_ID_voor_wijzigen = request.form["unieke_ID"]

            return redirect(url_for("gebruiker_wijzigen_functie", gebruiker_ID_voor_wijzigen=gebruiker_ID_voor_wijzigen))
        
    return render_template("gebruikers.html", users=users, identificator_informatie=identificator_informatie)
                           
@app.route("/gebruiker_wijzigen", methods=["GET", "POST"])
def gebruiker_wijzigen_functie():

    if "A" not in session["unieke_ID"]:
        return render_template("toegang_geweigerd.html")

    gebruiker_ID_voor_wijzigen = request.args.get("gebruiker_ID_voor_wijzigen")

    gebruiker_info = account_informatie_vinden_in_json(gebruiker_ID_voor_wijzigen)

    nieuwe_unieke_ID = None
    # deze unieke ID wordt later ingevuld als de bevoegdheid van de gebruiker wordt gewijzigd
    if request.method == 'POST':
        
        data_om_te_veranderen = {}
        
        for data in request.form:
            
            if request.form[data] != '' and data != "Wijzigen":
               
                if data == "parkeerplaats":
                    parkeerplaats_om_te_verwijderen = parkeerplaats_functies.parkeerplaats_vinden_op_unieke_code(gebruiker_ID_voor_wijzigen)
                    parkeerplaats_functies.parkeerplaats_verwijderen(parkeerplaats_om_te_verwijderen)
                    data_om_te_veranderen[data] = None

                elif data == "bevoegdheid":

                    registratie_aantal_update_bij_bevoegdheid_wijziging(gebruiker_ID_voor_wijzigen)
                    nieuwe_unieke_ID = unieke_identificator_generator.unieke_registratie_code_generator(request.form[data])
                    data_om_te_veranderen[data] = request.form[data]
                    data_om_te_veranderen["unieke_ID"] = nieuwe_unieke_ID
                    
                else:
                    data_om_te_veranderen[data] = request.form[data]
        # als er geen te veranderen data is, wordt gebruiker teruggestuurd naar gebruikers_beheren pagina zonder verandering aan te brengen.
        if len(data_om_te_veranderen) == 0:
            return redirect(url_for("gebruikers_beheren"))
        

        # omdat het veranderen van de bevoegdheid van een gebruiker ook de unieke_ID veranderd, naar een die de bijbehorende letter bevat,
        # moet dit ook aangepast worden in alle evenementen waar deze gebruiker is ingeschreven.
        if "bevoegdheid" in data_om_te_veranderen:
            
            # eerst wordt er bij de gebruikers oude unieke_ID bij al ingeschreven evenementen verwijderd. 
            for event_ID in gebruiker_info["evenementen"]:
                bezoeker_uitschrijven_evenement_in_json(event_ID, gebruiker_ID_voor_wijzigen)

            # daarna kan in json alle doorgegeven te veranderen data van de form worden aangepast in de json.
            bezoeker_informatie_wijzigen_in_json_data(gebruiker_ID_voor_wijzigen, data_om_te_veranderen)

            # pas daarna kan de gebruiker weer voor alle evenementen opnieuw ingeschreven met zijn nieuwe unieke_ID
            for event_ID in gebruiker_info["evenementen"]:
                bezoeker_inschrijven_evenement_in_json(event_ID, nieuwe_unieke_ID)
        else:
            # als bevoegdheid niet veranderd is, hoeft er geen nieuwe unieke_ID aangemaakt te worden
            # en kan de te veranderen data meegegeven worden zonder deze aanpassingen.
            bezoeker_informatie_wijzigen_in_json_data(gebruiker_ID_voor_wijzigen, data_om_te_veranderen)

        
        if gebruiker_ID_voor_wijzigen == session["unieke_ID"] and "bevoegdheid" in data_om_te_veranderen: 
            return redirect(url_for("unieke_ID_bevestigen", unieke_ID=nieuwe_unieke_ID))

        return redirect(url_for("gebruikers_beheren"))
    
    
    return render_template("gebruiker_wijzigen.html", user_info=gebruiker_info )