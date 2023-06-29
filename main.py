

def make_dic_stations(txt):
    list_lines = txt.readlines()

    stations = {}

    for line in list_lines:

        line = line.strip()
        if line[0: 1] == 'V':
            list_line = line.split(' ', 2)
        elif line[0: 1] == 'E':
            list_line = line.split(' ', 3)
        else:
            list_line = line

        if list_line[0] == 'V':
            stations[int(list_line[1])] = [list_line[2], [], []]

        elif list_line[0] == 'E':

            stations[int(list_line[1])][1].append(int(list_line[2]))
            stations[int(list_line[1])][2].append(int(list_line[3]))

            if int(list_line[1]) == 259:
                continue
            if int(list_line[1]) == 196:
                continue
            if int(list_line[1]) == 373:
                continue
            if int(list_line[1]) == 36 and int(list_line[2]) == 198:
                continue
            if int(list_line[1]) == 198:
                continue
            if int(list_line[1]) == 52:
                continue
            if int(list_line[1]) == 145 and int(list_line[2]) == 373:
                continue
            if int(list_line[1]) == 201:
                continue
            stations[int(list_line[2])][1].append(int(list_line[1]))
            stations[int(list_line[2])][2].append(int(list_line[3]))

    return stations


def make_dic_liaisons(dic_station):
    liaisons = {}

    for station in dic_station:

        if (dic_station[station][0] in liaisons):
            liaisons[dic_station[station][0]].append(station)
        else:
            liaisons[dic_station[station][0]] = [station]

    change_size = 1

    while change_size:
        change_size = 0

        for liaison in liaisons:

            if len(liaisons[liaison]) == 1:

                del liaisons[liaison]
                change_size = 1
                break

    return liaisons


def make_dic_lignes(dic_station):

    lignes = {'1': [130], '2': [256], '3': [251], '3bis': [279], '4': [268], '5': [28], '6': [57], '7': [152], '7bis': [170], '8': [240], '9': [253], '10': [37], '11': [68], '12': [276], '13': [72], '14': [24]}

    for ligne in lignes:
        lignes[ligne] = find_line(lignes[ligne][0], dic_station, [])

    return lignes

def find_line(n_station, dic_station, ligne):

    if n_station in ligne:
        return ligne

    ligne += [n_station]

    for connexion in dic_station[n_station][1]:

        if dic_station[connexion][0] != dic_station[n_station][0]:
            ligne = find_line(connexion, dic_station, ligne)

    return ligne


def find_shortest_way(n_station, station_rech, way, dico_station, best_time=None):
    #print(n_station)

    if n_station in station_rech:
        return True

    way_list = []

    for station in dico_station[n_station][1]:

        if station in way[0]:
            continue

        own_time = dico_station[n_station][2][dico_station[n_station][1].index(station)]

        if (type(best_time) == int and (best_time < sum(way[1]) + own_time)) or sum(way[1]) + own_time >= 3000:
            continue

        else:
            essai = find_shortest_way(station, station_rech, [way[0] + [n_station], way[1] + [own_time]], dico_station, best_time)

            if type(essai) == bool and essai is True:
                if best_time is None or (sum(way[1]) + own_time) < best_time:
                    best_time = sum(way[1]) + own_time
                    way_list = [way[0] + [n_station, station], way[1] + [own_time]]

            if type(essai) == list:
                if best_time is None or sum(essai[1]) < best_time:
                    best_time = sum(essai[1])
                    way_list = essai

    if len(way_list) == 0:
        return False

    return way_list

def get_line(n_station, dico_line):

    for line in dico_line:
        if n_station in dico_line[line]:

            return line

def find_direction(trajet, n_station, dico_station, dico_line):

    line = get_line(trajet[0], dico_line)

    if n_station in trajet:
        return False
    elif get_line(n_station, dico_line) != line:
        return False
    else:
        res = []

        for station in dico_station[n_station][1]:
            if n_station not in dico_station[station][1]:
                continue

            search = find_direction(trajet + [n_station], station, dico_station, dico_line)

            if type(search) == bool:
                if search is not True:
                    continue

            if type(search) == list:
                for terminus in search:
                    res.append(terminus)

        if len(res) == 0:
            res.append(n_station)

        return res

def affiche_direction(last_station, station, dico_station, dico_line):
    dir = find_direction([last_station], station, dico_station, dico_line)

    text = ''

    for direction in dir:
        text += dico_station[direction][0]

        if direction != dir[-1]:
            text += ' ou '

    print("Direction ", text, ", jusqu'à ", dico_station[station][0])


def connexite(dico_station, n_station, list_conn):

    list_conn.append(n_station)

    if len(list_conn) == len(dico_station):
        return True

    res = []

    for station in dico_station[n_station][1]:

        if station in list_conn:
            continue

        res = connexite(dico_station, station, list_conn)

        if type(res) == bool and res is True:
            return True

    if type(res) == list and len(res) == 0:
        res = False

    return res


