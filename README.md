# 🚜 TP API pour l'AgroTIC : de la consommation à la création

Bienvenue dans cet atelier de 2h30 pour découvrir le monde des APIs !

**Votre mission :** Vous êtes ingénieur(e) AgroTIC. Un client agronome a besoin d'un outil simple pour l'aider à décider s'il doit irriguer sa parcelle. Votre rôle est de récupérer des données météo brutes, de les transformer en un conseil clair et de le rendre accessible via une API que vous allez créer.

**Objectifs pédagogiques :**
* Comprendre ce qu'est une API et à quoi ça sert.
* Consommer une API externe (météo) avec Python.
* Créer votre propre API web simple avec le framework Flask.
* Tester vos points d'accès (endpoints) avec un client REST.

---

### ✅ Prérequis

Avant de commencer, assurez-vous d'avoir installé :
1.  [Python](https://www.python.org/) (version 3.8 ou supérieure)
2.  [Git](https://git-scm.com/)
3.  [Visual Studio Code](https://code.visualstudio.com/)

---

### ⚙️ 1. Mise en place de l'environnement (10 min)

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
    * **Sur Windows (cmd/powershell) :**
        ```powershell
        .\venv\Scripts\Activate
        ```
    * **Sur macOS / Linux :**
        ```bash
        source venv/bin/activate
        ```
    *(Votre terminal devrait maintenant afficher `(venv)` au début de la ligne)*

5.  **Installez les librairies Python :**
    ```bash
    pip install -r requirements.txt
    ```

Vous êtes prêt !

---

### 🌦️ 2. Acte I : L'explorateur météo (consommation)

Votre mission est de contacter l'API météo **Open-Meteo** pour récupérer les données d'une parcelle près de Montpellier. Mais pour cela, il vous faudra d'abord lire la documentation pour savoir *comment* lui parler !

**Exercice 1 : Construire la requête**

1.  Ouvrez le fichier `get_weather.py`. Vous y trouverez une URL de base et un dictionnaire `params` vide.
2.  Rendez-vous sur la **documentation officielle d'Open-Meteo : [https://open-meteo.com/en/docs](https://open-meteo.com/en/docs)**.
3.  **Votre mission :** Lisez la documentation pour trouver les bons paramètres à ajouter au dictionnaire `params` afin d'obtenir :
    * La météo actuelle.
    * Le cumul de précipitation journalier.
    * Les données pour le fuseau horaire de Paris.
4.  Une fois le dictionnaire complété, exécutez le script : `python get_weather.py`.

<details>
<summary>💡 En cas de blocage pour l'exercice 1, cliquez ici</summary>

* **Indice 1 (Structure) :** Une URL de requête se compose de l'URL de base, suivie d'un `?`, puis des paires `cle=valeur` séparées par des `&`. La librairie `requests` s'en occupe pour nous avec le dictionnaire `params`. Vous devez juste trouver les bonnes clés et valeurs.
* **Indice 2 (Météo actuelle) :** Cherchez le paramètre `current_weather` dans la documentation. La doc précise qu'il faut lui donner la valeur `true` pour l'activer.
* **Indice 3 (Données journalières) :** Le paramètre pour les données journalières est `daily`. La documentation montre qu'il faut lui préciser *quelles* données on veut. Pour le cumul de pluie, la valeur sera donc `precipitation_sum`.
* **Indice 4 (Fuseau horaire) :** Cherchez `timezone` dans la doc. Pour Paris, la valeur requise est `Europe/Paris`.

</details>

**Exercice 2 : Extraire les données**

Maintenant que vous recevez les données, votre script affiche un gros bloc JSON.

1.  **Votre mission :** Suivez les instructions `TODO` de l'**Exercice 2** dans le fichier `get_weather.py` pour extraire et afficher proprement la température et le cumul de pluie.

<details>
<summary>💡 En cas de blocage pour l'exercice 2, cliquez ici</summary>

* **Indice 1 :** La variable `data` est un dictionnaire Python. Vous pouvez accéder à ses clés avec `data['nom_de_la_cle']`.
* **Indice 2 :** Pour voir la structure, n'hésitez pas à ajouter `print(data)` au début de votre code pour visualiser toutes les clés disponibles.
* **Indice 3 :** Les valeurs peuvent être elles-mêmes des dictionnaires ! Pour accéder à une valeur nichée, on enchaîne les clés : `data['cle_principale']['cle_secondaire']`.
* **Indice 4 :** Pour le cumul de pluie, la clé `'precipitation_sum'` contient une *liste*. Il faut donc accéder à son premier élément avec `[0]`.

</details>

---

### 🛠️ 3. Acte II : Le créateur de service (création)

Maintenant, nous allons créer notre propre API pour fournir un conseil simple à notre agronome.

**Exercice 3 : Notre première API "Hello, Farmer!"**

1.  Ouvrez le fichier `app.py`. Le code de base pour une API simple y est déjà présent.
2.  Lancez le serveur depuis votre terminal : `python app.py`.
3.  Ouvrez votre navigateur et allez sur `http://127.0.0.1:5000`. Vous devriez voir un message de bienvenue ! Cela confirme que votre serveur fonctionne.

**Exercice 4 : L'API d'aide à l'irrigation**

Suivez les instructions `TODO` dans `app.py` pour créer la route `/conseil-irrigation`.

**Tester votre nouvelle API avec REST Client**

Une fois votre code écrit, arrêtez et relancez votre serveur (`python app.py`).
Ouvrez le fichier `requests.http` et cliquez sur "Send Request" pour tester votre API avec différentes coordonnées et vérifier qu'elle se comporte comme attendu.

<details>
<summary>💡 En cas de blocage, cliquez ici pour des indices</summary>

* **Indice 1 (Décorateur) :** N'oubliez pas le décorateur `@app.route('/conseil-irrigation')` juste avant la définition de votre fonction.
* **Indice 2 (Paramètres) :** Pour récupérer les paramètres d'URL (`?lat=...`), utilisez l'objet `request` de Flask : `lat = request.args.get('lat')`. N'oubliez pas d'importer `request` depuis `flask` !
* **Indice 3 (Réutiliser le code) :** Copiez-collez la logique d'appel à l'API météo que vous avez écrite dans `get_weather.py`.
* **Indice 4 (Retourner du JSON) :** Une API doit retourner un format standardisé. Utilisez la fonction `jsonify()` de Flask pour transformer un dictionnaire Python en une réponse JSON valide. Par exemple : `return jsonify({"cle": "valeur"})`.

</details>

---

### 🏆 Défis pour les plus rapides

Si vous avez terminé, voici quelques idées pour aller plus loin :

* **Défi 1 :** Créer une nouvelle route `/info-parcelle/<id_parcelle>` qui utilise un **paramètre de chemin** et renvoie un JSON avec de fausses informations sur la parcelle (type de sol, culture...).
* **Défi 2 :** Dans la route `/conseil-irrigation`, ajoutez un paramètre `type_culture` (ex: `?lat=...&lon=...&type_culture=mais`). La logique de décision doit changer : le maïs a besoin de plus d'eau que la vigne !
* **Défi 3 :** Gérez mieux les erreurs. Que se passe-t-il si les paramètres `lat` ou `lon` sont manquants ? Renvoyez un message d'erreur clair avec un code de statut 400 (Bad Request).

---

### 📚 Conclusion & ressources pour aller plus loin

Félicitations ! Vous avez consommé une API et créé la vôtre en moins de 3 heures. Vous avez découvert les concepts de **route**, de **paramètres**, de **JSON** et vu comment des services peuvent communiquer entre eux.

* **Documentation de Flask :** [Welcome to Flask](https://flask.palletsprojects.com/)
* **Documentation de Requests :** [Requests Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/)
* **Une liste d'APIs publiques amusantes :** [Public APIs](https://github.com/public-apis/public-apis)