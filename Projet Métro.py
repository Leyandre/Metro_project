import pygame, sys
import os
import time

width = 1000
height = 500
framerate = 5

#permet de garder en mémoire la barre de recherhce active
srch_activ = None

class point(object):
    #class permettant de créer et gérer des points sur l'écran

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, point):
            return point(self.x + other.x, self.y + other.y)
        elif isinstance(other, list) or isinstance(other, tuple):
            return point(self.x + other[0], self.y + other[1])
        else:
            raise TypeError("Error : {0} type used instead of list or tuple".format(other))

    def __iadd__(self, other):
        if isinstance(other, point):
            self.x = self.x + other.x
            self.y = self.y + other.y

            return self
        elif isinstance(other, list) or isinstance(other, tuple):
            self.x = self.x + other[0]
            self.y = self.y + other[1]

            return self
        else:
            raise TypeError("Error : {0} type used instead of list or tuple".format(other))

    def __sub__(self, other):
        if isinstance(other, point):
            return point(self.x - other.x, self.y - other.y)
        elif isinstance(other, list) or isinstance(other, tuple):
            return point(self.x - other[0], self.y - other[1])
        else:
            raise TypeError("Error : {0} type used instead of list or tuple".format(other))

    def __isub__(self, other):
        if isinstance(other, point):
            self.x = self.x - other.x
            self.y = self.y - other.y

            return self
        elif isinstance(other, list) or isinstance(other, tuple):
            self.x = self.x - other[0]
            self.y = self.y - other[1]

            return self
        else:
            raise TypeError("Error : {0} type used instead of list or tuple".format(other))

    def __mul__(self, other):
        if isinstance(other, point):
            return point(self.x * other.x, self.y * other.y)
        elif isinstance(other, list) or isinstance(other, tuple):
            return point(self.x * other[0], self.y * other[1])
        else:
            raise TypeError("Error : {0} type used instead of list or tuple".format(other))

    def __imul__(self, other):
        if isinstance(other, point):
            self.x = self.x * other.x
            self.y = self.y * other.y

            return self
        elif isinstance(other, list) or isinstance(other, tuple):
            self.x = self.x * other[0]
            self.y = self.y * other[1]

            return self
        else:
            raise TypeError("Error : {0} type used instead of list or tuple".format(other))

    def __truediv__(self, other):
        if isinstance(other, point):
            return point(self.x / other.x, self.y / other.y)
        elif isinstance(other, list) or isinstance(other, tuple):
            return point(self.x / other[0], self.y / other[1])
        else:
            raise TypeError("Error : {0} type used instead of list or tuple".format(other))

    def __itruediv__(self, other):
        if isinstance(other, point):
            self.x = self.x / other.x
            self.y = self.y / other.y

            return self
        elif isinstance(other, list) or isinstance(other, tuple):
            self.x = self.x / other[0]
            self.y = self.y / other[1]

            return self
        else:
            raise TypeError("Error : {0} type used instead of list or tuple".format(other))

    def g_tuple(self):
        return (self.x, self.y)

class objet(object):
    #class permmettant de gérer des objets pour une interaction avec l'utilisateur
    #tel que des boutons ou une saisie de texte

    def __init__(self, pt, img_name, zone=None):

        self.set_point(pt)
        self.load_img(img_name)
        self.set_zone(zone)
        self.activate = False

    def set_point(self, pt):
        # Crée le point qui sera au milieu de son image

        if isinstance(pt, point):
            self.pt = point(pt.x, pt.y)
        elif isinstance(pt, list) or isinstance(pt, tuple):
            self.pt = point(pt[0], pt[1])
        else:
            raise TypeError("Error : {0} type instead of list, tuple or point".format(type(pt)))

    def load_img(self, name):
        self.img = pygame.image.load(name).convert_alpha()
        self.img = pygame.transform.smoothscale(self.img, ((self.img.get_width() / 1.5), (self.img.get_height() / 1.5)))

    def blit_img(self, screen):
        screen.blit(self.img, ((self.pt.x - (self.img.get_width() / 2)), (self.pt.y - (self.img.get_height() / 2))))

    def set_zone(self, zone):
        #Définie une zone de sélection sur l'image pour l'activation de l'objet

        if zone == None:
            xmin = self.pt.x - (self.img.get_width() / 2)
            ymin = self.pt.y - (self.img.get_height() / 2)

            self.zone = pygame.Rect(xmin, ymin, self.img.get_width(), self.img.get_height())

        elif isinstance(zone, list) or isinstance(zone, tuple):
            if len(zone) == 2:
                xmin = self.pt.x - (zone[0] / 2)
                ymin = self.pt.y - (zone[1] / 2)

                self.zone = pygame.Rect(xmin, ymin, zone[0], zone[1])

        else:
            raise TypeError("Error : {0} type instead of list or tuple".format(type(zone)))

