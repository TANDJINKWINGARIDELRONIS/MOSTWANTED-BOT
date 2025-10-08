import os
import time
from random import *
from google import genai
import tempfile
import datetime
import json
import subprocess
import requests
from telegram import Update
from googleapiclient.discovery import build
from google.genai import types 
from telegram.ext import ApplicationBuilder,CommandHandler,MessageHandler,filters,ContextTypes
BOT_TOKEN = "8319035036:AAG2C3YbDUa4cZgSkcAb_KnF51dzueW0Ru0"
API_KEY="e110de4530ce8923798c6668613b92f3"
OPENIA_KEY="AIzaSyBBJbrPdw2fwfsmGu6sV-yFAdeZQBJDUvc"
KEY_TIME = "9UJS6LPXID3A"
youtube_api = "AIzaSyBx-Dr2ttZjd2UQNsVnjC1Xel6ZlpHNNx8"
youtube = build("youtube","v3",developerKey=youtube_api)

MUSIC = "music_MW"
USERS_FILE = "users1.json"
users1 = {}


if os.path.exists(USERS_FILE):
    with open(USERS_FILE,"r") as f:
        try:
            users1 = json.load(f)
        except:
            users1 = {}

# Fonction start
async def start(update,context):
    users1
    user = update.message.from_user
    users1[str(user.id)] = {
        "first" : user.first_name,
        "last" : user.last_name,
        "full" : f"{user.first_name} {user.last_name}",
        "username" : user.username
    }
    with open(USERS_FILE, "w") as f:
        json.dump(users1,f,indent = 4)
    await update.message.reply_text(f"Ghost 🤖 : Salut {user.first_name} ! Tu es enregistré ✅\n Tape /help pour voir ce dont je suis capable 😎")
    
# Fonction help
async def help_command(update,context):
    user= update.message.from_user
    await update.message.reply_text(
        f"Ghost 🤖 : salut 👋🏻 {user.first_name} \n"
        "╭─≼ 👨🏻‍💻 MOSTWANTED BOT 🤖 ≽─╮\n"
        "│\n"
        "│ 1- /start   = Démarre le bot 🤖\n"
        "│ 2- /aide    = Afficher les commandes disponibles 📜\n"
        "│ 3- /infos   = Donne des infos sur le bot ℹ️\n"
        "│ 4- /test    = Vérifie dans tes groupes si je suis en ligne 📡\n"
        "│\n"
        "├─≼ 🔧 SECTION UTILITAIRE ≽─┤\n"
        "│\n"
        "│ 1- /hour      = Donne l'heure actuelle 🕒\n"
        "│ 2- /getmeteo  = Donne la météo d'une ville ⛅\n"
        "│ 3- /generate  = Génère des phrases ✍️\n"
        "│ 4- /sendto    = Envoyer un message à un utilisateur 📩\n"
        "│ 5- /question  = Poser une question au bot 🤖\n"
        "│ 6- /showusers = Consulter les utilisateurs enregistrés 📂\n"
        "│\n"
        "├─≼ 📚 SECTION DE TRAVAIL ≽─┤\n"
        "│\n"
        "│ 1- /addition   = Effectuer une addition ➕\n"
        "│ 2- /soustraction  = Effectuer une soustraction ➖\n"
        "│ 3- /multiplication  = Effectuer une multiplication ✖️\n"
        "│ 4- /division    = Effectuer une division ➗\n"
        "│ 5- /exp    = Calculer a^b 🔼\n"
        "│ 6- /modulo   = Reste de la division (a mod b) 🧮\n"
        "│ 7- /audio  = Jouer une musique 🎵\n"
        "│ 8- /movie  = Rechercher une vidéo 📹\n"
        "│ 9- /clean  = Nettoyer message \n"
        "├─≼ SECTION FUN ≽─┤\n"
        "| 1- /de = lancer le dé 🎲️"
        "│\n"
        "╰─≼ 🚀 POWERED BY MOSTWANTED ≽─╯"
    )

