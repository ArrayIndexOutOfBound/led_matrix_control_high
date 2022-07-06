from flask import Flask
from flask import render_template,redirect,url_for,request
import sys

sys.stdout.reconfigure(line_buffering=True)
sys.path.append("/opt/panel/modules/")
from read_config import getConfigLine

COMMAND_PATH = getConfigLine("command_path")
HOST = getConfigLine("host")
PORT = getConfigLine("port")
DEBUG=False

app = Flask(__name__)

couleur="#ffffff"
couleur_fond="#000000"
texte="Remplir ici"
posX="0"
posY="0"

temps="10"

alt_texte=""
alt_posX="0"
alt_posY="0"
alt_couleur="#ffffff"
alt_couleur_fond="#000000"

@app.route("/", methods=['GET', 'POST'])
def index():
    global couleur
    global texte
    global posX
    global posY
    global temps
    global alt_texte
    global alt_posX
    global alt_posY
    global alt_couleur
    global alt_couleur_fond

    return render_template('index.html',couleur=couleur, texte=texte, posX=posX, posY=posY, temps=temps, alt_texte=alt_texte, alt_posX=alt_posX, alt_posY=alt_posY, alt_couleur=alt_couleur, alt_couleur_fond=alt_couleur_fond)

@app.route("/set" , methods=['GET', 'POST'])
def set():
    global texte
    global posX
    global posY
    global couleur
    global couleur_fond

    global temps

    global alt_texte
    global alt_posX
    global alt_posY
    global alt_couleur
    global alt_couleur_fond

    texte=request.form.get("texte")
    couleur=request.form.get("couleur")
    posX=request.form.get("posX")
    posY=request.form.get("posY")
    couleur_fond=request.form.get("couleur_fond")

    temps=request.form.get("temps")

    alt_posX=request.form.get("alt_posX")
    alt_posY=request.form.get("alt_posY")
    alt_texte=request.form.get("alt_texte")
    alt_couleur=request.form.get("alt_couleur")
    alt_couleur_fond=request.form.get("alt_couleur_fond")

    print(f'ETAPE 1 : Texte:{texte} \n Couleur:{couleur} \n PosX:{posX} \n PosY:{posY} \n Fond:{couleur_fond} \n Alt_Texte:{alt_texte} \n Alt_Couleur:{alt_couleur} \n Alt_Fond:{alt_couleur_fond} \n Alt_posX:{alt_posX} \n Alt_posY:{alt_posY} \n Temps:{temps}')

    if (posX=="None" or posX=="" or posX is None):
        posX="0"
    if (posY=="None" or posY=="" or posY is None):
        posY="0"
    if (couleur=="None" or couleur=="" or couleur is None):
        couleur="#ffffff" # RGB, blanc
    if (couleur_fond=="None" or couleur_fond=="" or couleur_fond is None):
        couleur_fond="#000000" # RGB, noir

    if (temps=="None" or temps=="" or temps is None):
        temps="10"


    if (alt_texte=="None" or alt_texte=="" or alt_texte is None):
        alt_texte=""
    if (alt_posX=="None" or alt_posX=="" or alt_posX is None):
        alt_posX="0"
    if (alt_posY=="None" or alt_posY=="" or alt_posY is None):
        alt_posY="0"
    if (alt_couleur=="None" or alt_couleur=="" or alt_couleur is None):
        alt_couleur=couleur # repliquer la couleur
    if (alt_couleur_fond=="None" or alt_couleur_fond=="" or alt_couleur_fond is None):
        alt_couleur_fond=couleur_fond # repliquer le fond


    print(f'ETAPE 2 : Texte:{texte} \n Couleur:{couleur} \n PosX:{posX} \n PosY:{posY} \n Fond:{couleur_fond} \n Alt_Texte:{alt_texte} \n Alt_Couleur:{alt_couleur} \n Alt_Fond:{alt_couleur_fond} \n Alt_posX:{alt_posX} \n Alt_posY:{alt_posY} \n Temps:{temps}')

    c=hex_to_rgb(couleur)
    b=hex_to_rgb(couleur_fond)

    alt_c=hex_to_rgb(alt_couleur)
    alt_b=hex_to_rgb(alt_couleur_fond)

    f = open(COMMAND_PATH, "w")
    f.write(f"C:{c[0]},{c[1]},{c[2]};B:{b[0]},{b[1]},{b[2]};X:{posX};Y:{posY};T:{texte}\nC:{alt_c[0]},{alt_c[1]},{alt_c[2]};B:{alt_b[0]},{alt_b[1]},{alt_b[2]};X:{alt_posX};Y:{alt_posY};T:{alt_texte}\n{temps}\n")
    f.flush()
    f.close()
    return render_template('set.html',couleur=couleur, texte=texte, posX=posX, posY=posY, couleur_fond=couleur_fond, alt_texte=alt_texte, alt_couleur=alt_couleur, alt_posX=alt_posX, alt_posY=alt_posY, alt_couleur_fond=alt_couleur_fond, temps=temps)
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

if __name__=="__main__" :
    app.run(host=HOST,port=PORT,debug=DEBUG)
