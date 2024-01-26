from flask import Flask, render_template, request, redirect, url_for, flash, session
from gebruikers import *
from json_functies import *
import unieke_identificator_generator
import parkeerplaats_functies

app = Flask(__name__)
app.secret_key = "dhbbh"
@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/account_aanmaken', methods=['GET', 'POST'])
def aanmeld_submit():

    if request.method == 'POST':
        #
        nieuwe_gebruiker = Gebruiker(request.form['name'], bevoegdheid=request.form["bevoegdheid"])
        #
        account_aanmaken_in_json(nieuwe_gebruiker)
        # dit is misschien dubbel... niet optimaal maar t werkt wel 
        return redirect(url_for("unieke_ID_bevestigen", unieke_ID=nieuwe_gebruiker.unieke_ID))
    
    return render_template("account_aanmaken.html")


@app.route('/account_aanmaken/ID_bevestigen')
def unieke_ID_bevestigen():
    
    # als account aangemaakt wordt, wordt huidige gebruiker uitgelogd
    session.pop("unieke_ID", None)
    unieke_ID = request.args.get("unieke_ID")    
    
    return render_template("account_aanmaken_ID_bevestigen.html", unieke_ID=unieke_ID)
  

@app.route('/inloggen', methods=['GET', 'POST'])
def inlog_submit():

    if request.method == 'POST':

        inlog_code = request.form["unieke_code"]

        session["unieke_ID"] = inlog_code

        # hier komen if statements omheen voor error checking dus dit is niet dubbel
        account_data_unieke_ID = account_informatie_vinden_in_json(inlog_code)["unieke_ID"]
        #

        # instances van objects als argument meegegeven gaat niet(of iig moeilijk), daarom pas in /home een instance maken met de data
        
        return redirect(url_for("gebruiker_home", unieke_ID=account_data_unieke_ID))
    
    else:

        if "unieke_ID" in session:
            inlog_code = session["unieke_ID"]
            return redirect(url_for("gebruiker_home", unieke_ID=inlog_code))
        
        return render_template("inloggen.html")
    
@app.route("/logout")
def log_uit():
    session.pop("unieke_ID", None)
    return redirect(url_for("hello_world"))

@app.route("/home")
def gebruiker_home():
    
    if "unieke_ID" not in session and session["unieke_ID"] != request.args.get("unieke_ID"):
            return render_template("toegang_geweigerd.html")
    
    else:
        
        huidige_gebruiker_ID = session["unieke_ID"] or request.args.get("unieke_ID")

        account_instance = gebruiker_instance_aanmaken_met_json_data(huidige_gebruiker_ID)
        
        return render_template("home.html", account_instance=account_instance)
     

@app.route('/evenement_aanmaken', methods=['GET', 'POST'])
def evenement_aanmaken():

    if "A" not in session["unieke_ID"] and "P" not in session["unieke_ID"]:
        return render_template("toegang_geweigerd.html")
    
    huidige_presentator = False

    if "P" in session["unieke_ID"]:
        presentator_gebruiker_info = account_informatie_vinden_in_json(session["unieke_ID"])
        huidige_presentator = True

    presentator_lijst = presentator_lijst_uit_json_maken()

    if request.method == 'POST':

     
        startTijd = request.form['startTijd']
        eindTijd = request.form['eindTijd']
        locatie = request.form['locatie']

        overlapping = evenementen_overlapping_controle(startTijd, eindTijd, locatie)

        if overlapping != False:

            error_message = f'Overlapping gevonden met evenement {overlapping[0]} op locatie {overlapping[1]}. <br>Starttijd: {overlapping[2]["uur"]:02d}:{overlapping[2]["minuten"]:02d} <br>Eindtijd: {overlapping[3]["uur"]:02d}:{overlapping[3]["minuten"]:02d}'          
            return render_template("evenement_aanmaken.html", error_message=error_message, huidige_presentator=huidige_presentator) 

        # De 'presentator' invul optie op de pagina wordt alleen maar weergegeven bij beheerders die een evenement aanmaken,
        # Als een presentator een evenement aanmaakt, wordt dit veld automatisch als presentator ingevuld.
        try:
            presentator_naam = account_informatie_vinden_in_json(request.form["presentator"])["naam"]
            presentator = {request.form["presentator"] : presentator_naam}
        except:
            presentator = {session["unieke_ID"] : presentator_gebruiker_info["naam"]} 
        

        nieuw_evenement = Evenement(
        naam=request.form['evenementnaam'],
        locatie=request.form['locatie'],
        startTijd=startTijd,
        eindTijd=eindTijd,
        presentator=presentator,
        bezoekers_limiet=request.form['bezoekers_limiet'],
        beschrijving=request.form['beschrijving'])

        evenement_aanmaken_in_json(nieuw_evenement)

        return redirect(url_for("evenementen_bekijken"))
        
    return render_template("evenement_aanmaken.html", huidige_presentator=huidige_presentator, presentator_lijst=presentator_lijst) 