# Fonction time
async def local_time(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)    
    data = response.json()
    latitude = data["coord"]["lat"]
    longitude = data["coord"]["lon"]
    
    # Apres avoir obtenu la latitude et la longitude de la ville on va demande une requete API
    url1 = f"http://api.timezonedb.com/v2.1/get-time-zone?key={KEY_TIME}&format=json&by=position&lat={latitude}&lng={longitude}"
    reponse = requests.get(url1)
    data1 = reponse.json()
    
    if latitude is None or longitude is None:
        return "❌ Ville Introuvable"
    print("Heure locale affichee avec succès !")
    return data1["formatted"]

async def time_command(update,context):
   if not context.args:
       await update.message.reply_text("Ghost 🤖 : Utilisation : /hour <Nom de la ville>")
       return
   ville = " ".join(context.args)
   await update.message.reply_text(await local_time(ville))

# Fonction infos
async def bot_infos(update,context):
    await update.message.reply_text(
        "Ghost 🤖 : \n"
        "🤓️BOT NAME : GHOST \n"
        "✨VERSION  : 3.5 \n"
        "🥇️LANGUAGE : PYTHON \n"
        "👩‍💻️DEVELOPPEUR : MOSTWANTED 😎 \n"
        "©️LIEN DU BOT : t.me/MostwantedX_bot\n"
        "📱contact de MOSTWANTED :\n"
        "💻WhatsApp=655-56-26-34\n"
        "🖥️Facebook lite=RIDEL TANDJI \n"
    )