class SearchBar(objet):

    def __init__(self, pt, img_name, font, size_word, limite=None, texte='', color=(0, 0, 0), zone=None):

        objet.__init__(self, pt, img_name, zone)

        self.font = pygame.font.SysFont(font, size_word, True)

        self.update_text(texte, color)


        self.load_img_poss()

        self.limit = limite
        self.selection = None

    def set_def_word(self, word, color=None):
        #définie un mot-descriptif dans la barre de recherche

        #si aucune couleur n'est mentionnée, prend une couleur qui est déjà définie
        #ou une couleur noire
        if color is None:
            if not hasattr(self, 'word_def_color'):
                self.word_def_color = (0, 0, 0)
        else:
            #sinon définie la couleur mentionée comme couleur par défaut
            self.word_def_color = color

        self.txt_word_def = word

        self.word_def = self.font.render(word, True, self.word_def_color)

        #Définie un point sur la gauche de la barre de recherche pour le mot-descriptif
        x = ((self.pt.x - (self.img.get_width() / 3)) - (self.word_def.get_width() / 2) + 5)
        y = (self.pt.y - (self.word_def.get_height() / 2)) + 3
        self.word_def_pt = point(x, y)

        self.update_text(self.text_str)

    def update_text(self, text, color=None):
        #Mets à jour la saisie dans la barre de recherche

        #même que pour le mot-descriptif
        if color is None:
            if not hasattr(self, 'word_def_color'):
                self.txt_color = (0, 0, 0)
        else:
            self.txt_color = color

        self.text = self.font.render(text, True, self.txt_color)
        self.text_str = text

        #redéfinie le point du texte en fonction de la taille du texte et celle du mot-descriptif
        self.set_txt_pt()

        #Gère le cursor du texte
        self.set_cursor()

    def set_txt_pt(self):
        if hasattr(self, 'word_def'):
            x = self.word_def_pt.x + self.word_def.get_width() + 10
        else:
            x = self.pt.x - (self.img.get_width() / 2) + 10
        y = (self.pt.y - (self.text.get_height() / 2)) + 3

        self.text_pt = point(x, y)

    def set_cursor(self):
        x = self.text_pt.x + self.text.get_width()
        ymin = self.pt.y - (self.text.get_height() / 2) + 3
        ymax = self.pt.y + (self.text.get_height() / 2) + 3
        self.cursor_1 = point(x, ymin)

        self.cursor_2 = point(x, ymax)

    def iscursoratend(self):
        if self.pt.x + (self.img.get_width() / 2) - self.cursor_1.x <= 100:
            return True
        else:
            return False

    def load_img_poss(self):
        self.img_1_poss = pygame.image.load("./data/Search_1_poss.png").convert_alpha()
        self.img_1_poss = pygame.transform.smoothscale(self.img_1_poss, ((self.img_1_poss.get_width() / 1.5), (self.img_1_poss.get_height() / 1.5)))
        self.img_1_poss_pt = point(self.pt.x, (self.pt.y + self.img.get_height() - 100))

        self.img_up_poss = pygame.image.load("./data/Search_up_poss.png").convert_alpha()
        self.img_up_poss = pygame.transform.smoothscale(self.img_up_poss, ((self.img_up_poss.get_width() / 1.5), (self.img_up_poss.get_height() / 1.5)))
        self.img_up_poss_pt = point(self.pt.x, (self.pt.y + self.img.get_height() - 100))

        self.img_down_poss = pygame.image.load("./data/Search_down_poss.png").convert_alpha()
        self.img_down_poss = pygame.transform.smoothscale(self.img_down_poss, ((self.img_down_poss.get_width() / 1.5), (self.img_down_poss.get_height() / 1.5)))

        self.img_mid_poss = pygame.image.load("./data/Search_mid_poss.png").convert_alpha()
        self.img_mid_poss = pygame.transform.smoothscale(self.img_mid_poss, ((self.img_mid_poss.get_width() / 1.5), (self.img_mid_poss.get_height() / 1.5)))

    def set_search_stations(self, list_station, dico_station):
        self.station_poss = []
        memory_y = 0

        if len(list_station) < 1:
            list = list_station
        else:
            list = list_station[0]

        for ind, elt in enumerate(list):

            if ind == (self.limit - 1) and len(list_station[0]) > self.limit:
                #Quand le nombre de possibilité est trop grand pour pouvoir tout montrer on garde la dernière barre
                #pour indiquer le nombre de possibilités restantes non visibles
                self.station_poss.append(Srch_station_choices(None, [], "+{0}".format(len(list_station[0]) - (self.limit - 1)), self.img_down_poss, (self.pt.x, memory_y)))
                break

            elt_chr = dico_station[elt][0]

            if len(list_station[0]) == 1:
                #Dans le cas d'une seule possibilité
                self.station_poss.append(Srch_station_choices(elt, list_station[1][ind], elt_chr, self.img_1_poss, self.img_1_poss_pt.g_tuple()))
                continue

            if ind == 0:
                #Première possiblité (dans l'ordre alphabétique)
                self.station_poss.append(Srch_station_choices(elt, list_station[1][ind], elt_chr, self.img_up_poss, self.img_up_poss_pt.g_tuple()))
                memory_y = self.img_up_poss_pt.y + self.img_up_poss.get_height()
                continue

            elif ind == (len(list_station[0]) - 1):
                #Dernière possibilité (dans l'ordre alphabétique)
                self.station_poss.append(Srch_station_choices(elt, list_station[1][ind], elt_chr, self.img_down_poss, (self.pt.x, memory_y)))
                continue

            else:
                #Autres possibilités
                self.station_poss.append(Srch_station_choices(elt, list_station[1][ind], elt_chr, self.img_mid_poss, (self.pt.x, memory_y)))
                memory_y += self.img_mid_poss.get_height()

    def blit_station_poss(self, screen):
        pt_x = self.pt.x - (self.img.get_width() / 2) + 50

        for choice in self.station_poss:
            x = choice.pt.x - (choice.img.get_width() / 2) + 5
            screen.blit(choice.img, (x, choice.pt.y))

            self.text_station = self.font.render(choice.char, True, self.txt_color)
            screen.blit(self.text_station, (pt_x, choice.pt.y + 10))

    def blit_it(self, screen):
        self.blit_img(screen)

        if hasattr(self, 'word_def'):
            screen.blit(self.word_def, self.word_def_pt.g_tuple())

        if hasattr(self, 'text'):
            screen.blit(self.text, self.text_pt.g_tuple())

    def draw_cursor(self, screen):

        if time.time() % 1 > 0.5:
            pygame.draw.line(screen, self.txt_color, self.cursor_1.g_tuple(), self.cursor_2.g_tuple(), 2)

