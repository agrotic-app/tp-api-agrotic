# 🚜 TP API AgroTIC : De la consommation à la création

Bienvenue dans cet atelier de 2h30 pour découvrir le monde des APIs !

**Votre mission :** Vous êtes ingénieur(e) AgroTIC. Un client agronome a besoin d'un outil simple pour l'aider à décider s'il doit irriguer sa parcelle. Votre rôle est de récupérer des données météo brutes, de les transformer en un conseil clair et de le rendre accessible via une API que vous allez créer.

**Objectifs Pédagogiques :**

- Comprendre ce qu'est une API et à quoi ça sert.
- Consommer une API externe (météo) avec Python.
- Créer votre propre API web simple avec le framework Flask.
- Tester vos points d'accès (endpoints) avec un client REST.

---

### ✅ Prérequis

Avant de commencer, assurez-vous d'avoir installé :

1.  [Python](https://www.python.org/) (version 3.8 ou supérieure)
2.  [Git](https://git-scm.com/)
3.  [Visual Studio Code](https://code.visualstudio.com/)

---

### ⚙️ 1. Mise en Place de l'Environnement (10 min)

1.  **Clonez le projet :** Ouvrez un terminal et exécutez la commande suivante pour télécharger le projet sur votre machine.

    ```bash
    git clone [https://github.com/VOTRE_NOM_UTILISATEUR/NOM_DU_REPO.git](https://github.com/VOTRE_NOM_UTILISATEUR/NOM_DU_REPO.git)
    cd NOM_DU_REPO
    ```

2.  **Installez l'extension VSCode :** Dans VSCode, allez dans l'onglet Extensions (Ctrl+Shift+X) et installez **REST Client** (par `huizhou.vs-code-rest`).

3.  **Créez un environnement virtuel :** C'est une "boîte" isolée pour les dépendances de notre projet.

    ```bash
    # La commande peut être 'python3' sur macOS/Linux
    python -m venv venv
    ```

4.  **Activez l'environnement virtuel :**

        - **Sur Windows (cmd/powershell) :**
          ```powershell
          .\venv\Scripts\Activate
          ```
        - **Sur macOS / Linux :**
          `bash

    source venv/bin/activate
    `      _(Votre terminal devrait maintenant afficher`(venv)` au début de la ligne)\_

5.  **Installez les librairies Python :**
    ```bash
    pip install -r requirements.txt
    ```

Vous êtes prêt !

---

### 🌦️ 2. Acte I : L'Explorateur Météo (Consommation)

Notre première étape est de récupérer les données météo pour une parcelle située près de Montpellier. Nous utiliserons l'API **Open-Meteo**.

**Exercice 1 & 2 : Récupérer et extraire la température**

1.  Ouvrez le fichier `get_weather.py`.
2.  Analysez le code fourni ci-dessous, puis copiez-le dans votre fichier.
3.  Exécutez le script depuis votre terminal : `python get_weather.py`

<details>
<summary>▶️ Cliquez ici pour voir le code de l'exercice 1 & 2</summary>

```python
# get_weather.py
import requests

# Coordonnées GPS de Montpellier
LATITUDE = 43.61
LONGITUDE = 3.87

# URL de l'API Open-Meteo
# On demande la météo actuelle et le cumul de pluie journalier
url = f"[https://api.open-meteo.com/v1/forecast?latitude=](https://api.open-meteo.com/v1/forecast?latitude=){LATITUDE}&longitude={LONGITUDE}&current_weather=true&daily=precipitation_sum&timezone=Europe/Paris"

print("Appel à l'API Open-Meteo...")

# On effectue la requête GET
response = requests.get(url)

# On vérifie si la requête a réussi (code de statut 200)
if response.status_code == 200:
    print("Succès ! Données reçues.")
    # On transforme la réponse (texte) en un dictionnaire Python (JSON)
    data = response.json()

    # --- EXERCICE 2 : Extraction ---
    # Naviguez dans le dictionnaire pour extraire la température actuelle
    current_temp = data['current_weather']['temperature']
    print(f"🌡️ Température actuelle à Montpellier : {current_temp}°C")

    # Défi : Extraire le cumul de pluie prévu pour aujourd'hui (c'est le premier élément de la liste 'daily')
    rain_today = data['daily']['precipitation_sum'][0]
    print(f"💧 Cumul de pluie prévu aujourd'hui : {rain_today} mm")

else:
    print(f"Erreur, la requête a échoué avec le code : {response.status_code}")

```

</details>

---

### 🛠️ 3. Acte II : Le Créateur de Service (Création)

Maintenant, nous allons créer notre propre API pour fournir un conseil simple à notre agronome.

**Exercice 3 : Notre première API "Hello, Farmer!"**

1.  Ouvrez le fichier `app.py`.
2.  Copiez-y le code ci-dessous pour créer un serveur web minimaliste.

<details>
<summary>▶️ Cliquez ici pour voir le code de l'exercice 3</summary>

```python
# app.py
from flask import Flask

# On crée l'application Flask
app = Flask(__name__)

# On définit une "route", une URL que notre API peut recevoir
@app.route('/')
def hello():
    return "Bienvenue sur l'Agro-Conseil API ! 🌾"

# Cette partie permet de lancer le serveur en exécutant 'python app.py'
if __name__ == '__main__':
    app.run(debug=True)
```

</details>

3.  Lancez le serveur depuis votre terminal : `python app.py`.
4.  Ouvrez votre navigateur et allez sur `http://127.0.0.1:5000`. Vous devriez voir le message de bienvenue !

**Exercice 4 : L'API d'aide à l'irrigation**

Nous allons maintenant créer le cœur de notre service : une route `/conseil-irrigation` qui prend des coordonnées GPS en paramètres, appelle l'API météo, et renvoie un conseil.

1.  Modifiez votre fichier `app.py` pour y ajouter le code suivant.

<details>
<summary>▶️ Cliquez ici pour voir le code de l'exercice 4</summary>

```python
# app.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return "Bienvenue sur l'Agro-Conseil API ! 🌾"

# Nouvelle route pour le conseil d'irrigation
@app.route('/conseil-irrigation')
def irrigation_advice():
    # On récupère les paramètres d'URL (ex: ?lat=43.6&lon=3.8)
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    # Validation simple : on vérifie que les paramètres sont bien présents
    if not lat or not lon:
        return jsonify({"erreur": "Les paramètres 'lat' et 'lon' sont requis."}), 400

    # --- On réutilise notre logique de la Partie 1 ---
    url = f"[https://api.open-meteo.com/v1/forecast?latitude=](https://api.open-meteo.com/v1/forecast?latitude=){lat}&longitude={lon}&daily=precipitation_sum&timezone=Europe/Paris"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"erreur": "L'API météo n'a pas pu être contactée."}), 500

    data = response.json()
    rain_today = data['daily']['precipitation_sum'][0]

    # --- Logique métier très simple ---
    conseil = "NON"
    if rain_today < 5.0:
        conseil = "OUI"

    # On prépare la réponse JSON
    result = {
        "coordonnees": {"lat": lat, "lon": lon},
        "pluie_prevue_aujourdhui_mm": rain_today,
        "decision_irrigation": conseil
    }

    # 🕵️ Easter Egg !
    if float(lat) == 90.0:
        result = {"decision_irrigation": "NON", "message": "Pas besoin d'irriguer le Pôle Nord ! 🥶"}

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
```

</details>

**Tester notre nouvelle API avec REST Client**

1.  Arrêtez et relancez votre serveur `python app.py`.
2.  Ouvrez le fichier `requests.http` et copiez-y le texte suivant.
3.  Cliquez sur le petit "Send Request" qui apparaît au-dessus du texte.

<details>
<summary>▶️ Cliquez ici pour voir le contenu de requests.http</summary>

```http
### Test de notre API d'irrigation

# Requête pour Montpellier
GET [http://127.0.0.1:5000/conseil-irrigation?lat=43.6&lon=3.8](http://127.0.0.1:5000/conseil-irrigation?lat=43.6&lon=3.8)

###

# Requête pour Brest (il pleut souvent là-bas !)
GET [http://127.0.0.1:5000/conseil-irrigation?lat=48.39&lon=-4.48](http://127.0.0.1:5000/conseil-irrigation?lat=48.39&lon=-4.48)

###

# Test de l'Easter Egg du Pôle Nord !
GET [http://127.0.0.1:5000/conseil-irrigation?lat=90&lon=0](http://127.0.0.1:5000/conseil-irrigation?lat=90&lon=0)
```

</details>

---

### 🏆 Défis pour les plus rapides

Si vous avez terminé, voici quelques idées pour aller plus loin :

- **Défi 1 :** Créer une nouvelle route `/info-parcelle/<id_parcelle>` qui utilise un **paramètre de chemin** et renvoie un JSON avec de fausses informations sur la parcelle (type de sol, culture...).
- **Défi 2 :** Dans la route `/conseil-irrigation`, ajoutez un paramètre `type_culture` (ex: `?lat=...&lon=...&type_culture=mais`). La logique de décision doit changer : le maïs a besoin de plus d'eau que la vigne !
- **Défi 3 :** Gérez mieux les erreurs. Que se passe-t-il si l'API météo renvoie une erreur ? Ou si les coordonnées sont invalides ?

---

### 📚 Conclusion & Ressources pour aller plus loin

Félicitations ! Vous avez consommé une API et créé la vôtre en moins de 3 heures. Vous avez découvert les concepts de **route**, de **paramètres**, de **JSON** et vu comment des services peuvent communiquer entre eux.

- **Documentation de Flask :** [Welcome to Flask](https://flask.palletsprojects.com/)
- **Documentation de Requests :** [Requests Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/)
- **Une liste d'APIs publiques amusantes :** [Public APIs](https://github.com/public-apis/public-apis)