async def met(city) :
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=fr"
    reponse = requests.get(url)
    if reponse.status_code == 200:
        data = reponse.json()
        infos_meteo={
            "Nom":data["name"],
            "Temperature" : data["main"]["temp"],
            "Humidite": data["main"]["humidity"],
            "Description":data["weather"][0]["description"],
            "Date" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open("meteo.json","a",encoding="utf-8") as file :
            file.write(json.dumps(infos_meteo) + "\n") 
            print(f"Les données sur la ville ont bien été conservé ✅")
            return f"Ville : {infos_meteo['Nom']}\nTemperature : {infos_meteo['Temperature']}\nHumidité :{infos_meteo['Humidite']}\nDescription : {infos_meteo['Description']}\n"
    else:
        return f"Erreur ! Impossible de charger les informations sur {city}"

async def meteo(update,context) :
    if not context.args :
        await update.message.reply_text("Ghost 🤖 : Utilisation correcte /getmeteo <nom ville>")
        return 
    ville=" ".join(context.args)      
    await update.message.reply_text(await met(ville))

async def gen_phrase(update, context):
    if not context.args:
        await update.message.reply_text("Ghost 🤖 : Usage : /gen_phrase mot1 mot2 mot3 ...")
        return
    
    mots = context.args[:]   
    shuffle(mots)
    phrase = ' '.join(mots).capitalize() + '.'
    
    await update.message.reply_text("Ghost 🤖 : Voici une phrase :")
    await update.message.reply_text(phrase)

async def sendto(update, context):
    # Vérifier qu'il y a bien un nom et un message
    if len(context.args) < 2:
        await update.message.reply_text("Ghost 🤖 : Utilisation: /sendto <nom_utilisateur> <message>")
        return

    destinataire_nom = context.args[0]
    message = " ".join(context.args[1:])
    found = False
    sender = update.message.from_user.first_name
    for id,info in users1.items():
        username = (info.get("username") or "").lower()
        first = (info.get("first") or "").lower()
        last = (info.get("last") or "").lower()
        full = (info.get("full") or "").lower()
       
        if destinataire_nom.lower() in [username,first,last,full] :  
            destinataire_id = int(id)
            context.bot.send_message(chat_id=destinataire_id, text=f"Message de {sender}: \n{message}")
            found = True
            break
    if found :
        await update.message.reply_text("Ghost 🤖 : Message envoyé ✅")
    else :
        await update.message.reply_text("Ghost 🤖 : ❌ Erreur")

async def listusers(update, context):
    if not users1:
        await update.message.reply_text("Ghost 🤖 : ❌ Aucun utilisateur enregistré.")
        return
    sender = update.message.from_user.first_name
    print(f"Le client {sender} a consulter les utilisateurs enregistres !  ")
    
    message = "Ghost 🤖 : 📋 Utilisateurs enregistrés :\n\n"
    for uid, info in users1.items():
        first_name = info.get("first", "")
        last_name = info.get("last", "")
        full_name = info.get("full") or f"{first_name} {last_name}".strip()
        username = info.get("username")
        uname = f"@{username}" if username else "❌ (pas de username)"
        
        message += f"👤 {full_name} | ID: {uid} | Username: {uname}\n\n"
    await update.message.reply_text(message)
#fonction addition   
 
async def add(update,context) :
    try :
        nbre1 = float(context.args[0])
        nbre2 = float(context.args[1])
        await update.message.reply_text(f"Ghost 🤖 : ✨Résultat : {nbre1} + {nbre2} = {nbre1+nbre2 } ")
    except   :
        await update.message.reply_text("Ghost 🤖 : ❌Usage correct : /addition <nombre1> <nombre2>")

#fonction soustraction   
     
async def sous(update,context) :   
    try :
        nbre1 = float(context.args[0])
        nbre2 = float(context.args[1])
        await update.message.reply_text(f"Ghost 🤖 : ✨Résultat : {nbre1} - {nbre2} = {nbre1-nbre2 } ")
    except  :
        await update.message.reply_text("Ghost 🤖 : ❌Usage correct : /soustraction <nombre1> <nombre2>")
        
#fonction multiplication 
async def multi(update,context) :
    try :
        nbre1 = float(context.args[0])
        nbre2 = float(context.args[1])
        await update.message.reply_text(f"Ghost 🤖 : ✨Résultat : {nbre1} x {nbre2} = {nbre1*nbre2 } ")
    except  :
        await update.message.reply_text("Ghost 🤖 : ❌Usage correct : /multiplication <nombre1> <nombre2>")
              
#fonctuon division 
async def div (update,context)  :
    try :
        nbre1 = float(context.args[0])
        nbre2 = float(context.args[1])
        if nbre2==0 :
            await update.message.reply_text("Ghost 🤖 : Impossible d'effectuer les divisions par zéro (0)")
        else :    
            await update.message.reply_text(f"Ghost 🤖 : ✨Résultat : {nbre1} ÷ {nbre2} = {nbre1/nbre2 } ")
    except  :
        await update.message.reply_text("Ghost 🤖 : ❌Usage correct : /division <nombre1> <nombre2>")

#fonction puissance 
async def exp(update,context) :
    try :
        nbre1 = float(context.args[0])
        nbre2 = float(context.args[1])
        if nbre2==0 :
            await update.message.reply_text(f"Ghost 🤖 : Résultat : {nbre1}^0 = 1"
            "📝PETITE REMARQUE : Tout nombre exposant zéro égale 1" )
        else :  
            await update.message.reply_text(f"Ghost 🤖 : ✨Résultat : {nbre1}^{nbre2} = {nbre1**nbre2}")
    except :
        await update.message.reply_text("Ghost 🤖 : ❌Usage correct : /exp <nombre1> <nombre2>")
        
#fonction modulo
async def mod(update,context) :
    try :
        nbre1 = float(context.args[0])
        nbre2 = float(context.args[1])
        if nbre2==0 :
            await update.message.reply_text("Ghost 🤖 : Impossible d'effectuer le modulo zéro")
        else :
            await update.message.reply_text(f"Ghost 🤖 : Résultat : {nbre1}mod{nbre2} = {nbre1%nbre2}")
    except :
        await update.message.reply_text("Ghost 🤖 : ❌Usage correct : /modulo <nombre1> <nombre2>")


#fonction pour questionner le bot 
async def ask(update,context) :
    question = " ".join(context.args)
    sender = update.message.from_user.first_name
    print(f"Le client {sender} a poser cette question au bot : {question}")
    if not question:
        await update.message.reply_text("❌ Utilisation : /question <ta question>")
        return

    try:
        client = genai.Client(api_key="AIzaSyBBJbrPdw2fwfsmGu6sV-yFAdeZQBJDUvc")

        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=question
        )

        answer = response.text
        for i in range(0,len(answer),2000) :
            await update.message.reply_text("Ghost IA🤖 \n ")
            await update.message.reply_text("💡 Réponse : "+answer[i:i+4096])
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ghost IA : {e}")
        
