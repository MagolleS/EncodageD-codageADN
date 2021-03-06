# coding: utf-8
from values import TRITS, LIST_ID, LIST_INSERT, LIST_APPEND
from string import digits, ascii_uppercase
from random import randint
import time


def encoder(tipe, valeur, fichier_save):
    """Fonction appelé lorsqu'on lance l'encodage. Elle prend en paramètre le
    type (fichier ou texte), la valeur(texte ou chemin de fichier), ainsi que
    le chemin ou sauver le fichier .dna. Elle renvoi une série de variable
    nécessaire au mode démonstration"""

    
    time1 = time.clock() #Calcule le temps au début de la fonction
    
    #Fonction qui récupere la séquence binaire du fichier/texte et la transforme en ternaire. Elle renvoie la séquence binaire et la séquence ternaire.
    s_trit1, s_bytes = byteToTrit(tipe, valeur)

    
    #Fonction qui crée S4 et renvoi S4, S2 (len_Trit et nb0) et S3.
    s_trit4, len_Trit, nb0, s_trit3 = tritToFinalTrit(s_trit1)

    
    #Fonction qui transforme une séquence ternaire en séquence de nucléotides. Renvoi une liste comportant les bases.
    s_dna = TritToDNA(s_trit4)

    
    #Fonction qui crée tout les segments et l'indexation propore à chacun d'eux. Renvoi la séquence d'ADN final, plusieurs dictionnaire comportant en clé i et en valeur différents états du segment ou de son indexation.
    s_dna_final, dicoDebut, dicoReverse, dicoI3, ID, dicoP, dicoIX, dicoIX_dna, dicoFinal = DnaToDnaFinal(s_dna)

    
    #Fonction qui enregistre la séquence d'ADN dans un fichier .dna. Elle prend en paramètre le type (tipe), la valeur (le chemin, si le type est un fichier), la séquence d'ADN, et le chemin ou sauver le fichier.
    enregistrement(tipe, valeur, s_dna_final, fichier_save)
    
    time2=time.clock() #Calcule le temps à la fin de la fonction.
    temps=time2-time1  #Stocke le temps écoulé entre le début et la fin de la fonction.
    #Toutes les variables nécessaire au mode démonstration sont renvoyé par cette fonction
    return temps, s_bytes, s_trit1, len_Trit, nb0, s_trit3, s_trit4, s_dna, dicoDebut, dicoReverse, dicoI3, ID, dicoP, dicoIX, dicoIX_dna, dicoFinal, s_dna_final
    



def convert(nombre, base = 2):
    """Fonction permettant de convertir un nombre en base 10 en une base défini.
    Elle prend en paramètre le nombre en base 10 ainsi que la base vers laquel
    le nombre doit etre converti, et qui par défaut est 2."""
    
    resultat = ''
    q = nombre // base
    r = nombre % base
    resultat = str(r) + resultat
    while q != 0:
        r = q % base
        resultat = str(r) + resultat
        q = q // base
    return resultat


def enregistrement(tipe, valeur, s_dna, fichier_save):
    """Fonction qui récupere une séquence d'adn et un emplacement de fichier et
    enregistre un fichier en .dna contenant cette séquence"""
    
    if tipe=="fichier":
        #Si le type est un fichier, on efface tout le chemin afin de ne laisser plus que le nom du fichier ainsi que son extension
        i=-1
        test=True
        while test:
            if valeur[i]=="/":
                valeur=valeur[i:]
                test=False
            i-=1
        valeur+=".dna" #On ajoute ensuite l'extension .dna
        fichier_save+="/"+valeur #enfin, on l'ajoute au chemin de sauvegarde défini auparavant.
        with open(fichier_save, "w") as ouverture:
            ouverture.write(s_dna)#On crée un fichier à l'emplacement crée auparavant et on y écrit la séquence d'ADN.
    
    else:
        #Si le type est un texte, on ajoute au chemin de sauvegarde texte_ suivi d'un nombre entre 0 et 1000 (aléatoire) puis l'extension .txt et enfin .dna.
        fichier_save+="/texte_"+str(randint(0,1000))+".txt"+".dna"
        with open(fichier_save, "x") as ouverture:
            ouverture.write(s_dna)#On crée un fichier à l'emplacement crée auparavant et on y écrit la séquence d'ADN.
        
