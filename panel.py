#!/usr/bin/env python3
import os
import shutil
import sys
import subprocess
import time
import datetime
import random

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sys.stdout.reconfigure(line_buffering=True)
sys.path.append("/opt/panel/modules/")
from read_config import getConfigLine

DIRECTORY_TO_WATCH = getConfigLine("directory_to_watch")
LAST_MESSAGE = getConfigLine("last_message")
BASH_PATH = getConfigLine("bash_path")

new_print = False;
alt_print = False;
message = "C:0,0,255;T:<<PRET>>";
alt_message = "C:0,0,255;T:Ou pas";
texte = " ";
alt_texte = "";
defilement = False;
positionDefilement = 0;
decalageAccent=0;
nombreDeCaracteres=8; # Constante (ici testé avec 8 chars, sur le panneau de test)
tempsAttente=10
position_x=0
position_y=0

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        global new_print
        global message
        global texte
        global defilement
        global positionDefilement
        global alt_texte
        global alt_message
        global tempsAttente
        global alt_print

        if event.is_directory:
            return None

        elif event.event_type == 'modified':
            # Take any action here when a file is first modified.
            time.sleep(1)
            datetime_object = datetime.datetime.now()
            print ("Envent : %s" % time.ctime())
            print ("Received modified event - %s." % event.src_path)
            if (os.path.exists(event.src_path)):
                new_print = True;
                # Using readlines()
                file1 = open(event.src_path, 'r')
                message = file1.readline() + "\n"
                # file1.close()
                print ("\nFile %s processed." % event.src_path)
                os.rename(event.src_path,LAST_MESSAGE)
                print ("Message : " + message)
                timestamp = datetime_object.strftime("%d/%m/%Y %H:%M:%S")
                print (timestamp)
                texte = message.rsplit(';')[4].rstrip() # On sait qu'il y a des ; donc pas besoin de le chercher avant, retirer les \n
                print ("Texte : " + texte)
#                if (len(texte)>nombreDeCaracteres or texte.find('é')!=-1):
#                    print ("Condition defilement remplie")
#                    defilement = True
#                    positionDefilement=0
#                    new_message = False # Mettre ce flag à False, pour faire tranquillement mon défilement
#                else :
#                    print("Pas de defilement")
#                    defilement = False
#                    positionDefilement=0
#                decalageAccent=0 # Dans tout les cas, mettre ce flag à "False", on le gère dans la loop
                alt_message = file1.readline() + "\n" # \n pour bien que l'interpreteur soit sur (pas forcement necessaire)
                alt_texte = alt_message.rsplit(';')[4].rstrip()
                print ("Alt_texte : " + alt_texte)
                if (alt_texte!=" " and alt_texte!="" and alt_texte!="\n" and alt_texte!="\0" and alt_texte!="T:" and alt_texte!="T: "): # ca fait bizarre en terme de couleur
                    print("Conditions du if réussi, alt_message : " + alt_message)
                    alt_print=True
                tempsAttente = int(file1.readline()) # 10 par défaut
                print("Temps attente : " + str(tempsAttente))
                file1.close()
        elif event.event_type == 'created':
            # Taken any action here when a file is created.
            print ("\nReceived created event - %s." % event.src_path)

        elif event.event_type == 'deleted':
            # Taken any action here when a file is deleted.
            print ("Received deleted event - %s." % event.src_path)

def main():
        global new_print
        global alt_print
        global message
        global alt_message
        global texte
        global alt_texte
        global defilement
        global positionDefilement
        global decalageAccent
        global nombreDeCaracteres
        global tempsAttente
        global position_x
        global position_y

        myPopen = subprocess.Popen([BASH_PATH,'--led-no-hardware-pulse','--led-gpio-mapping=adafruit-hat-pwm','-f /root/spleen/spleen-16x32.bdf','--led-brightness=100','--led-limit-refresh=60','--led-chain=2','--led-parallel=1','--led-cols=64','--led-rows=32','--led-row-addr-type=0','--led-scan-mode=0','--led-pwm-lsb-nanoseconds=200','-x 0','-y 0','-C 0,0,255'],stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding = 'utf-8',bufsize=1,universal_newlines=True)
