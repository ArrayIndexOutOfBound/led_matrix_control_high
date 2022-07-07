#!/usr/bin/env python3
import os
import shutil
import sys
import subprocess
import time
import datetime
import random
import RPi.GPIO as GPIO

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
tempsAttente = getConfigLine("temps_attente")
position_x=0
position_y=0

def main():
        global nombreDeCaracteres
        global tempsAttente
        global position_x
        global position_y

        myPopen = subprocess.Popen([BASH_PATH,'--led-no-hardware-pulse','--led-gpio-mapping=adafruit-hat-pwm','-f /root/spleen/spleen-16x32.bdf','--led-brightness=70','--led-limit-refresh=60','--led-chain=2','--led-parallel=1','--led-cols=64','--led-rows=32','--led-row-addr-type=0','--led-scan-mode=0','--led-pwm-lsb-nanoseconds=130','--led-slowdown-gpio=2','-x 0','-y 0','-C 0,0,255'],stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding = 'utf-8',bufsize=1,universal_newlines=True)
        print("Subprocess : ouvert\n")

        print("Initialisation des GPIO")
        PIN_1 = 19
        PIN_2 = 25
        GPIO.setmode(GPIO.BCM)
        # Si on décommente ça, la valeur de base sera 1, il faut retirer le courant
        GPIO.setup(PIN_1, GPIO.IN)
        GPIO.setup(PIN_2, GPIO.IN)
        # Si on décommente ça, la valeur de base sera 0, il faut ajouter du courant
        #GPIO.setup(PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #GPIO.setup(PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        time.sleep(1)

        print("Entrée dans la boucle infinie\n")
        try:
            while True: # 1 = HIGH, 0 = LOW, HIGH = base, LOW = activé
                #print("Lecture GPIO")
                etat_19 = GPIO.input(PIN_1)
                etat_25 = GPIO.input(PIN_2)

                #print("19="+str(etat_19))
                #print("25="+str(etat_25))

                #print("Les IFS")
                if etat_19==1 and etat_25==1:
                    #print("1-1")
                    myPopen.stdin.write("C:255,0,0;B:0,0,0;X:0;Y:0;T:Rien\n\n")
                if etat_19==1 and etat_25==0:
                    #print("1-0")
                    myPopen.stdin.write("C:255,0,0;B:0,0,0;X:0;Y:0;T:Pin25\n\n")
                if etat_19==0 and etat_25==1:
                    #print("0-1")
                    myPopen.stdin.write("C:255,0,0;B:0,0,0;X:0;Y:0;T:Pin19\n\n")
                if etat_19==0 and etat_25==0:
                    #print("0-0")
                    myPopen.stdin.write("C:255,0,0;B:0,0,0;X:0;Y:0;T:Pin19&25\n\n")

                #print("10sec attente")
                time.sleep(int(tempsAttente))
        except:
            print ("Erreur : ", sys.exc_info()[0])
            #GPIO.cleanup()

print("Pre Main")
main()
#GPIO.cleanup()
