import sys
import os

PATH_TO_CONFIG = "/opt/panel/config.txt"

def getConfigLine(argument):
    fichier = open(PATH_TO_CONFIG)

    ligne=fichier.readline().rstrip()
#    print (ligne+"\n")

    while argument not in ligne :
        ligne=fichier.readline().rstrip()
#        print (ligne+"\n")

    resultat=ligne[ligne.rfind('=')+1:]
#    print (resultat)

    fichier.close()
    return resultat

if __name__ == "__main__" :
    print("Je suis là !\n")
    getConfigLine("host")
    getConfigLine("port")