class Srch_station_choices(object):

    def __init__(self, numero, alterego, chr, img, pt):

        self.num_station = numero
        self.alter = alterego
        self.char = chr
        self.pt = point(pt[0], pt[1])
        self.img = img
        self.set_zone()

    def set_zone(self):

        xmin = self.pt.x - (self.img.get_width() / 2)
        ymin = self.pt.y

        self.zone = pygame.Rect(xmin, ymin, self.img.get_width(), self.img.get_height())

class Mouse(object):

    def __init__(self):
        self.last_curs = 'Selection'

        self.set_into_selec()

    def control_chgt_mouse(self, dico_objet, choice_zone=None):

        self.now_text_curs = None

        for obj in dico_objet:
            if dico_objet[obj].zone.collidepoint(pygame.mouse.get_pos()) and (srch_activ == obj or srch_activ is None):
                self.now_text_curs = 'Text'

                if self.last_curs != self.now_text_curs:
                    self.set_into_text()

        if choice_zone is not None:
            for choice in choice_zone:
                if choice.zone.collidepoint(pygame.mouse.get_pos()):
                    self.now_text_curs = 'Diamond'

                    if self.last_curs != self.now_text_curs:
                        self.set_into_diamond()

        if self.now_text_curs == None:
            self.set_into_selec()

    def set_into_text(self):
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    def set_into_selec(self):
        pygame.mouse.set_cursor(*pygame.cursors.arrow)

    def set_into_diamond(self):
        pygame.mouse.set_cursor(*pygame.cursors.diamond)