@app.route('/evenementen', methods=['GET', 'POST'])
def evenementen_bekijken():
    
    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)

    session_gebruiker = session["unieke_ID"]
    session_acc_bevoegdheid = account_informatie_vinden_in_json(session_gebruiker)["bevoegdheid"]    
    #evenementen die meegegeven worden aan html
    eventlist = []

    for event in data:
        eventlist.append(data[event])
        
    if request.method == 'POST':
       
        if "Inschrijven" in request.form:

            # ?
            session_acc_naam = account_informatie_vinden_in_json(session["unieke_ID"])["naam"]
            
            event_ID_voor_inschrijven = eventlist[int(request.form["index"])]["event_ID"]
            
            bezoeker_inschrijven_evenement_in_json(event_ID_voor_inschrijven, session_gebruiker)
            return redirect(url_for("evenementen_bekijken"))             
            
            
        elif "Uitschrijven" in request.form:
            
            event_ID_voor_uitschrijven = eventlist[int(request.form["index"])]["event_ID"]

            bezoeker_uitschrijven_evenement_in_json(event_ID_voor_uitschrijven, session_gebruiker)
            
            return redirect(url_for("evenementen_bekijken"))
        
        elif "Verwijderen" in request.form:
        
            event_ID_voor_uitschrijven = eventlist[int(request.form["event_ID"])]["event_ID"]
            gebruiker_id_voor_uitschrijven = request.form["unieke_ID"]

            bezoeker_uitschrijven_evenement_in_json(event_ID_voor_uitschrijven, gebruiker_id_voor_uitschrijven) 

            return redirect(url_for("evenementen_bekijken"))

        elif "Wijzigen" in request.form:

            event_ID_voor_wijzigen = eventlist[int(request.form["index"])]["event_ID"]
            
            return redirect(url_for("evenement_wijzigen", event_ID_voor_wijzigen=event_ID_voor_wijzigen))

            
    return render_template("evenementen.html", len=len(eventlist), eventlist=eventlist, bevoegdheid=session_acc_bevoegdheid, session_gebruiker=session_gebruiker)
    # append alleen evenementen waar de gebruiker voor aangemeld is
    # for event in data:
    #     if session["unieke_ID"] in event["aanmeldingen"]:
    #                              # data[event]["aanmelding"] ?
    #         eventlist.append(data[event])
    

@app.route("/evenement_wijzigen", methods=['GET', 'POST'])
def evenement_wijzigen():
    
    if "A" not in session["unieke_ID"] and "P" not in session["unieke_ID"]:
        return render_template("toegang_geweigerd.html")

    event_ID_voor_wijzigen = request.args.get("event_ID_voor_wijzigen")

    event_info = evenement_informatie_vinden_in_json(event_ID_voor_wijzigen)
    
    presentator_lijst = presentator_lijst_uit_json_maken()
    
    if request.method == 'POST':

        if "Wijzigen" in request.form:
            
            data_om_te_veranderen = {}

            for i in request.form:
                if request.form[i] != '' and i != "Wijzigen":

                    if i == "presentator":     
                        presentator_naam = account_informatie_vinden_in_json(request.form[i])["naam"]
                        data_om_te_veranderen[i] = {request.form[i] : presentator_naam}
                    else:
                        data_om_te_veranderen[i] = request.form[i]

            if len(data_om_te_veranderen) == 0:
                return redirect(url_for("evenementen_bekijken"))
            
            # dit controleert op alle mogelijke combinaties van informatie dat betrekking heeft op overlappingsmogelijkheid      
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

            if overlapping != False:
                error_message = f'Overlapping gevonden met evenement {overlapping[0]} op locatie {overlapping[1]}. <br>Starttijd: {overlapping[2]["uur"]:02d}:{overlapping[2]["minuten"]:02d} <br>Eindtijd: {overlapping[3]["uur"]:02d}:{overlapping[3]["minuten"]:02d}'
                return render_template("evenement_wijzigen.html", event_info=event_info, error_message=error_message)

            else:

                evenement_informatie_wijzigen_in_json_data(event_ID_voor_wijzigen, data_om_te_veranderen)

                return redirect(url_for("evenementen_bekijken"))
            
        
        elif "Verwijderen" in request.form:

            evenement_verwijderen_in_json(event_ID_voor_wijzigen)
            return redirect(url_for("evenementen_bekijken"))
        
        
    return render_template("evenement_wijzigen.html", event_info=event_info, presentator_lijst=presentator_lijst, session_gebruiker=session["unieke_ID"])

@app.route("/parkeerplaatsen", methods=["GET", "POST"])
def parkeerplaatsen():

    session_gebruiker = account_informatie_vinden_in_json(session["unieke_ID"])
   
    if session_gebruiker["parkeerplaats"]:
        plaats_gereserveerd = True
    else:
        plaats_gereserveerd = False
        
    print(plaats_gereserveerd)

    if request.method == 'POST':

        if "Reserveren" in request.form:
            
            gereserveerde_parkeerplaats = parkeerplaats_functies.parkeerplaats_reserveren(session["unieke_ID"])
            account_informatie_wijzigen_in_json(session["unieke_ID"], "parkeerplaats", gereserveerde_parkeerplaats)

            plaats_gereserveerd = True

            return render_template("parkeerplaatsen.html", plaats_gereserveerd=plaats_gereserveerd)

        elif "Annuleren" in request.form:
            parkeerplaats_functies.parkeerplaats_verwijderen(session_gebruiker["parkeerplaats"])
            account_informatie_wijzigen_in_json(session["unieke_ID"], "parkeerplaats", None)

            plaats_gereserveerd = False

            return render_template("parkeerplaatsen.html", plaats_gereserveerd=plaats_gereserveerd)
        
    return render_template("parkeerplaatsen.html", plaats_gereserveerd=plaats_gereserveerd)

@app.route("/gebruikers", methods=['GET', 'POST'])
def gebruikers_beheren():
    
    users = alle_gebruikers_informatie_ophalen()

    if request.method == 'POST':
    
        gebruiker_ID_om_te_verwijderen = request.form["unieke_ID"]
        
        if session["unieke_ID"] == gebruiker_ID_om_te_verwijderen:
            session.pop("unieke_ID", None)
            return redirect(url_for("log_uit"))
            
        bezoeker_verwijderen_in_json(gebruiker_ID_om_te_verwijderen)

        users = alle_gebruikers_informatie_ophalen()
        return render_template("gebruikers.html", users=users)
    
            
    return render_template("gebruikers.html", users=users)
                           