async def play(update, context):
    if not context.args:
        await update.message.reply_text("Ghost 🤖 : ✨Usage correct : /audio <titre de la musique>")
        return
    
    music_query = " ".join(context.args)
    user = update.message.from_user
    try:
            with tempfile.TemporaryDirectory() as MUSIC : 
                output_path = os.path.join(MUSIC, "%(title).50s.%(ext)s")
        
                subprocess.run([
                    "yt-dlp",
                    "--extract-audio",
                    "--audio-format", "mp3",
                    "--audio-quality", "192k",
                    "-o", output_path,
                    f"ytsearch:{music_query}"
                ], check=True)
                
                files = os.listdir(MUSIC)
                mp3_files = [f for f in files if f.endswith(".mp3")]
                mp3_files.sort(key=lambda f: os.path.getctime(os.path.join(MUSIC, f)))
                latest_file = os.path.join(MUSIC, mp3_files[-1])
                
                with open(latest_file, "rb") as audio:
                    await update.message.reply_text(f"Ghost 🤖 : {music_query} trouvé [x]")
                    await update.message.reply_audio(audio)
    except Exception as e:
        await update.message.reply_text(f"Ghost 🤖 : ❌Erreur impossible de télécharger: {str(e)}")        

# Recherche Video
    
async def search_video(name):
   requests = youtube.search().list(q = name,part="snippet",type="video",maxResults=1)
   # Ici on veut trouver l'ID d'une video via son nom
   response = requests.execute()
   # Ici on envoie une requete et on obtient une reponse
   
   if response["items"]:
       video = response["items"][0]["id"]["videoId"]
       # Ca recupere l'id de la video
       title = response["items"][0]["snippet"]["title"]
       stats = youtube.videos().list(part="statistics",id=video)
       stats_res = stats.execute()
       stats = stats_res["items"][0]["statistics"]
       like_count = stats.get("likeCount", "N/A")
       vues = stats.get("viewCount", "N/A")
       
       # recherche playlist
       req_playlist = youtube.search().list(q=name, part="snippet", type="playlist", maxResults=1)
       res_playlist = req_playlist.execute()
       playlist_id, playlist_title = (None, None)
       if res_playlist["items"]:
            playlist_id = res_playlist["items"][0]["id"]["playlistId"]
            playlist_title = res_playlist["items"][0]["snippet"]["title"]
       return (video,title,like_count,vues),(playlist_id,playlist_title)
   return None,None,None,None


# Pour recuperer le nombre de video d'une playlist
async def info_playlist(playlist_id):
    request = youtube.playlistItems().list(part="snippet",playlistId=playlist_id,maxResults=50)
    
    response = request.execute()
    total_videos = response.get("pageInfo",{}).get("totalResults",0)
    return total_videos

# Code Pour Les Commentaires
async def commentaries(video_id,max_results=10):
    comments = []
    requests = youtube.commentThreads().list(part = "snippet",videoId=video_id,textFormat="plainText",maxResults=max_results)
    # On a construit la requete pour recuperer les commentaires
    response = requests.execute()
    # Lancement de la requete
    for commentary in response["items"]:
        pet = commentary["snippet"]["topLevelComment"]["snippet"]
        #Ca va chercher le vrai commentaire
        text = pet["textDisplay"]
        #Recupere le texte du commentaire
        like = pet["likeCount"]
        comments.append((text,like))
    return comments