class Trajets(object):

    def __init__(self, screen):

        self.bloc = []
        self.screen = screen

    def set_last_bloc(self):
        self.last_bloc = len(self.bloc) - 1

    def add_bloc(self, font, couleur):
        list_txt = []
        img = pygame.image.load("./data/Search_1_poss.png").convert_alpha(self.screen)
        font = font
        color = couleur
        larg = 4
        long = 0

        self.bloc.append([list_txt, img, font, color, [long, larg]])

        self.set_last_bloc()

    def add_text(self, str):
        id = self.last_bloc

        self.bloc[id][0].append(self.bloc[id][2].render(str, True, self.bloc[id][3]))

        self.bloc[id][4][1] += self.bloc[id][0][len(self.bloc[id][0]) - 1].get_height()
        x = self.bloc[id][0][len(self.bloc[id][0]) - 1].get_width()

        if x > self.bloc[id][4][0]:
            self.bloc[id][4][0] = x + 80

    def aff_bloc(self, bl, y):

        self.img = pygame.transform.smoothscale(bl[1], (bl[4][0], bl[4][1]))
        self.screen.blit(self.img, (((width / 2) - (bl[4][0] / 2)), y))

        for i in range(len(bl[0])):
            x = ((width / 2) - (bl[0][i].get_width() / 2))
            here_y = y + (i * bl[0][i].get_height())
            self.screen.blit(bl[0][i], (x, here_y))

        return y + bl[4][1]



def load_search_bars(couleur_def=(0, 0, 0), couleur_txt=(0, 0, 0)):
    dico_srch = {}

    dico_srch["start"] = SearchBar(((width / 2), (height / 2)), './data/Search_bar_no_bg_2.png', 'couriernew', 20, 5, zone=(440, 50))
    dico_srch["start"].set_def_word("Départ", couleur_def)
    dico_srch["start"].update_text('', couleur_txt)

    start_y = dico_srch["start"].pt.y
    start_hgt = dico_srch["start"].img.get_height() / 2
    above_start = start_y + start_hgt

    dico_srch["end"] = SearchBar(((width / 2), above_start), './data/Search_bar_no_bg_2.png', 'couriernew', 20, 4, zone=(440, 50))
    dico_srch["end"].set_def_word("Arrivée", couleur_def)
    dico_srch["end"].update_text('', couleur_txt)

    return dico_srch

def load_background(screen, couleur):
    list = []
    list.append(pygame.image.load("./data/Background.jpg").convert(screen))

    list.append(pygame.image.load("./data/Background_grid.png").convert_alpha(screen))
    list[-1] = pygame.transform.smoothscale(list[-1],((list[-1].get_width() * 1.42), (list[-1].get_height() * 1.42)))

    list.append(pygame.image.load("./data/Background_title.png").convert_alpha(screen))
    list[-1] = pygame.transform.smoothscale(list[-1],
                                              ((list[-1].get_width() * 1.42), (list[-1].get_height() * 1.42)))

    font = pygame.font.SysFont('couriernew', 17, True)
    list.append(font.render("Quitter:(Echap)", True, couleur))

    return list

def blit_background(screen, list, accueil=True):

    for elt in list:

        if list.index(elt) == (len(list) - 2):
            if accueil:
                screen.blit(elt, (0, 0))

            continue

        if list.index(elt) == (len(list) - 1):
            screen.blit(elt, (0, 20))
            continue

        screen.blit(elt, (0, 0))

def change_aff_echap(bg, txt, couleur):
    font = pygame.font.SysFont('couriernew', 17, True)

    bg[-1] = font.render(txt, True, couleur)

    return bg