def tritToFinalTrit(s_trit1):
    """Fonction qui prend en paramètre une liste contenant des str de 5 ou 6 caractere
    (0,1 ou 2) et la transforme de sorte qu'on puisse y connaitre sa longueur ainsi que
    la longueur totale soit un multiple de 25. Elle renvoi également S2 (len_Trit et nb0) et S3."""
    
    s_trit1 = "".join(s_trit1)
    #On crée s_trit2 qui mesure 20 trit et qui donne la longueur de s1 en ternaire
    len_Trit = convert(len(s_trit1), base=3)
    nb0 = 20 - len(convert(len(s_trit1), base=3))
    s_trit2 = nb0*"0" + len_Trit
    #On crée s_trit3 en fonction de s_trit1 et s_trit2 pour que ces 3 derniers ait comme longueur un multiple de 25
    len_trit_1_2 = len(s_trit1) + 20
    s_trit3 = 0
    while (len_trit_1_2 + s_trit3)%25 != 0:
        s_trit3+=1
    s_trit3 = s_trit3*"0"
    #On crée S4 : S1 + S3 + S2
    s_trit4 = str(s_trit1) + s_trit3 + s_trit2
    return s_trit4, len_Trit, nb0*"0", s_trit3
    




def TritToDNA(s_trit, pre_nt = "A"):
    """Fonction qui transforme une séquence ternaire en séquence ADN.
    Elle prend en fonction la séquence de trit et, en paramtre faculatif,
    le nucléotide précedent, par défaut A, et renvoi une liste de nucléotides."""
    
    
    s_t = list(map(int, str(s_trit)))  # Liste qui contient la séquence en trinaire
    s_dna = []  # Liste qui va acceuillir les nucléotides transformés
    for trit in s_t:
        if s_dna == []:
            pre_trit = pre_nt
        else:
            pre_trit = s_dna[-1]
            
        if pre_trit == "A":
            if trit == 0:
                s_dna.append("C")
            elif trit == 1:
                s_dna.append("G")
            elif trit == 2:
                s_dna.append("T")
        elif pre_trit == "C":
            if trit == 0:
                s_dna.append("G")
            elif trit == 1:
                s_dna.append("T")
            elif trit == 2:
                s_dna.append("A")
        elif pre_trit == "G":
            if trit == 0:
                s_dna.append("T")
            elif trit == 1:
                s_dna.append("A")
            elif trit == 2:
                s_dna.append("C")
        elif pre_trit == "T":
            if trit == 0:
                s_dna.append("A")
            elif trit == 1:
                s_dna.append("C")
            elif trit == 2:
                s_dna.append("G")

    return s_dna