#        myPopen = subprocess.Popen(['/opt/panel/panel.sh','--led-no-hardware-pulse','--led-gpio-mapping=adafruit-hat-pwm','-f /root/spleen/spleen-16x32.bdf','--led-brightness=100','--led-limit-refresh=120','--led-chain=2','--led-parallel=1','--led-cols=64','--led-rows=32','--led-row-addr-type=0','-x 0','-y 0','-C 0,0,255'],stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding = 'utf-8',bufsize=1,universal_newlines=True)
        print("Subprocess : ouvert\n")

#        myPopen = subprocess.Popen(['./text-example','-f','/root/slpeen/spleen-16x32.bdf','--led-gpio-mapping=adafruit-hat-pwm','--led-chain=2','--led-cols=64','--led-rows=32','--led-row-addr-type=0','--led-brightness=50','--led-slowdown-gpio=4','--led-limit-refresh=120'], stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding = 'ascii',bufsize=1,universal_newlines=True)
#        myPopen = subprocess.Popen('./simu.sh',stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding = 'ascii',bufsize=1,universal_newlines=True)


        if (os.path.exists(LAST_MESSAGE)): # Si le fichier lastmessage existe
            file1 = open(LAST_MESSAGE, 'r')
            message = file1.readline() +"\n"
            alt_message = file1.readline() +"\n" # \n pour s'assurer du bon fonctionnement
            texte = message.rsplit(';')[4].rstrip()
            alt_texte = alt_message.rsplit(';')[4].rstrip()
            print ("LAST MESSAGE FICHIER : " + message.rstrip() + " ;;; " + alt_message.rstrip())
            if (alt_texte!=" " and alt_texte!="" and alt_texte!="\n" and alt_texte!="T:" and alt_texte!="T: "): # ca fait bizarre en terme de couleur
                print("Conclusion : Plusieurs textes")
                alt_print=True
            else :
                print("Conclusion : Seulement un texte")
            new_print=True
            tempsAttente = int(file1.readline()) # 10 par défaut
            print("Temps attente : " + str(tempsAttente))
            file1.close()
#            if (len(texte)>nombreDeCaracteres or texte.find('é')!=-1): # On vérifie ce que contient le dernier message, comme au dessu lors d'un nouveau texte, potentiellement en faire une fonction pour gagner de l'espace
#                defilement = True
#                positionDefilement=0
#                new_message=False
#            else :
#                defilement=False
#                new_message=True
        else:
            message = "C:0,0,255;T:<<PRET>>\n"
            #texte = "C;0,0,255;T;<<PRET>>\n"
            new_print = True

        myobserver = Observer()
        event_handler = Handler()
        myobserver.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
        myobserver.start()

        current_texte = 1 # 1 pour texte normal, 2 pour alt_texte
#        keepBuffer="Va permettre d'eviter le clognitement lors de é"
        print("Entrée dans la boucle infinie\n")
        try:
            while True:
