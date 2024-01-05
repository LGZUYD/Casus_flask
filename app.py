from flask import Flask, render_template, request, redirect, url_for
from gebruikers import *
from json_functies import *
import unieke_identificator_generator

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/home")
def gebruiker_home():
    
    account_instance = gebruiker_instance_aanmaken_met_json_data(request.args.get("unieke_ID"))

    # hier alle button logic etc maken

    return render_template("home.html", account_instance=account_instance)



@app.route('/account_aanmaken', methods=['GET', 'POST'])
def aanmeld_submit():

    if request.method == 'POST':

        nieuwe_gebruiker = Gebruiker(request.form['name'], bevoegdheid=request.form["bevoegdheid"])
        
        account_aanmaken_in_json(nieuwe_gebruiker)

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

        # hier komen if statements omheen voor error checking dus dit is niet dubbel
        account_data_unieke_ID = account_informatie_vinden_in_json(inlog_code)["unieke_ID"]
        #

        # instances van objects als argument meegegeven gaat niet(of iig moeilijk), daarom pas in /home een instance maken met de data

        return redirect(url_for("gebruiker_home", unieke_ID=account_data_unieke_ID))

    return render_template("inloggen.html")

