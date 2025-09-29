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
1. [Python](https://www.python.org/) (version 3.8 ou supérieure)
2. [Git](https://git-scm.com/)
3. [Visual Studio Code](https://code.visualstudio.com/)

**Préparation avant l'atelier :**
1. **Vérifiez vos outils** :
   - Assurez-vous que Python 3.8+ est installé : `python --version`
   - Assurez-vous que Git est installé : `git --version`
   - Si Git n'est pas installé, téléchargez-le depuis [https://git-scm.com/](https://git-scm.com/).
2. **Introduction à Git** :
   - Git est un outil de gestion de versions. Pour cloner le projet, utilisez :
     ```bash
     git clone https://github.com/AGROTIC-TEAM/agrotic-api-workshop.git
     cd agrotic-api-workshop
     ```
   - Si vous obtenez une erreur (par exemple, "command not found"), vérifiez que Git est installé et ajouté au PATH de votre système.
   - Si vous êtes novice avec Git, demandez de l'aide à votre formateur ou consultez [Git Basics](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Au-sujet-du-contr%C3%B4le-de-version).

---

### ⚙️ 1. Mise en place de l'environnement (10 min)

1. **Clonez le projet :** Ouvrez un terminal et exécutez la commande suivante pour télécharger le projet sur votre machine.
    ```bash
    git clone https://github.com/agrotic-app/tp-api-agrotic
    cd tp-api-agrotic
    ```
   *Note :* Si vous rencontrez des problèmes d'accès au dépôt, contactez votre formateur.

2. **Installez l'extension VSCode :** Dans VSCode, allez dans l'onglet Extensions (Ctrl+Shift+X) et installez **REST Client** (par `huizhou.vs-code-rest`).

3. **Créez un environnement virtuel :** C'est une "boîte" isolée pour les dépendances de notre projet.
    ```bash
    # La commande peut être 'python3' sur macOS/Linux
    python -m venv venv
    ```

4. **Activez l'environnement virtuel :**
   * **Sur Windows (cmd/powershell) :**
       ```powershell
       .\venv\Scripts\Activate
       ```
   * **Sur macOS / Linux :**
       ```bash
       source venv/bin/activate
       ```
   *(Votre terminal devrait maintenant afficher `(venv)` au début de la ligne)*


5. **Installez les librairies Python :**
    ```bash
    pip install -r requirements.txt
    ```


6.  **Exécutez l'application Flask :**
    ```bash
    flask run
    ```
    Une fois le serveur démarré, vous devriez voir un message dans votre terminal indiquant qu'il est actif, généralement à l'adresse `http://127.0.0.1:5000`. Vous pouvez alors ouvrir cette URL dans votre navigateur pour voir votre application en action.

Vous êtes prêt !

---

### 🌦️ 2. Acte I : L'explorateur météo (consommation)

Votre mission est de contacter l'API météo **Open-Meteo** pour récupérer les données d'une parcelle près de Montpellier. Mais pour cela, il vous faudra d'abord lire la documentation pour savoir *comment* lui parler !

**Exercice 1 : Construire la requête**

1. Ouvrez le fichier `get_weather.py`. Vous y trouverez une URL de base et un dictionnaire `params` vide.
2. Rendez-vous sur la **documentation officielle d'Open-Meteo : [https://open-meteo.com/en/docs](https://open-meteo.com/en/docs)**.
3. **Votre mission :** Lisez la documentation pour trouver les bons paramètres à ajouter au dictionnaire `params` afin d'obtenir :
   * La météo actuelle.
   * Le cumul de précipitation journalier.
   * Les données pour le fuseau horaire de Paris.
4. Une fois le dictionnaire complété, exécutez le script : `python get_weather.py`.

<details>
<summary>💡 En cas de blocage pour l'exercice 1, cliquez ici</summary>

* **Indice 1 (Structure) :** Une URL de requête se compose de l'URL de base, suivie d'un `?`, puis des paires `cle=valeur` séparées par des `&`. La librairie `requests` s'en occupe pour nous avec le dictionnaire `params`. Vous devez juste trouver les bonnes clés et valeurs.
* **Indice 2 (Météo actuelle) :** Cherchez le paramètre `current_weather` dans la documentation. La doc précise qu'il faut lui donner la valeur `true` pour l'activer.
* **Indice 3 (Données journalières) :** Le paramètre pour les données journalières est `daily`. La documentation montre qu'il faut lui préciser *quelles* données on veut. Pour le cumul de pluie, la valeur sera donc `precipitation_sum`.
* **Indice 4 (Fuseau horaire) :** Cherchez `timezone` dans la doc. Pour Paris, la valeur requise est `Europe/Paris`.

</details>

**Exercice 2 : Extraire les données**

1. Ouvrez `get_weather.py` et trouvez la section `TODO`.
2. Extrayez la température actuelle et le cumul de précipitation journalier depuis le dictionnaire `data`.
3. Ajoutez une gestion d'erreur pour vérifier si les clés existent. Par exemple, utilisez `data.get('current_weather', {}).get('temperature', 'N/A')` ou un bloc `try-except` pour gérer les `KeyError`.
4. Testez votre script avec `python get_weather.py` et vérifiez la sortie.

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

1. Ouvrez le fichier `app.py`. Le code de base pour une API simple y est déjà présent.
2. Lancez le serveur depuis votre terminal : `python app.py`.
3. Ouvrez votre navigateur et allez sur `http://127.0.0.1:5000`. Vous devriez voir un message de bienvenue ! Cela confirme que votre serveur fonctionne.

**Exercice 4 : L'API d'aide à l'irrigation**

1. Ouvrez `app.py` et trouvez le `TODO` pour la route `/conseil-irrigation`.
2. Utilisez `request.args.get('lat')` et `request.args.get('lon')` pour récupérer la latitude et la longitude des paramètres de l'URL.
3. Validez que `lat` et `lon` sont fournis et sont des nombres valides. Sinon, renvoyez une réponse JSON d'erreur avec le code HTTP 400 en utilisant `abort(400, description="Message d'erreur")`.
4. Réutilisez la logique de l'API météo de `get_weather.py` pour récupérer les données et renvoyer une réponse JSON avec un conseil d'irrigation.
5. Ajoutez une fonction pour déterminer le conseil d'irrigation basé sur les données météo. Par exemple :
   - Si les précipitations sont inférieures à 5 mm et la température dépasse 25°C, recommandez l'irrigation.
   - Sinon, conseillez de ne pas irriguer.
6. Implémentez cette logique dans la route `/conseil-irrigation` avant de renvoyer la réponse JSON. Exemple :
    ```python
    advice = "Irrigation recommandée" if precipitation < 5 and temperature > 25 else "Pas d'irrigation nécessaire"
    ```
7. Assurez-vous que le champ `advice` est inclus dans la réponse JSON.

**Tester votre nouvelle API avec REST Client**

1. Une fois votre code écrit, arrêtez et relancez votre serveur (`python app.py`).
2. Ouvrez le fichier `requests.http` dans VSCode.
3. Cliquez sur "Send Request" à côté de chaque requête dans `requests.http` pour tester votre API.
4. Interprétez les réponses :
   - **200 OK** : La requête a réussi. Vérifiez la sortie JSON pour la température, les précipitations et le conseil d'irrigation.
   - **400 Bad Request** : Paramètres manquants ou invalides (par exemple, `lat` ou `lon`). Lisez le champ `description` pour plus de détails.
   - **500 Internal Server Error** : Problème avec l'API Open-Meteo ou la logique du serveur. Vérifiez votre code et l'état de l'API.
5. Essayez de modifier les valeurs de `lat` et `lon` dans `requests.http` pour tester d'autres lieux (par exemple, Paris : `lat=48.8566&lon=2.3522`).
6. Si REST Client ne fonctionne pas, essayez `curl` dans le terminal :
    ```bash
    curl http://127.0.0.1:5000/conseil-irrigation?lat=43.6119&lon=3.8772
    ```

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
* **Défi 2 :** Modifiez la route `/conseil-irrigation` pour accepter un paramètre `type_culture` (par exemple, `?lat=...&lon=...&type_culture=mais`). Définissez un dictionnaire avec les besoins en eau des cultures (par exemple, maïs : 5 mm/jour, vigne : 3 mm/jour). Ajustez la logique d'irrigation pour recommander l'irrigation si les précipitations sont inférieures au besoin de la culture et la température dépasse 25°C. Mettez à jour la réponse JSON pour inclure le type de culture.
* **Défi 3 :** Gérez mieux les erreurs. Que se passe-t-il si les paramètres `lat` ou `lon` sont manquants ? Renvoyez un message d'erreur clair avec un code de statut 400 (Bad Request).
* **Défi 4 :** Modifiez la route `/conseil-irrigation` pour récupérer le paramètre `et0_fao_evapotranspiration` depuis Open-Meteo (voir [https://open-meteo.com/en/docs](https://open-meteo.com/en/docs)). Ajustez la logique d'irrigation pour recommander l'irrigation si l'évapotranspiration dépasse 4 mm/jour et les précipitations sont insuffisantes. Mettez à jour la réponse JSON pour inclure les données d'évapotranspiration.
* **Défi 5 :** Créez un fichier `weather_chart.html` pour afficher un graphique en barres des précipitations journalières avec Chart.js. Récupérez 5 jours de données de précipitation depuis Open-Meteo en ajoutant `"daily": "precipitation_sum"` et `forecast_days=5` dans les paramètres de l'API. Mettez à jour l'objet `data` de Chart.js avec les valeurs récupérées. Ouvrez `weather_chart.html` dans un navigateur pour voir le graphique.

---

### 📊 Visualisation des données

Pour visualiser les données, deux outils sont fournis :
1. **Graphique des précipitations** : Le fichier `weather_chart.html` affiche un graphique en barres des précipitations journalières. Ouvrez-le dans un navigateur pour voir le résultat. Pour intégrer des données réelles, modifiez le script pour appeler une route API (voir Défi 5).
2. **Diagramme du flux de données** : Un diagramme Mermaid est inclus dans `api_flow.mmd`. Ouvrez-le dans VSCode avec l'extension Mermaid pour visualiser le flux entre le client REST, votre API Flask, et l'API Open-Meteo.

---

### Solutions
Consultez les fichiers `solutions/get_weather_solution.py` et `solutions/app_solution.py` pour vérifier vos réponses après avoir terminé les exercices.

---

### 🕒 Planning de l'atelier (2h30)

| Section | Durée estimée |
|---------|---------------|
| Mise en place de l'environnement | 10 min |
| Acte I : L'explorateur météo | 40 min |
| Acte II : Le créateur de service | 60 min |
| Défis pour les plus rapides | 30 min |
| Conclusion & discussion | 10 min |

---

### 📚 Conclusion & ressources pour aller plus loin



Félicitations ! Vous avez consommé une API et créé la vôtre en moins de 3 heures. Vous avez découvert les concepts de **route**, de **paramètres**, de **JSON** et vu comment des services peuvent communiquer entre eux.

* **Documentation de Flask :** [Welcome to Flask](https://flask.palletsprojects.com/)
* **Documentation de Requests :** [Requests Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/)
* **Une liste d'APIs publiques amusantes :** [Public APIs](https://github.com/public-apis/public-apis)