def DnaToDnaFinal(s_dna):
    
    """"Fonction qui crée les segments de longueur 117. Elle prend en paramètre une séquence
    d'ADN et renvoi une autre séquence d'ADN"""
    
    ID = LIST_ID[randint(0,8)]#On determine ID qui reste le même pour toute la séquence donné en paramètre.
    #Création de dictionnaires qui vont contenir des infomations nécessaires au mode démonstration.
    dicoDebut = {}
    dicoReverse = {}
    dicoI3 = {}
    dicoP = {}
    dicoIX = {}
    dicoIX_dna = {}
    dicoFinal = {}
    
    maxNt = 100
    minNt = 0
    i=0
    segment = []
    s_dna_final = ""
    while i != (len(s_dna)/25)-3:
        #Boucle qui traite chaque segment séparement
        #On crée le segment de longueur 100. 
        if minNt == 0:
            segment=s_dna[:maxNt]        
        else:
            segment=s_dna[minNt:maxNt] 
        dicoDebut[i]="".join(segment)

        #Si i est impair, on inverse et complémente le segment
        if not i%2==0:
            segment = reverseDna(segment)
        dicoReverse[i] = "".join(segment)


        #On crée i3 de longueur 12
        i_trit = str(convert(i, base=3))
        i3 = (12 - len(i_trit))*"0" + i_trit
        dicoI3[i]=i3


        #On calcule P, d'abord "normalement" puis, tant que P est différent de 0, 1 ou 2, on retranche 3 si il est superieur a 2 ou ajoute 3 si il est inferieur à 0
        P = int(ID[0]) + int(i3[0]) + int(i3[2]) + int(i3[4]) + int(i3[6]) + int(i3[8]) + int(i3[10])
        
        while P != 0 or P != 1 or P != 2:
            if P <0:
                P+=3
            elif P>2:
                P-=3
            else:
                break
        dicoP[i]=P
        #On crée IX : ID + i3 + P. On le converti ensuite en ADN en précisant le nucléotide précedent avec le dernier nucléotide du segment
        IX = str(ID) + str(i3) + str(P)
        dicoIX[i] = IX
        IX_dna = TritToDNA(IX, pre_nt=segment[-1])
        dicoIX_dna[i] = IX_dna
        
        segment.extend(IX_dna)#On ajoute IX au segment.


        #On ajoute un nucléotide au début et un à la fin du segment, aléatoirement si possible mais en prenant en compte les nucléotides suivant ou précedent.
        if segment[0] == "A":
            segment.insert(0, "T")
        elif segment[0] == "T":
            segment.insert(0, "A")
        else:
            segment.insert(0, LIST_INSERT[randint(0,1)])

        if segment[-1]=="C":
            segment.append("G")
        elif segment[-1]=="G":
            segment.append("C")
        else:
            segment.append(LIST_APPEND[randint(0,1)])
        s_dna_final += "".join(segment)#On ajoute le segment à la séquence d'ADN final.
        dicoFinal[i]=segment
        
        i+=1
        maxNt+=25
        minNt+=25


        
        #Test si le segment a la bonne longueur
        if len(segment)!=117:
            print("Pas la bonne longueur")
        if len(segment)<117:
            print("Plus petit ")
        elif len(segment)>117:
            print("plus grand")
    return s_dna_final, dicoDebut, dicoReverse, dicoI3, ID, dicoP, dicoIX, dicoIX_dna, dicoFinal #On renvoi la séquence d'ADN final ainsi que des variables nécessaires au mode décodage.
        
           
        
def reverseDna(s_dna):
    """Fonction qui inverse une séquence d'ADN puis change chaque nucléotides
    par le nucléotide complémentaire. Elle prend en paramètre une séquence d'ADN et renvoi une autre séquence d'ADN"""
    
    if type(s_dna)!=list:
        s_dna = list(map(str, str(s_dna)))
        #Si c'est une chaine de caractere qui est recu en parametre, on la
        #transforme en liste
    a = "A"
    c = "C"
    g = "G"
    t = "T"
    s_dna_r = []#Liste qui va accueillir le nouvelle séquence d'adn
    for nt in s_dna:
        if nt == a:
            s_dna_r.append(t)
        elif nt == t:
            s_dna_r.append(a)
        elif nt == g:
            s_dna_r.append(c)
        elif nt == c:
            s_dna_r.append(g)

    s_dna_r.reverse()#On inverse la liste
    return s_dna_r
            
    
    
            
def byteToTrit(tipe, valeur):
    """Fonction qui prend en parametre un emplacement de fichier sous forme de
    string(str), va récuperer sous forme de d'un bytes la séquence binaire du
    fichier, puis le transformer en une séquence de trit. Cette séquence est s_trit
    et est represente en une liste contenant des str de 5 ou 6 caractere (0,1 ou 2)
    """
    
    if tipe=="fichier":
        with open(valeur, "rb") as ouverture:
            octets = ouverture.read()
    else:
        octets=valeur.encode()
    #Le fichier est ouvert et la séquence binaire est dans le bytes octets
        
    s_trit = []
    #Pour chaque octets, la valeur correspond à 5 ou 6 trits qu'on ajoute à s_trit
    for oct in octets:
        s_trit.append(TRITS[oct])
    #On retourne la liste
    return s_trit, octets

    