def make_dic_stations(txt):
    #Crée un dictionnaire associant à chaque station toutes les autres auxquelles elle est reliée
    list_lines = txt.readlines()

    stations = {}

    for line in list_lines:
        #list_lines mets dans une liste tous les éléments de la ligne 

        #dico_stations[num_station][0] = nom de la station
        #dico_stations[num_station][1][x] -> toutes les stations directement connectées à celle-ci
        #dico_stations[num_station][2][x] -> le temps de trajet entre les deux stations 

        line = line.strip()
        if line[0: 1] == 'V':
            list_line = line.split(' ', 2)
        elif line[0: 1] == 'E':
            list_line = line.split(' ', 3)
        else:
            list_line = line

        if list_line[0] == 'V':
            #Les lignes commençant par V associent à chaque station un numéro
            #stations[0] = numéro de station unique relatif à la ligne de métro
            stations[int(list_line[1])] = [list_line[2], [], []]

        elif list_line[0] == 'E':
            #Les lignes commençant par E associent 2 stations avec un temps de trajet

            #Crée un lien dans le dictionnaire de la 1ère vers la 2ème avec son temps de trajet
            stations[int(list_line[1])][1].append(int(list_line[2]))
            stations[int(list_line[1])][2].append(int(list_line[3]))

            #Crée un lien dans le dictionnaire de la 2me vers la 1ère avec son temps de trajet
            stations[int(list_line[2])][1].append(int(list_line[1]))
            stations[int(list_line[2])][2].append(int(list_line[3]))

    return stations

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

def affiche_direction(last_station, station, dico_station, dico_line, bloc, font, couleur):
    dir = find_direction([last_station], station, dico_station, dico_line)

    text = ''

    for direction in dir:
        text += dico_station[direction][0]

        if direction != dir[-1]:
            text += ' ou '

    bloc.add_text("Direction " + text + ", jusqu'à " + dico_station[station][0])

def affiche_chemin(l_bloc, espacement=0):

    h = 0
    for bl in l_bloc.bloc:

        h = l_bloc.aff_bloc(bl, (h + espacement))


def search_station_word(answer, dico_station):
    #Recherche toutes les stations dont le nom commence par l'input dans la barre de recherche
    station_poss = [[], []]

    #station_poss[0][X] -> Station X possiblement rechercher par l'utilisateur
    #station_poss[1][X][Y] -> Station Y alterego de la station X

    for station in dico_station:

        if answer not in dico_station[station][0].lower() and answer not in dico_station[station][0].upper():
            #Si l'input n'est pas trouvé au début du nom de la station on passe à la prochaine station
            continue
        else:
            if len(station_poss[0]) == 0 or dico_station[station][0] != dico_station[station_poss[0][-1]][0]:
                #Si la liste est encore vierge ou si ce n'est pas une station déjà mise dans la liste
                station_poss[0].append(station)
                station_poss[1].append([station])
            else:
                #sinon la station a déjà été implanté dans la liste sous une ligne différente et on garde celle-ci dans une liste d'alterego
                station_poss[1][-1].append(station)

    if len(station_poss[0]) == 0:
        return None

    return station_poss

def answer_find_station(dico_station, answer_text):
    #Standardise la réponse de l'utilisateur et l'envoie 

    #Supprime les espaces avant le texte
    while answer_text != '' and answer_text[0] == ' ':
        if answer_text == ' ':
            answer_text = ''
        else:
            answer_text = answer_text[1:]

    if answer_text != '':
        station_poss = search_station_word(answer_text, dico_station)
    else:
        return []

    if station_poss is None:
        return []

    return station_poss

