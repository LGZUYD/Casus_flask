from flask import Flask, render_template, request, redirect, url_for, flash, session
from gebruikers import *
from json_functies import *
import unieke_identificator_generator

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

    unieke_ID = request.args.get("unieke_ID")    
    
    return render_template("account_aanmaken_ID_bevestigen.html", unieke_ID=unieke_ID)
  

@app.route('/inloggen', methods=['GET', 'POST'])
def inlog_submit():

    if request.method == 'POST':

        inlog_code = request.form["unieke_code"]

        #session
        session["unieke_ID"] = inlog_code

        # hier komen if statements omheen voor error checking dus dit is niet dubbel
        account_data_unieke_ID = account_informatie_vinden_in_json(inlog_code)["unieke_ID"]
        #

        # instances van objects als argument meegegeven gaat niet(of iig moeilijk), daarom pas in /home een instance maken met de data
        
        return redirect(url_for("gebruiker_home", unieke_ID=account_data_unieke_ID))

    return render_template("inloggen.html")


@app.route("/home")
def gebruiker_home():
    
    huidige_gebruiker_ID = request.args.get("unieke_ID")

    account_instance = gebruiker_instance_aanmaken_met_json_data(huidige_gebruiker_ID)
    
    return render_template("home.html", account_instance=account_instance)




@app.route('/evenement_aanmaken', methods=['GET', 'POST'])
def evenement_aanmaken():

    if request.method == 'POST':

        nieuw_evenement = Evenement(
        naam=request.form['evenementnaam'],
        locatie=request.form['locatie'],
        tijd=request.form['tijd'],
        duur=request.form['duur'],
        presentator=request.form['presentator'],
        bezoekers_limiet=request.form['bezoekers_limiet'])

        evenement_aanmaken_in_json(nieuw_evenement)
        

    return render_template("evenement_aanmaken.html") 



@app.route('/evenementen', methods=['GET', 'POST'])
def evenementen_bekijken():
    
    with open("json/evenementen.json", "r") as json_file:
        data = json.load(json_file)

    #evenementen die meegegeven worden aan html
    eventlist = []

    for event in data:
        eventlist.append(data[event])

    if request.method == 'POST':

        session_gebruiker = session["unieke_ID"]

        if "Inschrijven" in request.form:

            session_acc_naam = account_informatie_vinden_in_json(session["unieke_ID"])["naam"]
            
            event_ID_voor_inschrijven = eventlist[int(request.form["index"])]["event_ID"]
            
            bezoeker_inschrijven_evenement_in_json(event_ID_voor_inschrijven, session_gebruiker)

        elif "Uitschrijven" in request.form:
            
            event_ID_voor_uitschrijven = eventlist[int(request.form["index"])]["event_ID"]

            bezoeker_uitschrijven_evenement_in_json(event_ID_voor_uitschrijven, session_gebruiker)

    # append alleen evenementen waar de gebruiker voor aangemeld is
    # for event in data:
    #     if session["unieke_ID"] in event["aanmeldingen"]:
    #                              # data[event]["aanmelding"] ?
    #         eventlist.append(data[event])
    return render_template("evenementen.html", len=len(eventlist), eventlist=eventlist)