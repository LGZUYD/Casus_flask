# Casus Flask Install

### Vereisten
**python 3.10+**<br/>
**pytest**

## Installeren

1. Open de geleverde project map in vscode of text editor met voorkeur

2. Open in vscode 

3. Open terminal in vscode [ Ctrl + ` ]

4. Type de volgende commands in terminal om Virtual Enviroment en Flask te installen:

### Windows:
``` bash
py -3 -m venv .venv
.venv\Scripts\activate
pip install Flask
```
### MacOS/Linux:
``` bash
python3 -m venv .venv
. .venv/bin/activate
```

5. Om de applicatie te runnen type dit in terminal:
``` bash
flask run
```

6. In terminal staat nu het volgende, open deze in browser **[ CTRL + Click ]** :

> * Running on http://127.0.0.1:5000

 CTRL + C in terminal om Flask af te sluiten

7.	Bij het eerste gebruik van de applicatie zijn er voorbeeldaccounts geleverd voor elke gebruikersrol:

    **Beheerder account:**<br/>
    Inlogcode : **A-0**<br/>
    Wachtwoord: **test**<br/>
        
    **Presentator account:<br/>**
    Inlogcode: **P-0**<br/>
    Wachtwoord: **test**<br/>

    **Bezoekers account:<br/>**
    Inlogcode: **G-0**<br/>
    Wachtwoord: **test**<br/>
    
Deze gebruikers kunnen veilig worden verwijderd of gewijzigd in het Bezoekers-scherm

8. Om de geleverde unittests uit te voeren, wordt gebruik gemaakt van 'pytest'<br/>
**Let op:** Bij het uitvoeren van de unittests worden de ingebouwde functies gebruikt voor het bewerken van de JSON-gegevens met betrekking tot gebruikersregistratie. Als de unittests worden uitgevoerd, worden de gegevens in "identificators.json" bijgewerkt en komen ze niet meer overeen met de werkelijke geregistreerde gebruikers data en moeten ze handmatig worden teruggezet naar hun oorspronkelijke waarden.
