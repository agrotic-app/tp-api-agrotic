# TP API pour AgroTIC : La Chaîne de Décision de Fauche

Bienvenue dans cet atelier de **2h30** pour découvrir l'architecture et l'interconnexion des APIs dans un contexte agronomique.

## Votre Mission : Développeur(se) pour la F.A.U.C.H.E.

Vous faites partie d'une équipe de développeurs AgroTIC. Votre client a besoin d'un outil d'aide à la décision pour optimiser la **fauche de ses prairies de foin**. La fauche est un processus critique qui demande de combiner plusieurs facteurs : la **maturité de la culture**, les **prévisions météo** et les **risques environnementaux/logistiques**.

**Votre rôle est de participer collectivement à la construction d'une chaîne d'APIs :**
1.  **APIs Filles (Les Experts) :** Chaque binôme développe une API spécialisée (Degrés-Jours, Météo, Risques) qui fournit un indicateur clé.
2.  **API Mère (Le Décideur) :** Un binôme développera l'API finale qui appelle les APIs filles, combine les résultats et renvoie le conseil de fauche final.

**Objectifs Pédagogiques :**
* **Comprendre l'Architecture Microservices :** Comment des services isolés communiquent pour résoudre un problème complexe.
* **Consommer une API Externe (Météo) :** Appeler un service public pour récupérer des données brutes.
* **Créer et Interconnecter vos propres APIs (Flask) :** Utiliser votre IP locale pour appeler le service développé par un autre binôme.
* **Modélisation Agronomique :** Traduire des règles agronomiques (DDC, Risque Faune, Météo de Séchage) en code.

---

## Distribution des Rôles (Groupes de 3 et 4 binômes)

Chaque binôme sera responsable du développement et de la documentation de son API, en respectant le **contrat JSON** pour que l'API Mère puisse s'y connecter.

| Groupe | Binôme | Rôle de l'API | Fonction Agronomique |
| :--- | :--- | :--- | :--- |
| **G1 & G2** | **B1 (API Mère)** | `api-decision-fauche` | **Synthèse et Décision** : Appelle toutes les autres APIs, applique la logique finale pour dire OUI/NON à la fauche. |
| **G1 & G2** | **B2 (API Fille 1)** | `api-degres-jours` | **Maturité de la Culture** : Calcule le DDC pour vérifier si la culture est prête. |
| **G1 & G2** | **B3 (API Fille 2)** | `api-meteo-sechage` | **Logistique Séchage** : Vérifie l'absence de pluie et les conditions de séchage pour les 48h suivantes. |
| **G2** | **B4 (API Fille 3)** | `api-risque-faon` | **Biodiversité/Risque Faune** : Évalue le risque de présence de faons (logique simulée). |

---

## Prérequis et Environnement de Travail

### Prérequis Techniques