# Code Pour Analyser une Playlist
async def analyse_playlist(playlist_id,playlist_title):
    videos = []
    req = youtube.playlistItems().list(part="snippet",playlistId=playlist_id,maxResults=20)
    res = req.execute()

    for item in res.get("items", []):
        title = item["snippet"]["title"]
        videos.append(title)

    if not videos:
        return "Impossible d’analyser : la playlist est vide."

    input_text = "\n".join([f"- {t}" for t in videos])

    prompt = f"""Voici les titres des vidéos de la playlist "{playlist_title}" :
    {input_text}
    Analyse cette playlist et réponds :
    1. Résume en quelques phrases ce que couvre cette playlist.
    2. Pour quel type de spectateurs est-elle adaptée ?
    3. Donne une note de pertinence /10.
    4. Dis si tu la recommanderais, et pourquoi.
    """

    client = genai.Client(api_key="AIzaSyBBJbrPdw2fwfsmGu6sV-yFAdeZQBJDUvc")
    model = "gemini-2.5-flash"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
    ]

    config = types.GenerateContentConfig(response_modalities=["TEXT"])

    output = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        if getattr(chunk, "text", None):
            output += chunk.text

    return output.strip()

# Code Recuperer Dans Google AI studio
def analyse_comments(comments):
    client = genai.Client(api_key=("AIzaSyAQBpi-rDqpY4rqSZbeFc0Szjg0dsCYixQ"))
    # Ici on prend les commentaires les plus likes
    input_text = "\n".join(
        [f"- {txt} ({likes} likes)" for txt,likes in sorted(comments,key=lambda x:x[1],reverse=True)[:5]]
    )

    prompt = f"""Voici des commentaires d'une vidéo récupérés sur YouTube : {input_text}
    Analyse ces commentaires et dit moi ci en 1 la video est pertinente , en 2 pour quelle type de spectatuers c'est reserver , en 3 tu donne une note /10 pour la pertinence , 
    en 4 tu donne une raison pour laquelle tu recommanderait cette video
    ."""

    model = "gemini-2.5-flash"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
    ]

    config = types.GenerateContentConfig(response_modalities=["TEXT"])

    output = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        if getattr(chunk, "text", None):
            output += chunk.text

    return output.strip()
async def youtube_se(update,context):
    if not context.args :
        await update.message.reply_text("Ghost 🤖 : Utilisation correcte /movie <nom de la video a rechercher>")
        return 
    name="".join(context.args)      
    (video_id,title,likes,vues),(playlist_id,playlist_title) = await search_video(name)
    await update.message.reply_text(f"\n\tVideo trouvee : {title}")
    await update.message.reply_text(f"lien : https://www.youtube.com/watch?v={video_id}")
    await update.message.reply_text(f"Nombres De Likes : {likes} | Vues : {vues} ")
    await update.message.reply_text("Analyses des commentaires des differentes video ...")
    comment = await commentaries(video_id)
    recommandation = analyse_comments(comment)
    await update.message.reply_text("Meilleur Commentaire Trouvee ")
    await update.message.reply_text(f"{len(comment)} commentaires recuperes.")
    await update.message.reply_text("\n=== Video recommandee a partir des commentaires ===")
    await update.message.reply_text(recommandation)
    await update.message.reply_text("\n")
    #Playlist recuperes
    await update.message.reply_text(f"\n\t=== Meilleure Playlist Trouvée Pour {name} : {playlist_title} ===")
    await update.message.reply_text(f"-URL de la playlist : https://www.youtube.com/playlist?list={playlist_id}")
    total = await info_playlist(playlist_id)
    await update.message.reply_text(f"Nombre De Video De La Playlist {total} videos")
    await update.message.reply_text("\n=== Recommandation de la Playlist ===")
    analyse = analyse_playlist(playlist_id, playlist_title)
    await update.message.reply_text(analyse)

