import json
# LET OP! Zorg ervoor dat je ME.PY aanpast zodat deze verwijst naar JOUW studentcode
#
# Je kan je eigen code uitvoeren door op de button "RUN" te klikken.
#
# Gebruik de toets-combinatie Cmd+Shift+S (MacOS) of Ctrl+Shift+S bij andere operating systemen om de terminal te tonen.
#
# -----------------------------------------------
# FUNCTIONEEL TESTEN
# Type in de terminal het commando "pytest" in en druk op Enter.
# Bekijk de uitkomsten en zorg ervoor dat er GEEN FAILURES zijn
#
# -----------------------------------------------
# STYLE GUIDE
# Type in de terminal het commando "pycodestyle" en druk op Enter.
# Bekijk de uitkomsten en zorg ervoor dat er GEEN FAILURES zijn
#
# -----------------------------------------------
# DOCUMENTATIE CONVENTIES
# Type in de terminal het commando "pydocstyle" en druk op Enter.
# Bekijk de uitkomsten en zorg ervoor dat er GEEN FAILURES zijn
#
# -----------------------------------------------
# INLEVEREN OPDRACHT TER GOEDKEURING
# Werkt alles functioneel? Is de stijl in orde? EN de documentatie?
# Haal het commentaar teken voor SUBMIT weg en plaats deze voor de optie TEST.
# Druk opnieuw op RUN
# Voer je wachtwoord in (het systeem vraagt hier om).
#
# MODE = "TEST"
MODE = "SUBMIT"
# ------------------------------------------------
# Hieronder kan je je eigen code toevoegen.....
#
# Example code you can use
a = []


def getGVBLineInfo(gvbJSONFileName):
    """Open GVB JSON file."""
    try:
        with open(gvbJSONFileName,) as gvbFileObject:
            return json.load(gvbFileObject)
    except FileNotFoundError:
        print(f'File not found ({gvbJSONFileName})')
        return -1
    else:
        print('No able to open the file ')
        return -1


def readGVBLineInfo(gvbJSONFileName):
    """Leest GVB informatie in uit een JSON bestand."""
    lineData = getGVBLineInfo(gvbJSONFileName)
    if (lineData == -1):
        return -1

    for mainItem in lineData:
        # There should be only 1 mainItem that starts with something like "GVB_"
        # We need this to access the other information
        # First read the transportation type and its id
        lineInfo = lineData[mainItem]['Line']
        typeOfTransportation = lineInfo['TransportType']
        idOfTransportation = lineInfo['LinePublicNumber']
        print(f"Inlezen: {typeOfTransportation} {idOfTransportation}")
        # read the network for this line
        allNetworkInfo = lineData[mainItem]['Network']['611354433']
    for networkStop in allNetworkInfo:
        # add a stop to a list based on its order; this is described by  UserStopOrderNumber .. but only when it does not exist already
        stationOrderNumber = allNetworkInfo[networkStop]['UserStopOrderNumber']
        stationName = allNetworkInfo[networkStop]['TimingPointName']
        a.append((stationOrderNumber, stationName))
# print(f"Station: {stationName} is de {stationOrderNumber}e halte")
    for trams in sorted(a):
        element_one = trams[0]
        element_two = trams[1]
        print(f"Station: {element_two} is de {element_one}e halte")


print("Currently you are in TEST MODUS ...")
readGVBLineInfo("data/GVB_1_1.json")


# ------------------------------------------------
def startYourCode():
    """Basis functie van waaruit je eigen routines kan aanroepen.

    Onderstaande code is gewoon een voorbeeld
    """


# -------------------------------------------------
def addTwoNumbers(number1, number2):
    """Functie is bedoeld om de werking van PYTEST aan te tonen.

    Zodra je PYTEST uitvoert zal deze functie worden getest en een fout opleveren.
    Immers, de functie moet 2 getallen optellen maar geeft alleen de waarde van 1 variabele terug.
    """
    numbers = number1 + number2
    # Deze functie telt de 2 getallen bij elkaar op
    # pas de code aan zodat deze werkt!
    return numbers


def ads_numberOfStationsInTrack():
    """Telt het aantal stations in lijn 1."""
    return len(a)


def ads_nameOfStartStationInTrack():
    """Output is gelijk aan de naam van het 1e station van lijn 1."""
    return sorted(a)[0][1]


def ads_nameOfEndStationInTrack():
    """Output is gelijk aan de naam van het eindstation van lijn 1."""
    return sorted(a)[-1][1]


def ads_listOfStationsInTrack():
    """Output gelijk aan de namen van de stations van lijn 1."""
    alle_namen = []
    for halte_naam in sorted(a):
        alle_namen.append(halte_naam[1])
    return alle_namen


# -------------------------------------------------
# please do NOT edit the part below
def main():
    """Functie kijkt naar de gewenste MODUS en voert bijbehorende actie uit."""
    if MODE == "TEST":
        startYourCode()
    elif MODE == "SUBMIT":
        from submit import submitCode
        submitCode()
    else:
        print("Onbekend MODUS ... gebruik of TEST of SUBMIT")


if __name__ == "__main__":
    main()