def show_path(dep_station, fin_station, dico_station, dico_line, screen, couleur):

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

    bloc_ligne = Trajets(screen)
    font_path = pygame.font.SysFont('couriernew', 20, True)

    for station in path[0]:

        if len(path[0]) == path[0].index(station) + 1:

            affiche_direction(last_station, station, dico_station, dico_line, bloc_ligne, font_path, couleur)

            bloc_ligne.add_bloc(font_path, couleur)
            bloc_ligne.add_text("Vous êtes arrivé à " + dico_station[station][0])
            bloc_ligne.add_text("Temps de trajet : "+ str((time // 60)) +" minutes et "+ str((time % 60)) +" secondes.")

        if actual_line != get_line(station, dico_line):
            if actual_line != None:
                before_last_station = path[0][path[0].index(last_station) - 1]
                affiche_direction(before_last_station, last_station, dico_station, dico_line, bloc_ligne, font_path, couleur)

                actual_line = get_line(station, dico_line)

                bloc_ligne.add_bloc(font_path, couleur)
                bloc_ligne.add_text("Puis prenez la ligne " + str(actual_line))

            else:
                actual_line = get_line(station, dico_line)

                bloc_ligne.add_bloc(font_path, couleur)
                bloc_ligne.add_text("Vous êtes à " + dico_station[station][0])
                bloc_ligne.add_bloc(font_path, couleur)
                bloc_ligne.add_text("Prenez la ligne " + str(actual_line))

        last_station = station

    affiche_chemin(bloc_ligne, 50)

    return True


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.environ.get("_MEIPASS2",os.path.abspath("."))

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    pygame.init()

    fenetre = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    horloge_framerate = pygame.time.Clock()

    couleur_definition_rch = (90, 94, 137)
    couleur_txt_rch = (70, 70, 70)
    search_bars = load_search_bars(couleur_definition_rch, couleur_txt_rch)

    mouse = Mouse()

    metro_txt = open(resource_path("data/metro.txt"), 'r')

    background = load_background(fenetre, (255, 255, 255))

    # Fonction qui crée un dictionnaire de stations tel que : {numéro de station : [[nom][stations liées][temps des stations liées]]
    dic_stations = make_dic_stations(metro_txt)

    # fonction qui crée un dictionnaire des lignes du type {numéro de ligne : [stations]}
    dic_lignes = make_dic_lignes(dic_stations)

    while True:
        blit_background(fenetre, background)

        list_check_zone = []
        loop_path = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()

                if srch_activ is not None:
                    if hasattr(search_bars[srch_activ], 'station_poss'):
                        for choice in search_bars[srch_activ].station_poss:
                            if choice.zone.collidepoint(click):
                                choosen_station = choice.char
                                search_bars[srch_activ].update_text(choosen_station)

                                search_bars[srch_activ].selection = choice.alter

                    if not search_bars[srch_activ].zone.collidepoint(click):
                        srch_activ = None

                else:
                    for bar in search_bars:
                        if search_bars[bar].zone.collidepoint(click):
                            search_bars[bar].selection = None
                            srch_activ = bar
                            in_srch_bar = True

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if srch_activ is not None and int(event.key) >= 20 and int(event.key) <= 122 and int(event.key) != 94:

                    if not search_bars[srch_activ].iscursoratend():
                        search_bars[srch_activ].update_text(search_bars[srch_activ].text_str + event.unicode)

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_BACKSPACE:
                    if srch_activ is not None and len(search_bars[srch_activ].text_str) > 0:
                        search_bars[srch_activ].update_text(search_bars[srch_activ].text_str[:-1])
            if event.type == pygame.VIDEORESIZE:

                pygame.display.update()
                pygame.display.flip()

        if srch_activ is not None:
            search_bars[srch_activ].set_search_stations(answer_find_station(dic_stations, search_bars[srch_activ].text_str), dic_stations)
            search_bars[srch_activ].blit_it(fenetre)
            search_bars[srch_activ].draw_cursor(fenetre)
            search_bars[srch_activ].blit_station_poss(fenetre)

            if hasattr(search_bars[srch_activ], 'station_poss'):
                list_check_zone = search_bars[srch_activ].station_poss

        else:
            if search_bars['start'].selection != None and search_bars['end'].selection != None:
                loop_path = True

            else:
                for bar in search_bars:
                    search_bars[bar].blit_it(fenetre)

        mouse.control_chgt_mouse(search_bars, list_check_zone)

        while loop_path:
            background = change_aff_echap(background, "Retour:Echap", (255, 255, 255))
            blit_background(fenetre, background, False)

            show_path(search_bars['start'].selection, search_bars['end'].selection, dic_stations, dic_lignes, fenetre, couleur_txt_rch)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        background = change_aff_echap(background, "Quitter:Echap", (255, 255, 255))
                        for bar in search_bars:
                            search_bars[bar].selection = None
                            search_bars[bar].update_text('')
                        loop_path = False

            pygame.display.flip()

            horloge_framerate.tick(framerate)

        pygame.display.flip()

        horloge_framerate.tick(framerate)