def afficherEncodage(texte, temps, s_bytes, s_trit1, len_Trit, nb0, s_trit3, s_trit4, s_dna, dicoDebut, dicoReverse, dicoI3, ID, dicoP, dicoIX, dicoIX_dna, dicoFinal, s_dna_final):
    """Fonction qui prend en paramètre ce que retourne la fonction encode.
    Il retourne un string contenant un affichage lisible des etapes de
    l'encodage. """

    s = ""
    for index, trit in enumerate(s_trit1):
        octet = convert(s_bytes[index], 2)
        s += "{}  {}  {} \n\n".format(texte[index], int(8-len(octet))*"0"+str(octet), trit)
    s += "".join(s_trit1)
    s += "{} convertit en base 3 -> {}\n".format(int(len_Trit, 3), len_Trit)
    s += "La longueur du nombre est de {}, on rajoute donc 20-{} = {} :\n {} {}\n".format(len(len_Trit),len(len_Trit),len(nb0), nb0, len_Trit)
    s += "La longueur des deux séquences est de {}. Le plus proche multiple de 25 est {} on rajoute donc {} 0 : \n {}\n".format(
        str(int(len_Trit, 3)+20), str(len(s_trit4)), str(len(s_trit3)), str(s_trit3))
    s += "Cela nous donne : \n {} {} {} de longueur {}\n".format("".join(s_trit1), str(s_trit3), nb0+len_Trit, len(s_trit4))
    s += "On converti le tout en ADN : \n {}\n".format("".join(s_dna))


    s += "N est égal à {longueur}. Il y aura donc ({longueur}/25)-3 = {truc} segment.\n".format(longueur=len("".join(s_dna)), truc=int((len("".join(s_dna))/25)-3))
    ecart=""
    for cle, valeur in dicoDebut.items():
        
        s += "Segment {} : {}{} {} {} {}\n".format(cle, ecart, "".join(valeur[:25]), "".join(valeur[25:50]), "".join(valeur[50:75]), "".join(valeur[75:100]))
        ecart+= " " +" "*25
        

    s += "Pour chaque segment, on regarde si i est impair : \n"
    s += str(len(dicoI3)) + str( len(dicoReverse)) + "\n"
    for cle, valeur in dicoReverse.items():
        s += "Segment {}\n".format(cle)
        if cle%2==0:
            s += "i = {}, et est donc pair, on laisse le segment comme il est : \n {}\n".format(cle, "".join(valeur))
        else:
            s += "i = {}, et est impair, on inverse puis complemente donc le segment : \n {}\n".format(cle, "".join(valeur))

    s += "\n\n On défini ensuite i3 : \n\n"
    for i, i3 in dicoI3.items():
        s += "Segment {} :  \n".format(i)
        s += "On converti i = {} en base 3 : {} puis on le fait préceder d'assez de 0 pour que sa longueur soit 12 : {}\n\n".format(i, convert(i, 3), i3)

    s += "\n\nOn va ensuite calculer P à partir de ID et i3 :\n\n"
    for i, i3 in dicoI3.items():
        s += "Segment {} :   ID : {}, i3 : {}\n".format(i, ID, i3)
        s += "P est égal à {} + {} + {} + {} + {} + {} + {} modulo 3 = {} \n\n".format(ID[0] , i3[0] ,i3[2], i3[4],i3[6], i3[8], i3[10], dicoP[i])

    s += "\n Et enfin, on forme IX : \n"
    for i, IX in dicoIX_dna.items():
        s += "IX = {} {} {}. Transforme en ADN en prenant en compte le dernier nucléotide du segment, IX nous donne : {} de longueur 15 \n\n".format(ID, dicoI3[i], dicoP[i], "".join(IX))

    s += "On ajoute cela au segment : \n\n"
    for i, segment in dicoReverse.items():
        s += "Segment {} : \n {} {}\n\n".format(i, segment, "".join(dicoIX_dna[i]))

    s += "On ajoute deux nucléotides aux extremités ce qui forme un segment de 117 nt : \n\n"
    for i, segment in dicoFinal.items():
        s += "Segment {} :  {} {} {}\n \n".format(i, segment[0], "".join(segment[1:-1]), segment[-1])
    return s