#                if defilement == True and new_message == False:
#                    buffer = current_message.replace(texte,"") # Va garder le début de la commande à envoyer
#                    if (texte.find('é')!=-1 and decalageAccent==0): # Si cause défilement est l'accent
#                        if (len(texte)>nombreDeCaracteres and decalageAccent==0) : #Texte long et avec un 'é', n'arrivera pas (?????)
#                            print("??????????????????????")
#                            decalageAccent=1
#                        else : # Mettre un espace devant
#                            buffer = buffer.rstrip() + str(" ") + texte + "\n"
#                            decalageAccent=0
#                    else : # Si cause défilement est 8+ char, gérer le flag de décalage en plus à cause de 'é'
#                        if (positionDefilement>=0): # Mettre des espaces à droite
#                            if (len(texte)-positionDefilement>nombreDeCaracteres-1): # Si il y a encore des chars, -1 car la coupure se fait avec un decalage
#                                buffer = buffer.rstrip()+texte[positionDefilement:positionDefilement+nombreDeCaracteres]+"\n\n" # Remettre les \n
#                            else : # Attention aux out of bounds, vide a droite
#                                buffer = buffer.rstrip()+texte[positionDefilement:len(texte)]
#                                for i in range (nombreDeCaracteres-(len(texte)-positionDefilement)):
#                                    buffer = buffer+" "
#                                buffer = buffer + "\n\n" # Remettre les \n
#                            positionDefilement+=1
#                            if (len(texte)-positionDefilement==0): #Fin
#                                positionDefilement=-nombreDeCaracteres+1 # +1 pour bien avoir au moins une lettre à l'ecran
#                        else: # Espaces à gauche
#                            espacesGauche=""
#                            for i in range(-positionDefilement):
#                                #print ("Ajout d'un espace à gauche")
#                                espacesGauche = espacesGauche+" "
#                            buffer=buffer.rstrip()+espacesGauche+texte[0:nombreDeCaracteres+positionDefilement]+"\n" # nombre+(-pos) avec le decalage, supprimer les \n de buffer et espaces
#                            positionDefilement+=1
#                    if (keepBuffer!=buffer): # Va eviter le spam, car il s'agit d'une autre chose à afficher
#                        print(datetime.date.today().strftime("%d/%m/%Y"), datetime.datetime.now().strftime("%H:%M:%S"), ": Commande envoyé : " + buffer.rstrip()) # Date, Time, Commande, Buffer sans retour à la ligne
#                        myPopen.stdin.write(buffer)
#                        keepBuffer = buffer # Va eviter le clignotement
#                    if (positionDefilement==1): # Histoire de faire une pause sur la première frame
#                        time.sleep(3*tempsAttente)
                if alt_print == False : #Si un seul texte
                    if new_print == True:
                        print (datetime.date.today().strftime("%d/%m/%Y"), datetime.datetime.now().strftime("%H:%M:%S"), " : Un seul texte à print : ")
                        #print (message)
                        print (repr(message))
                        myPopen.stdin.write(message)
                        new_print = False
                else :
                    if current_texte == 1 :
                        print(datetime.date.today().strftime("%d/%m/%Y"), datetime.datetime.now().strftime("%H:%M:%S"), " : ", repr(message))
                        #print(current_message)
                        myPopen.stdin.write(message)
                        #myPopen.stdin.write(current_message) #Deux fois histoire d'etre sur, car il y a un bug quelque part
                        current_texte=2
                    else:
                        print(datetime.date.today().strftime("%d/%m/%Y"), datetime.datetime.now().strftime("%H:%M:%S"), " : ", repr(alt_message))
                        #print(current_message.replace(texte,temp_second))
                        myPopen.stdin.write(alt_message)
                        #myPopen.stdin.write(current_message.replace(texte,temp_second)) #Deux fois histoire d'etre sur, car il y a un bug quelque part
                        current_texte=1
#                if ((defilement==True and decalageAccent==1) or new_message==True):
#                    time.sleep(tempsAttente)
#                else : # Standby
                    #print(datetime.date.today().strftime("%d/%m/%Y"), datetime.datetime.now().strftime("%H:%M:%S"), ": rien de nouveau, standby")
                    #time.sleep(tempsAttente)
#                    time.sleep(10+random.randint(-2,2))
                    #time.sleep(10*tempsAttente+random.randint(-2*tempsAttente,2*tempsAttente))
                # print("Sleep de " + str(tempsAttente))
                time.sleep(tempsAttente)
        except:
            myobserver.stop()
            print ("Erreur : ", sys.exc_info()[0])

        myobserver.join()

print("Pre Main")
main()