def show_path(dep_station, fin_station, dico_station, dico_line):

    if len(dep_station) > 1:
        try_start = []
        timer = []

        for n in dep_station:
            try_start.append(find_shortest_way(n, fin_station, [[], []], dico_station))
            timer.append(sum(try_start[-1][1]))

        path = try_start[timer.index(min(timer))]
    else:
        path = find_shortest_way(dep_station[0], fin_station, [[], []], dico_station)

    time = sum(path[1])
    actual_line = None
    last_station = None

    for station in path[0]:

        if len(path[0]) == path[0].index(station) + 1:

            affiche_direction(last_station, station, dico_station, dico_line)

            print("Vous êtes arrivé à ", dico_station[station][0], " ; Temps de trajet : ", (time // 60), " minutes et ", (time % 60), " secondes.")

        if actual_line != get_line(station, dico_line):
            if actual_line != None:
                before_last_station = path[0][path[0].index(last_station) - 1]
                affiche_direction(before_last_station, last_station, dico_station, dico_line)

                actual_line = get_line(station, dico_line)
                print("Puis prenez la ligne ", actual_line)

            else:
                actual_line = get_line(station, dico_line)

                print("Vous êtes à ", dico_station[station][0])
                print("Prenez la ligne ", actual_line)

        last_station = station

    return True

def search_station_word(answer, dico_station):
    station_poss = [[], []]

    for station in dico_station:

        if answer not in dico_station[station][0] and answer not in dico_station[station][0].lower() and answer not in \
                dico_station[station][0].upper():
            continue
        else:
            if len(station_poss[0]) == 0 or dico_station[station][0] != dico_station[station_poss[0][-1]][0]:
                station_poss[0].append(station)
                station_poss[1].append([station])
            else:
                station_poss[1][-1].append(station)

    if len(station_poss[0]) == 0:
        return None
    elif len(station_poss[0]) == 1:
        print("\nUne station a été trouvée correspondant à votre entrée\n")
    else:
        print("\nPlusieurs stations correspondent à votre entrée\n")
    for n in station_poss[0]:
        print(station_poss[0].index(n), " : ", dico_station[n][0])
    print(len(station_poss[0]), " : Retour\n")

    return station_poss

def check_str_is_right_digit(str_selec, taille_poss):

    #Vérifies que c'est bien un chiffre ou nombre
    for charc in str_selec:
        if not charc.isdigit():
            print("\nErreur : La réponse donnée doit être décimale")
            return False

    #Si oui on le convertit en int
    try_selec = int(str_selec)

    #Vérifies que le int est raisonné
    if try_selec < 0 or try_selec > taille_poss:
        print("\nAucun de ces numéros n'est proposé, choisissez un numéro entre 0 et ", taille_poss)
        return False
    else:
        return try_selec

def answer_find_station(dico_station, quelle_station):

    #Tourne tant que la station n'a pas été trouvée
    while True:
        print("\nVeuillez m'indiquer votre station ", quelle_station, " : ")
        answer = str(input())

        #Evite les recherches inutiles
        if answer != ' ' and answer != '':
            station_poss = search_station_word(answer, dico_station)
            print(station_poss)
        else:
            station_poss = None

        #Si aucune station trouvée revient au début de la boucle
        if station_poss is None:
            print("\nAucune station n'a été trouvée correspondant à votre entrée\n")
            continue

        #Clé permettant de bloquer toute réponse inadéquate
        clear = False
        while not clear:

            select = input("Veuillez entrer le numéro de la station souhaitée : ")

            #Cherche si la réponse est un bon chiffre, renvoie False si non-chiffre ou chiffre non compris
            select = check_str_is_right_digit(select, len(station_poss[0]))

            if type(select) != bool:

                #Vérifie si la réponse est retour
                if select == len(station_poss[0]):
                    clear = True
                # Sinon renvoies le numéro de la station choisie
                else:
                    print("Vous avez choisi : ", dico_station[station_poss[0][select]][0])
                    return station_poss[1][select]



def ask_me(dico_station, dico_line):
    print("Bonjour,")

    #fonction qui récupère la station recherchée par l'utilisateur
    station_dep = answer_find_station(dico_station, "de départ")
    station_arr = answer_find_station(dico_station, "d'arrivée")

    #Annonce le début de l'itinéraire
    print("\n---------TRAJET---------\n")

    #Cherche et montre le chemin
    show_path(station_dep, station_arr, dico_station, dico_line)


if __name__ == '__main__':
    metro_txt = open("metro.txt", 'r')

    #Fonction qui crée un dictionnaire de stations tel que : {numéro de station : [[nom][stations liées][temps des stations liées]]
    dic_stations = make_dic_stations(metro_txt)
    """for station in dic_stations:
        print(station, ' : ', dic_stations[station])"""

    #Fonction qui crée un dictionnaire des stations alterego
    dic_liaisons = make_dic_liaisons(dic_stations)
    #print(dic_liaisons)

    #fonction qui crée un dictionnaire des lignes du type {numéro de ligne : [stations]}
    dic_lignes = make_dic_lignes(dic_stations)
    #print(dic_lignes)

    #Fonction qui vérifie la connexité du graphe, renvoie True si connexe
    check = connexite(dic_stations, 0, [])
    #print(check)

    #Fonction gérant l'interaction avec l'utilisateur pour trouver le chemin le plus rapide
    ask_me(dic_stations, dic_lignes)