#test connexion 
async def ping (update,context) :
    user=update.message.from_user
    await update.message.reply_text(f"MOSTWANTED_BOT 🤖\n\n\nsalut ☺️ {user.first_name} je suis en ligne ✅  ") 
  
# Réponses automtiques
async def auto_reply(update,context):
    bot_username = context.bot.username.lower()
    text = update.message.text.lower()
    user=update.message.from_user
    if (update.message.chat.type != 'private') and (f"@{bot_username}" not in text):
        return

    text = text.replace(f"@{bot_username}", "").strip()

    if "bonjour" in text or "salut" in text:
        reply = f"Ghost 🤖 :Salut 👋 {user.first_name} comment tu vas ?"
    elif "ça va" in text:
        reply = "Ghost 🤖 : Oui ça va très bien merci 🤖 et toi ?"
    elif "merci" in text:
        reply = "Ghost 🤖 : Avec plaisir 😎"
    elif "heure" in text:
        now = time_command()
        reply = f"Ghost 🤖 : ⏰ Il est actuellement {now.strftime('%H:%M:%S')}"
    elif "ton nom" in text:
        reply = "Ghost 🤖 : Je suis ton GHOST  🤖 créé par MOSTWANTED 😎"
    elif  "api" in text  or  "token" in text :
        reply ="Ghost 🤖 : Bien essayer mais tu auras pas mes clés si facilement 😂😂☺️"
    elif "idiot" in text:
        reply = "Ghost 🤖 : Va te faire foutre🖕️"
    elif  "yo" in text :
        reply = f"Ghost 🤖 : yess  {user.first_name} ça dit quoi "
    elif  "ça dit quoi" in text :
        reply="Ghost 🤖 : yes mon Cho carré et toi😎"
    elif "asser" in text :
        reply=f"Ghost 🤖 : wy {user.first_name}" 
    elif "qui es tu" in text or "ton nom" in text:
        reply ="Ghost 🤖 : un mini bot créer par MOSTWANTED 😎"
    else:
        responses = [
            "Ghost 🤖 : RÉPONSE ALÉATOIRE 🔀 \n Salut 👋 ça va ?",
            "Ghost 🤖 : RÉPONSE ALÉATOIRE 🔀 \n Je suis un bot 🤖 je suis l'assistant de MOSTWANTED 😎️!",
            "Ghost 🤖 : RÉPONSE ALÉATOIRE 🔀 \n Pour le moment mon boss est occupé, veuillez patienter quelques instants",
            "Ghost 🤖 : RÉPONSE ALÉATOIRE 🔀 \n Je vais bien, j'espère que c'est aussi ton cas 🤗",
            "Ghost 🤖 : RÉPONSE ALÉATOIRE 🔀 \n Intéressant 🤔... dis m’en plus",
            "Ghost 🤖 : RÉPONSE ALÉATOIRE 🔀 \n Je te conseille d'être très attentif sur ton projet scolaire 🙏",
            "Ghost 🤖 : RÉPONSE ALÉATOIRE 🔀 \n Haha 😅 bonne blague !",
            "Ghost 🤖 : RÉPONSE ALÉATOIRE 🔀 \n As-tu déjà fait tes devoirs ? ✍️",
            "Ghost 🤖 : RÉPONSE ALÉATOIRE 🔀 \n As-tu déjà mangé ? 🥞",
            "Ghost 🤖 : RÉPONSE ALÉATOIRE 🔀 \n Tu n'as alors rien compris",
            "Ghost 🤖 : RÉPONSE ALÉATOIRE 🔀 \n Sans souci",
            "Ghost 🤖 : RÉPONSE ALÉATOIRE 🔀 \n Good 👍",
            "Ghost 🤖 : RÉPONSE ALÉATOIRE 🔀 \n Es-tu faible ?",
            "Ghost 🤖 : RÉPONSE ALÉATOIRE 🔀 \n Je prends note ✅",
            "Ghost 🤖 : RÉPONSE ALÉATOIRE 🔀 \n Peux-tu expliquer un peu plus ?",
            "Ghost 🤖 : RÉPONSE ALÉATOIRE 🔀 \n Je suis là pour discuter avec toi ✨"
        ]
        reply = choice(responses)

    await update.message.reply_text(reply)

