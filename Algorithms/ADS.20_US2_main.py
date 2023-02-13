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
a = {}

listOfGVBFiles = {
    "1": "data/GVB_1_1.json", "2": "data/GVB_2_1.json", "3": "data/GVB_3_1.json",
    "4": "data/GVB_4_1.json", "5": "data/GVB_5_1.json", "7": "data/GVB_7_1.json",
    "11": "data/GVB_11_1.json", "12": "data/GVB_12_1.json", "13": "data/GVB_13_1.json",
    "14": "data/GVB_14_1.json", "15": "data/GVB_17_1.json", "19": "data/GVB_19_1.json",
    "24": "data/GVB_24_1.json", "26": "data/GVB_26_1.json", "50": "data/GVB_50_1.json",
    "51": "data/GVB_51_1.json", "52": "data/GVB_52_1.json", "53": "data/GVB_53_1.json",
    "54": "data/GVB_54_1.json"}


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
        allNetworkInfo = lineData[mainItem]['Network']
        a[idOfTransportation] = []
        for networkItem in allNetworkInfo:
            # usually there are 1 or 2 networkItems that each represent a list of network stops. Scan all stops PER NETWORKITEM
            for networkStop in allNetworkInfo[networkItem]:
                # add a stop to a list based on its order; this is described by UserStopOrderNumber .. but only when it does not exist already
                stationOrderNumber = allNetworkInfo[networkItem][networkStop]['UserStopOrderNumber']
                stationName = allNetworkInfo[networkItem][networkStop]['TimingPointName']
                if (stationOrderNumber, stationName) not in a[idOfTransportation]:
                    a[idOfTransportation].append((stationOrderNumber, stationName))
                print(f"Station: {stationName} is de {stationOrderNumber}e halte")


def readGVBTrack(track):
    """Read gvb track info based on track number."""
    try:
        gvbJSONFileName = listOfGVBFiles[str(track)]
        readGVBLineInfo(gvbJSONFileName)
        # print(len(a["50"]))
    except KeyError:
        print(f"Niet mogelijk om lijn {track} in te lezen omdat deze niet bestaat")


# ------------------------------------------------
def startYourCode():
    """Basis functie van waaruit je eigen routines kan aanroepen.

    Onderstaande code is gewoon een voorbeeld
    """
    print("Currently you are in TEST MODUS ...")


# -------------------------------------------------
def addTwoNumbers(number1, number2):
    """Functie is bedoeld om de werking van PYTEST aan te tonen.

    Zodra je PYTEST uitvoert zal deze functie worden getest en een fout opleveren.
    Immers, de functie moet 2 getallen optellen maar geeft alleen de waarde van 1 variabele terug.
    """
    # Deze functie telt de 2 getallen bij elkaar op
    # pas de code aan zodat deze werkt!

    numbers = number1 + number2
    return numbers


def ads_numberOfStationsInTrack(track=1):
    """Telt het aantal stations in lijn <track>."""
    readGVBTrack(track)
    try:
        return len(a[str(track)])
    except KeyError:
        return -1


def ads_nameOfStartStationInTrack(track=1):
    """Output is gelijk aan de naam van het 1e station van lijn <track>."""
    readGVBTrack(track)
    try:
        return sorted(a[str(track)])[0][1]
    except KeyError:
        return "(onbekend)"


def ads_nameOfEndStationInTrack(track=1):
    """Output is gelijk aan de naam van het eindstation van lijn <track>."""
    readGVBTrack(track)
    try:
        return sorted(a[str(track)])[-1][1]
    except KeyError:
        return "(onbekend)"


def ads_listOfStationsInTrack(track=1):
    """Output gelijk aan de namen van de stations van lijn <track>."""
    readGVBTrack(track)
    try:
        return [x[1] for x in sorted(a[str(track)])]
    except KeyError:
        return ["(onbekend)"]


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