Avant de commencer, assurez-vous d'avoir installé :
1.  **[Python](https://www.python.org/)** (version 3.8 ou supérieure)
2.  **[Git](https://git-scm.com/)**
3.  **[Visual Studio Code](https://code.visualstudio.com/)**

### Mise en place de l'environnement

1.  **Vérifiez vos outils :**
    * Assurez-vous que Python 3.8+ est installé : `python --version`
    * Assurez-vous que Git est installé : `git --version`
    * *Si Git n'est pas installé ou non trouvé, téléchargez-le depuis le site officiel.*

2.  **Clonez le projet :**
    ```bash
    git clone [https://github.com/agrotic-app/tp-api-agrotic](https://github.com/agrotic-app/tp-api-agrotic)
    cd tp-api-agrotic
    ```
    *Note : Si vous êtes novice avec Git, demandez de l'aide à votre formateur.*

3.  **Installez l'extension VSCode :** Dans VSCode, installez l'extension **REST Client** (par `huizhou.vs-code-rest`) pour tester facilement vos APIs.

4.  **Créez un environnement virtuel :**
    ```bash
    # La commande peut être 'python3' sur macOS/Linux
    python -m venv venv
    ```

5.  **Activez l'environnement virtuel :**
    * **Sur Windows (cmd/powershell) :**
        ```powershell
        .\venv\Scripts\Activate
        ```
    * **Sur macOS / Linux :**
        ```bash
        source venv/bin/activate
        ```
    *(Votre terminal devrait afficher `(venv)`)*

6.  **Installez les librairies Python :**
    ```bash
    pip install -r requirements.txt
    ```

7. **Déterminer votre Adresse IP** (pour l'interconnexion)

    Pour que l'API Mère puisse communiquer avec les APIs Filles, vous devez connaître l'adresse IP de votre machine sur le réseau local.

    Cette adresse IP doit remplacer la partie `192.168.1.XX` dans les variables `URL_DDC`, `URL_METEO`, etc., de votre fichier `api_fauche.py`.

    | Système d'exploitation | Commande à exécuter | Note : Cherchez l'adresse IPv4/inet de votre connexion Wi-Fi/Ethernet |
    | :--- | :--- | :--- |
    | **Windows** (cmd/PowerShell) | `ipconfig` | Cherchez la ligne **`IPv4 Address`**. |
    | **macOS** (Terminal) | `ifconfig` ou `ipconfig getifaddr en0` | Cherchez la ligne **`inet`**. |
    | **Ubuntu/Linux** (Terminal) | `ip a` (ou `ip address`) | Cherchez la ligne **`inet`** dans la bonne interface (`wlan0` ou `eth0`). |

    > **Exemple :** Si votre IP est `192.168.1.150`, l'API DDC de votre binôme doit être appelée via `http://192.168.1.150:5001/api-degres-jours`.


8.  **Exécutez l'application Flask :**
    ```bash
    flask run --debug --host=0.0.0.0
    ```
    *Le serveur devrait être actif sur `http://127.0.0.1:5000` 

---


## 1. Acte I : L'API Degrés-Jours Cumulés (DDC)

Votre binôme (API Fille 1) doit développer l’API qui détermine la **maturité** du foin.  
Pour cela, vous allez calculer les **Degrés-Jours Cumulés (DDC)**, une mesure thermique du développement des plantes.

$$\text{DDC} = \sum (\text{Température Moyenne} - \text{Température de Base})$$

Pour les graminées de foin, la **Température de Base ($T_b$)** est fixée à **6 °C**.

---

### 🔹 Objectif
Calculer le DDC à partir des **données historiques Open-Meteo** (sous-domaine `archive-api`) entre le **1er mars** de l’année en cours et la date du jour, puis indiquer si la maturité est atteinte.

---

### 🧩 Exercice 1 : Construire et consommer la requête historique

1. Ouvrez le fichier `degres_jours.py`.  
2. **Cherchez la documentation** Open-Meteo pour l’API **Archive** et trouvez :
   - l’**URL de base** pour les données historiques (`archive-api.open-meteo.com`),
   - le paramètre `daily` correspondant à la température moyenne (`temperature_2m_mean`).
3. Complétez les variables :
   - `URL_HISTORIQUE`
   - `params` (latitude, longitude, timezone, dates)
4. Exécutez le script :  
   ```bash
   python degres_jours.py

### 🧮 Exercice 2 : Calculer le DDC et Afficher la Maturité

Complétez la section `# TODO: Calcul du DDC` :

1. **Extraire la liste des températures** depuis la clé `data['daily']['temperature_2m_mean']`.
2. **Appliquer la formule du DDC** :  
   ```
   DDC_jour = max(0, T_moyenne - T_b)
   ```
3. **Sommer** tous les DDC journaliers pour obtenir `DDC_cumule`.
4. **Déterminer le statut de maturité** selon le seuil :
   - si `DDC_cumule > 600` → **ATTEINTE**
   - sinon → **PAS ENCORE ATTEINTE**
5. **Retourner le résultat au format JSON**, par exemple :
   ```json
   {
     "statut_maturite": "ATTEINTE",
     "ddc_cumule": 650.45,
     "seuil_maturite": 600
   }
   ```

---

💡 **Indices**

<details>
<summary>Indice 1 – URL et Paramètre</summary>
L’API d’archive est sur le sous-domaine `archive-api`.  
Le paramètre pour les températures moyennes journalières se trouve dans la section `daily`.
</details>

<details>
<summary>Indice 2 – Clé de la donnée</summary>
La clé pour les températures moyennes est `temperature_2m_mean`.
</details>

<details>
<summary>Indice 3 – Formule Python</summary>
Vous pouvez utiliser `max(a, b)` pour implémenter la partie `max(0, ...)` de la formule.
</details>

---

## 🌾 Acte II : L'API Séchage du Foin (Agrométéo)

Le séchage du foin dépend fortement des conditions météorologiques à court terme.  
L’objectif de cette API est de fournir un **conseil opérationnel** sur la faisabilité du séchage dans les 48 prochaines heures, à partir des prévisions météo issues de **l’API Open-Meteo Forecast**.

### 🔍 Données utilisées
Les variables horaires suivantes seront extraites depuis l’API :
- `precipitation_sum` (mm) : cumul des précipitations horaires
- `relative_humidity_2m` (%) : humidité relative de l’air à 2 mètres
- `temperature_2m` (°C) *(optionnel)*

###  Seuils agronomiques de référence
| Facteur | Variable | Seuil | Interprétation |
|----------|-----------|--------|----------------|
| Risque de pluie | `precipitation_sum > 0.1 mm` | Risque de séchage impossible |
| Humidité élevée | `relative_humidity_2m > 70 %` | Séchage lent |
| Cumul d’heures humides | `> 30 heures / 48` | Risque global défavorable |

###  Logique de décision
L’analyse suit la hiérarchie suivante :
1. **Pluie prévue** → Séchage non recommandé  
2. **Pas de pluie mais humidité élevée sur > 30h** → Séchage lent / déconseillé  
3. **Humidité modérée et pas de pluie** → Conditions favorables

   🧪 Exemple de sortie attendue

   ```json
   {
      "risque_sechage": "élevé",
      "conseil_sechage": "Risque de pluie détecté — reporter la fauche.",
      "resume": "Prévision de pluie dans les 48h et 35h d'humidité > 70%."
   }
   ```

💡 **Indices**

<details>
<summary>Indice 1 – API utilisée</summary>
Cette API utilise l’endpoint `/forecast` d’Open-Meteo.
</details>

<details>
<summary>Indice 2 – Données à récupérer</summary>
Les paramètres `hourly=relative_humidity_2m,precipitation` permettent de récupérer les valeurs utiles.
</details>

<details>
<summary>Indice 3 – Logique de décision</summary>
Comptez le nombre d’heures avec humidité > 70 %.  
S’il dépasse 30 heures ou s’il pleut dans les 48 h, le risque est **élevé**.
</details>


---

## 🦌 Acte III : L'API Risque Faons (Biodiversité)

L’objectif de cette API est d’évaluer le **risque faunistique** lors des opérations de fauche, en particulier pour les **faons de chevreuil** cachés dans les herbes hautes.  
Cette estimation repose sur des **règles écologiques simplifiées**, basées sur la période de mise bas, le type de voisinage, et les conditions saisonnières.

---

### ⚙️ Données d’entrée
L’API recevra trois paramètres :
- `date_fauche` : date prévue de la fauche (format ISO : `AAAA-MM-JJ`)
- `type_voisinage` : type d’habitat autour de la parcelle (`foret`, `haie_bocagere`, `champ_ouvert`)
- `annee_froide` : booléen indiquant si l’hiver précédent était rigoureux (impacte le calendrier biologique)

---

### 🧠 Règles du modèle

#### 1. Période de Risque (Score de base)
| Niveau | Période | Score |
|---------|----------|--------|
| Faible | En dehors du 15 mai – 30 juin | 2 |
| Moyen | 15–31 mai **ou** 21–30 juin | 5 |
| Élevé | 1–20 juin | 8 |

#### 2. Voisinage (Multiplicateur)
| Type de voisinage | Multiplicateur |
|--------------------|----------------|
| Forêt | × 1.5 |
| Haie bocagère | × 1.3 |
| Champ ouvert | × 1.0 |

#### 3. Décalage Saisonnier
Si `annee_froide=True`, **toutes les bornes sont décalées de +7 jours**  
(les dates de mise bas sont retardées).

---

### 🧮 Calcul attendu
1. Ajuster les dates si `annee_froide=True`
2. Déterminer le score de base selon la période
3. Appliquer le multiplicateur de voisinage
4. Calculer `score_final = score_base × multiplicateur`
5. Limiter le score à un maximum de 10.0
6. Fournir le **conseil** selon la grille suivante :

| Score final | Niveau de risque | Conseil |
|--------------|------------------|----------|
| ≥ 7.0 | Élevé | Fauche à haut risque — utiliser un système d’effarouchement ou de balayage. |
| ≥ 4.0 | Modéré | Fauche à risque modéré — procéder avec vigilance. |
| < 4.0 | Faible | Fauche à risque faible — procéder normalement. |


-  💬 Exemple de sortie attendue

   ```json
      {
      "risque_faon_niveau": 9.5,
      "conseil_faune": "Fauche à haut risque - Utiliser un système d'effarouchement ou de balayage.",
      "justification": "Score de base (8) ajusté par le voisinage (1.5x). Décalage saisonnier : NON."
      }
   ```

---

## 4. Acte IV : L'API Mère de Décision (Le Synthétiseur)

Votre binôme (API Mère - B1) est responsable de l'API finale : celle qui prend la décision de faucher ou non.  
Cette API doit non seulement utiliser les données de ses "filles" (DDC, Météo, Faon) mais aussi intégrer une **nouvelle API externe** pour une donnée agronomique non-climatique.

### 🔹 Donnée Externe Supplémentaire : Le Sol

Pour enrichir la décision, vous allez intégrer une API externe du projet **ISRIC World Soil Information** pour obtenir la **texture du sol** (ex: sableux, limoneux, argileux) de la parcelle.

➡️ **Rôle de la donnée Sol :**  
Elle ne fait pas l'objet d'un veto, mais doit impérativement être **affichée dans la justification finale** pour apporter un contexte agronomique.

### 🔹 Logique de Décision Finale

L'API Mère doit prendre la décision selon les règles strictes suivantes (**Logique de Veto**) :

1. **Veto Météo :**  
   Si l'API Météo Séchage renvoie autre chose que `"Fauchage Recommandé"`, la décision est **NON (Risque Météo)**.  
2. **Veto Qualité/Maturité :**  
   Si l'API DDC renvoie un `statut_maturite` différent de `"ATTEINTE"`, la décision est **NON (Maturité non atteinte)**.  
3. **Veto Faune :**  
   Si l'API Risque Faons renvoie un `risque_faon_niveau` > 7.0, la décision est **NON (Risque Faune Élevé)**.  
4. **Décision OK :**  
   Si aucune de ces conditions n'est remplie, la décision est **OUI (Conditions Optimales)**.


   #### Exemple de Résultat attendu

   ```json
   {
      "decision_finale_fauche": "OUI",
      "justification": "Maturité atteinte, Météo OK, Risque Faune Faible. (Sol: Limon Franc)",
      "facteurs_cles": {
         "maturite_ddc": 655.2,
         "conseil_sechage": "Fauchage Recommandé",
         "risque_faon_niveau": 3.2,
         "type_sol": "Limon Franc"
      }
   }
   ```

## Conclusion & ressources pour aller plus loin



Félicitations ! Vous avez consommé une API et créé la vôtre en moins de 3 heures. Vous avez découvert les concepts de **route**, de **paramètres**, de **JSON** et vu comment des services peuvent communiquer entre eux.

* **Documentation de Flask :** [Welcome to Flask](https://flask.palletsprojects.com/)
* **Une liste d'APIs publiques amusantes :** [Public APIs](https://github.com/public-apis/public-apis)