async def clear(update,context):
    chat = update.message.chat
    chat_id = chat.id
    message_id = update.message.message_id

    if chat.type == "private":
        empty_block = "\n\n".join(["\u200E" for _ in range(100)])
        await update.message.reply_text("🧹 Nettoyage de ta messagerie en cours...\n\n" + empty_block + "\n\n✅ Messagerie nettoyée")
        return

    if chat.type in ["group","supergroup"]:
        try:
            for i in range(message_id,message_id-10,-1):
                try:
                   await context.bot.delete_message(chat_id=chat_id,message_id=i)
                except:
                    pass
            await update.message.reply_text("✅ 10 derniers messages supprimés")
        except:
            await update.message.reply_text("❌ Impossible de nettoyer (le bot doit être admin et avoir la permission de suppression)")

async def dice(update,context):
    user=update.messae.from_user
    result= await randint(1,6)
    await update.message.reply_text(f"GENIAL {user.first_name} du as obtenu : 🎲️ {result} ")
    
# Main
async def main():
    app = ApplicationBuilder.token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("hour", time_command))
    app.add_handler(CommandHandler("infos", bot_infos))
    app.add_handler(CommandHandler("getmeteo", meteo))
    app.add_handler(CommandHandler("generate",gen_phrase))
    app.add_handler(CommandHandler("sendto", sendto))
    app.add_handler(CommandHandler("addition", add))
    app.add_handler(CommandHandler("soustraction",sous))
    app.add_handler(CommandHandler("multiplication",multi))
    app.add_handler(CommandHandler("showusers",listusers))
    app.add_handler(CommandHandler("division",div))
    app.add_handler(CommandHandler("modulo",mod))
    app.add_handler(CommandHandler("exp",exp))
    app.add_handler(CommandHandler("question",ask))
    app.add_handler(CommandHandler("audio",play))
    app.add_handler(CommandHandler("movie",youtube_se))
    app.add_handler(CommandHandler("clean",clear))
    app.add_handler(CommandHandler("ping",ping))
    app.add_handler(CommandHandler("de",dice))
    
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND),auto_reply))

    print("Ghost a été lancé avec succès ✅...")
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()  
    
    from telegram.ext import ApplicationBuilder
    
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("aide", help_command))
    app.add_handler(CommandHandler("hour", time_command))
    app.add_handler(CommandHandler("infos", bot_infos))
    app.add_handler(CommandHandler("getmeteo", meteo))
    app.add_handler(CommandHandler("generate",gen_phrase))
    app.add_handler(CommandHandler("sendto", sendto))
    app.add_handler(CommandHandler("addition", add))
    app.add_handler(CommandHandler("soustraction",sous))
    app.add_handler(CommandHandler("multiplication",multi))
    app.add_handler(CommandHandler("showusers",listusers))
    app.add_handler(CommandHandler("division",div))
    app.add_handler(CommandHandler("modulo",mod))
    app.add_handler(CommandHandler("exp",exp))
    app.add_handler(CommandHandler("question",ask))
    app.add_handler(CommandHandler("audio",play))
    app.add_handler(CommandHandler("clean",clear))
    app.add_handler(CommandHandler("movie",youtube_se))
    app.add_handler(CommandHandler("test",ping))
    
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND),auto_reply))

    print("Ghost a été lancé ")
    
    app.run_polling()
    
