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
# LET OP ... US01 en US02 bevatten voorbeelden om een GVB netwerk in te lezen
# daarom staat deze code hier niet meer in


# ------------------------------------------------
# BELANGRIJK!!! Deze functie wordt door PYTEST aangeroepen zodat je je eigen initialisaties kan uitvoeren.
a = {}
b = {}
z = {"nieuw": {}, "nieuwste": {}, }


listOfGVBFiles = {
    "1": "data/GVB_1_1.json", "2": "data/GVB_2_1.json", "3": "data/GVB_3_1.json",
    "4": "data/GVB_4_1.json", "5": "data/GVB_5_1.json", "7": "data/GVB_7_1.json",
    "11": "data/GVB_11_1.json", "12": "data/GVB_12_1.json", "13": "data/GVB_13_1.json",
    "14": "data/GVB_14_1.json", "17": "data/GVB_17_1.json", "19": "data/GVB_19_1.json",
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
        # print(f"Inlezen: {typeOfTransportation} {idOfTransportation}")
        # read the network for this line
        allNetworkInfo = lineData[mainItem]['Network']
        a[idOfTransportation] = []
        b[idOfTransportation] = typeOfTransportation
        for networkItem in allNetworkInfo:
            # usually there are 1 or 2 networkItems that each represent a list of network stops. Scan all stops PER NETWORKITEM
            for networkStop in allNetworkInfo[networkItem]:
                # add a stop to a list based on its order; this is described by UserStopOrderNumber .. but only when it does not exist already
                stationOrderNumber = allNetworkInfo[networkItem][networkStop]['UserStopOrderNumber']
                stationName = allNetworkInfo[networkItem][networkStop]['TimingPointName']
                if (stationOrderNumber, stationName) not in a[idOfTransportation]:
                    a[idOfTransportation].append((stationOrderNumber, stationName))


def readGVBTrack(track):
    """Read gvb track info based on track number."""
    try:
        gvbJSONFileName = listOfGVBFiles[str(track)]
        readGVBLineInfo(gvbJSONFileName)
    except KeyError:
        print(f"Niet mogelijk om lijn {track} in te lezen omdat deze niet bestaat")


def anan(an):
    """Functie om een lijst te sorteren, in mijn geval a -> dict."""
    for i in range(0, len(an) - 1):
        for j in range(0, len(an) - 1 - i):
            if an[j] > an[j + 1]:
                an[j], an[j + 1] = an[j + 1], an[j]
    return an


for lijn in list(listOfGVBFiles.keys()):
    readGVBTrack(lijn)
    # print(anan(a[lijn]))
    a[lijn] = anan(a[lijn])
# print(a)


def eben(lijst, station):
    """Output is de order van <station> in <lijst>."""
    stationNames = []
    for stationName in lijst:
        stationNames.append(stationName[1])
    for i in range(len(lijst)):
        if stationNames[i] == station:
            return i
    return -1


def startYourCode():
    """Basis functie van waaruit je eigen routines kan aanroepen.

    Onderstaande code is gewoon een voorbeeld
    """


def ads_numberOfStationsInTrack(track=1):
    """Telt het aantal stations in lijn <track>."""
    try:
        return len(a[str(track)])
    except KeyError:
        return -1


def ads_nameOfStartStationInTrack(track=1):
    """Output is gelijk aan de naam van het 1e station van lijn <track>."""
    try:
        return a[str(track)][0][1]
    except KeyError:
        return "(onbekend)"


def ads_nameOfEndStationInTrack(track=1):
    """Output is gelijk aan de naam van het eindstation van lijn <track>."""
    try:
        return a[str(track)][-1][1]
    except KeyError:
        return "(onbekend)"


def ads_listOfStationsInTrack(track=1):
    """Output gelijk aan de namen van de stations van lijn <track>."""
    try:
        return [x[1] for x in a[str(track)]]
    except KeyError:
        return ["(onbekend)"]


def ads_listOfTracksGivenStation(station):
    """Output gelijk aan een lijst met integers."""
    try:
        return [int(k) for k, v in a.items() for v in a[k] if station in v]
    except KeyError:
        return []


def ads_isStationOnTrack(track, station):
    """Output gelijk aan True of False."""
    try:
        return station in [item[1] for item in a[str(track)]]
    except KeyError:
        return False


def ads_travelTimeBetweenStationsGivenTrack(track, station_departure, station_arrival):
    """Output gelijk aan de reistijd in minuten van vertrek-naar eindstation."""
    c = []
    o = eben(a[str(track)], station_departure) - eben(a[str(track)], station_arrival)
    for haltes in a[str(track)]:
        c.append(haltes[1])
    if station_departure + station_arrival not in z['nieuw'] and station_departure + station_arrival in z['nieuwste']:
        return z['nieuwste'][station_departure + station_arrival]
    if station_departure + station_arrival in z['nieuw'] and station_departure + station_arrival in z['nieuwste']:
        return z['nieuwste'][station_departure + station_arrival]
    try:
        if o == -1 or o == 1:
            if station_departure in c and station_arrival in c:
                return 1.5
        else:
            return -1
    except KeyError:
        return -1


def ads_changeTravelTimeBetweenStationsGivenTrack(track, station_departure, station_arrival, travel_time):
    """Output gelijk aan de reistijd in minuten van vertrek- naar eindstation vóór de aanpassing."""
    waarde = 0
    o = eben(a[str(track)], station_departure) - eben(a[str(track)], station_arrival)
    c = []
    for haltes in a[str(track)]:
        c.append(haltes[1])
    if station_departure not in c and station_arrival not in c:
        return -1
    if b[str(track)] == 'TRAM':
        waarde = 3
    if b[str(track)] == 'METRO':
        waarde = 1.5
    if station_departure + station_arrival in z['nieuw'] and station_departure + station_arrival in z['nieuwste']:
        z['nieuw'][station_departure + station_arrival] = z['nieuwste'][station_departure + station_arrival]
    if o == -1 or o == 1:
        if station_departure + station_arrival in z['nieuw']:
            z['nieuwste'][station_departure + station_arrival] = travel_time
            return z['nieuw'][station_departure + station_arrival]
        else:
            z['nieuw'][station_departure + station_arrival] = travel_time
            return waarde
    else:
        return -1


def ads_shortestRouteBetweenStations(station_departure, station_arrival, treshold_travel_time=10):
    """Output gelijk aan een list of strings .. zie de opdrachtomschrijving."""
    stations = []
    output = []
    c = []
    treshold = 0
    for haltes in a.keys():
        for i in range(len(a[haltes]) - 1):
            c.append(a[haltes][i][1])
    if (station_departure not in c) or (station_arrival not in c):
        return['error']
    routes = alleRoutes(station_departure)
    for i in range(len(routes) - 1):
        if routes[i][1][-1] == station_arrival:
            for j in range(len(routes[i][1])):
                if any(station_departure in x for x in routes) or any(station_arrival in x for x in routes):
                    return ['unreachable']
                if j + 1 == len(routes[i][1]):
                    continue
                stations.append(alleStations(routes[i][1][j], routes[i][1][j + 1]))
                output.append('lijn: ' + str(stations[j][0]) + ' #instappen: ' + routes[i][1][j] + ' #uitstappen: ' + routes[i][1]
                              [j + 1] + ' #aantal haltes: 1')
                if ads_travelTimeBetweenStationsGivenTrack(stations[j][0], routes[i][1][j], routes[i][1][j + 1]) > treshold_travel_time:
                    return ['unreachable']
                if routes[i][1][j] + routes[i][1][j + 1] in z['nieuw']:
                    if z['nieuw'][routes[i][1][j] + routes[i][1][j + 1]] > treshold_travel_time:
                        return ['unreachable']
                if b[str(alleStations(routes[i][1][j], routes[i][1][j + 1])[0])] == 'TRAM':
                    treshold = 3
                    if treshold > treshold_travel_time:
                        return ['unreachable']
                else:
                    treshold = 1.5
                    if treshold > treshold_travel_time:
                        return ['unreachable']
            return output


def alleStations(station_departure, station_arrival):
    """Output gelijk aan <station_departure> en <station_arrival>."""
    vertrek = ads_listOfTracksGivenStation(station_departure)
    aakomst = ads_listOfTracksGivenStation(station_arrival)
    return list(set(vertrek).intersection(aakomst))


def ads_isEngineerDelayed(station_departure, station_arrival, treshold_travel_time):
    """Output gelijk aan True of False; zie de opdrachtomschrijving."""
    if treshold_travel_time < 0:
        return 0
    if ads_shortestRouteBetweenStations(station_departure, station_arrival, treshold_travel_time) == ['unreachable']:
        return True
    elif ads_shortestRouteBetweenStations(station_departure, station_arrival, treshold_travel_time) != ['unreachable']:
        return False


def ads_fastestRouteBetweenStations(station_departure, station_arrival):
    """Output gelijk aan een list of strings .. zie de opdrachtomschrijving."""
    stations = []
    output = []
    c = []
    for haltes in a.keys():
        for i in range(len(a[haltes]) - 1):
            c.append(a[haltes][i][1])
    if (station_departure not in c) or (station_arrival not in c):
        return['error']
    routes = alleRoutes(station_departure)
    for i in range(len(routes) - 1):
        if routes[i][1][-1] == station_arrival:
            for j in range(len(routes[i][1])):
                if any(station_departure in x for x in routes) or any(station_arrival in x for x in routes):
                    return ['unreachable']
                if j + 1 == len(routes[i][1]):
                    continue
                stations.append(alleStations(routes[i][1][j], routes[i][1][j + 1]))
                output.append('lijn: ' + str(stations[j][0]) + ' #instappen: ' + routes[i][1][j] + ' #uitstappen: ' + routes[i][1]
                              [j + 1] + ' #aantal haltes: 1')
            return output


class Node:
    """Maakt een node in het Dijkstra algoritme."""

    def __init__(self, data, indexloc=None):
        """Initialiseert de class."""
        self.data = data
        self.index = indexloc


class DijkstraNodeDecorator:
    """Maakt nodes bruikbaar voor Dijktra."""

    def __init__(self, node):
        """Initialiseert de class."""
        self.node = node
        self.prov_dist = float('inf')
        self.hops = []

    def index(self):
        """Index volgens Dijkstra algoritme."""
        return self.node.index

    def data(self):
        """."""
        return self.node.data

    def update_data(self, data):
        """."""
        self.prov_dist = data['prov_dist']
        self.hops = data['hops']
        return self


class BinaryTree:
    """."""

    def __init__(self, nodes=[]):
        """Initialiseert de class."""
        self.nodes = nodes

    def root(self):
        """."""
        return self.nodes[0]

    def iparent(self, i):
        """."""
        return (i - 1) // 2

    def ileft(self, i):
        """."""
        return 2 * i + 1

    def iright(self, i):
        """."""
        return 2 * i + 2

    def left(self, i):
        """."""
        return self.node_at_index(self.ileft(i))

    def right(self, i):
        """."""
        return self.node_at_index(self.iright(i))

    def parent(self, i):
        """."""
        return self.node_at_index(self.iparent(i))

    def node_at_index(self, i):
        """."""
        return self.nodes[i]

    def size(self):
        """."""
        return len(self.nodes)


class MinHeap(BinaryTree):
    """."""

    def __init__(self, nodes, is_less_than=lambda a, b: a < b, get_index=None, update_node=lambda node, newval: newval):
        """."""
        BinaryTree.__init__(self, nodes)
        self.order_mapping = list(range(len(nodes)))
        self.is_less_than, self.get_index, self.update_node = is_less_than, get_index, update_node
        self.min_heapify()

    def min_heapify_subtree(self, i):
        """."""
        size = self.size()
        ileft = self.ileft(i)
        iright = self.iright(i)
        imin = i
        if(ileft < size and self.is_less_than(self.nodes[ileft], self.nodes[imin])):
            imin = ileft
        if(iright < size and self.is_less_than(self.nodes[iright], self.nodes[imin])):
            imin = iright
        if(imin != i):
            self.nodes[i], self.nodes[imin] = self.nodes[imin], self.nodes[i]
            if self.get_index is not None:
                self.order_mapping[self.get_index(self.nodes[imin])] = imin
                self.order_mapping[self.get_index(self.nodes[i])] = i
            self.min_heapify_subtree(imin)

    def min_heapify(self):
        """."""
        for i in range(len(self.nodes), -1, -1):
            self.min_heapify_subtree(i)

    def min(self):
        """."""
        return self.nodes[0]

    def pop(self):
        """."""
        min = self.nodes[0]
        if self.size() > 1:
            self.nodes[0] = self.nodes[-1]
            self.nodes.pop()
            if self.get_index is not None:
                self.order_mapping[self.get_index(self.nodes[0])] = 0
            self.min_heapify_subtree(0)
        elif self.size() == 1:
            self.nodes.pop()
        else:
            return None
        if self.get_index is not None:
            self.order_mapping[self.get_index(min)] = None
        return min

    def decrease_key(self, i, val):
        """."""
        self.nodes[i] = self.update_node(self.nodes[i], val)
        iparent = self.iparent(i)
        while(i != 0 and not self.is_less_than(self.nodes[iparent], self.nodes[i])):
            self.nodes[iparent], self.nodes[i] = self.nodes[i], self.nodes[iparent]

            if self.get_index is not None:
                self.order_mapping[self.get_index(self.nodes[iparent])] = iparent
                self.order_mapping[self.get_index(self.nodes[i])] = i
            i = iparent
            iparent = self.iparent(i) if i > 0 else None

    def index_of_node_at(self, i):
        """."""
        return self.get_index(self.nodes[i])


class Graph:
    """."""

    def __init__(self, nodes):
        """."""
        self.adj_list = [[node, []] for node in nodes]
        for i in range(len(nodes)):
            nodes[i].index = i

    def connect_dir(self, node1, node2, weight=1):
        """."""
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        self.adj_list[node1][1].append((node2, weight))

    def connect(self, node1, node2, weight=1):
        """."""
        self.connect_dir(node1, node2, weight)
        self.connect_dir(node2, node1, weight)

    def connections(self, node):
        """."""
        node = self.get_index_from_node(node)
        return self.adj_list[node][1]

    def get_index_from_node(self, node):
        """."""
        if not isinstance(node, Node) and not isinstance(node, int):
            raise ValueError("node must be an integer or a Node object")
        if isinstance(node, int):
            return node
        else:
            return node.index

    def dijkstra(self, src):
        """."""
        src_index = self.get_index_from_node(src)
        dnodes = [DijkstraNodeDecorator(node_edges[0]) for node_edges in self.adj_list]

        dnodes[src_index].prov_dist = 0
        dnodes[src_index].hops.append(dnodes[src_index].node)

        def is_less_than(a, b):
            return a.prov_dist < b.prov_dist

        def get_index(node):
            return node.index()

        def update_node(node, data):
            return node.update_data(data)

        heap = MinHeap(dnodes, is_less_than, get_index, update_node)

        min_dist_list = []

        while heap.size() > 0:
            min_decorated_node = heap.pop()
            min_dist = min_decorated_node.prov_dist
            hops = min_decorated_node.hops
            min_dist_list.append([min_dist, hops])

            connections = self.connections(min_decorated_node.node)

            for (inode, weight) in connections:
                node = self.adj_list[inode][0]
                heap_location = heap.order_mapping[inode]
                if(heap_location is not None):
                    tot_dist = weight + min_dist
                    if tot_dist < heap.nodes[heap_location].prov_dist:
                        hops_cpy = list(hops)
                        hops_cpy.append(node)
                        data = {'prov_dist': tot_dist, 'hops': hops_cpy}
                        heap.decrease_key(heap_location, data)

        return min_dist_list


def hasan():
    """test."""
    x = 0
    for i in a.keys():
        x += len(a[i])
    return x


def alleRoutes(station):
    """."""
    x = {}
    try:
        for line in a.keys():
            for order in range(len(a[line])):
                if a[line][order][1] in x:
                    continue
                x[a[line][order][1]] = Node(a[line][order][1])
        grafiek = Graph(list(x.values()))
        for line in a.keys():
            for order in range(len(a[line]) - 1):
                if order + 1 > (len(a[line]) - 1):
                    continue
                else:
                    grafiek.connect(x[a[line][order][1]], x[a[line][(order + 1)][1]])
        return [(weight, [n.data for n in node]) for (weight, node) in grafiek.dijkstra(x[station])]
    except KeyError:
        return -1

# -------------------------------------------------
# please do NOT edit the part below


def main():
    """."""
    if MODE == "TEST":
        startYourCode()
    elif MODE == "SUBMIT":
        from submit import submitCode
        submitCode()
    else:
        print("Onbekend MODUS ... gebruik of TEST of SUBMIT")


if __name__ == "__main__":
    main()
