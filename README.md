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

Votre binôme (API Fille 1) doit développer l'API qui détermine la **maturité** du foin. Pour cela, vous allez calculer les **Degrés-Jours Cumulés (DDC)**, une mesure thermique du développement des plantes.

$$\text{DDC} = \sum (\text{Température Moyenne} - \text{Température de Base})$$

Pour les graminées de foin, la **Température de Base ($T_b$)** est souvent fixée à $\mathbf{6^{\circ}C}$.

**Votre mission :** Modifier le script `degres_jours.py` pour consommer l'API **Open-Meteo Archive** (données historiques) et calculer le DDC entre le **1er mars** de l'année en cours et la date du jour.

### Exercice 1 : Construire et Consommer la Requête Historique 

1.  Ouvrez le fichier `degres_jours.py`.
2.  **Recherchez la documentation Open-Meteo :** Trouvez l'**URL** de l'API dédiée aux **données historiques** (l'URL par défaut est pour les prévisions) et les **paramètres** nécessaires pour obtenir les températures moyennes journalières (`daily`).
3.  **Votre mission :** Complétez la variable `URL_HISTORIQUE` et le dictionnaire `params` dans `degres_jours.py`. Les paramètres doivent inclure :
    * Les **températures moyennes journalières**.
    * Les dates de début et de fin.
    * La latitude, la longitude et le fuseau horaire.
4.  Exécutez le script : `python degres_jours.py`.

### Exercice 2 : Calculer le DDC et Afficher la Maturité 

1.  Ouvrez `degres_jours.py` et trouvez la section `TODO: Calcul du DDC`.
2.  **Inspectez la réponse JSON :** À partir du `data` (la réponse JSON), trouvez la **clé exacte** qui contient la liste des températures moyennes.
3.  **Implémentez la logique de DDC :**
    * Initialisez `DDC_cumule = 0`.
    * Pour chaque température (`T_moyenne`) :
        * Calculez le Degré-Jour du jour en appliquant la formule
        * Ajoutez cette valeur au `DDC_cumule`.
4.  Affichez le DDC final et le conseil de maturité.
L'API mère attend une réponse au format JSON qui indique clairement l'état de maturité :

```json
{
  "statut_maturite": "ATTEINTE",
  "ddc_cumule": 650.45,
  "seuil_maturite": 600
}
```

<details>
<summary>💡 Indice 1 (URL et Paramètre)</summary>
L'API d'archive est sur le sous-domaine `archive-api`. Le paramètre pour les températures moyennes journalières se trouve dans la section `daily`.
</details>

<details>
<summary>💡 Indice 2 (Clé de la donnée)</summary>
La clé pour les températures moyennes est `temperature_2m_mean`.
</details>

<details>
<summary>💡 Indice 3 (Formule Python)</summary>
Vous pouvez utiliser la fonction native `max(a, b)` pour implémenter la partie $\max(0, ...)$ de la formule.
</details>

---

## 2. Acte II : L'API Météo Séchage (Logistique)

Votre binôme (API Fille 2) est responsable de l'évaluation du **risque logistique** lié à la météo. L'objectif est de s'assurer que, si l'on fauche aujourd'hui, les **48 prochaines heures** permettront au foin de sécher correctement sans être mouillé, ce qui dégraderait sa qualité (perte d'éléments nutritifs, risque de moisissure).

**Votre mission :** Modifier le script `meteo_sechage.py` pour consommer l'API **Open-Meteo Prévisions** (données futures) et évaluer le risque de pluie et l'efficacité du séchage sur les 48 heures à venir.

#### Exercice 3 : Construire la Requête de Prévisions 

1.  Ouvrez le fichier `meteo_sechage.py`.
2.  **Recherchez la documentation Open-Meteo :** Trouvez l'**URL** de l'API dédiée aux **prévisions** (l'URL par défaut pour le futur) et les **paramètres** nécessaires pour obtenir les prévisions **horaires** sur les 48 prochaines heures.
3.  **Votre mission :** Complétez la variable `URL_PREVISIONS` et le dictionnaire `params` dans `meteo_sechage.py`. Les paramètres doivent inclure :
    * Les prévisions **horaires** pour les **précipitations** (cumul de pluie) et l'**humidité relative de l'air**.
    * La durée : **48 heures**.
    * La latitude, la longitude et le fuseau horaire.
4.  Exécutez le script : `python meteo_sechage.py`.

#### Exercice 4 : Calculer le Risque de Séchage 

1.  Ouvrez `meteo_sechage.py` et trouvez la section `TODO: Calcul du Risque`.
2.  **Inspectez la réponse JSON :** Trouvez les **clés exactes** des données horaires : les **précipitations** (en mm) et l'**humidité relative de l'air** (en %).
3.  Règle de Décision Agronomique

La décision doit être prise selon la hiérarchie de risque suivante :

1.  **Priorité 1 (Pluie) :** S'il y a **une seule heure** avec une précipitation $> 0.1 \text{ mm}$ sur les 48h, le fauchage est **À Éviter (Raison : Pluie)**.
2.  **Priorité 2 (Séchage Lent) :** S'il y a **plus de 30 heures** avec une humidité relative de l'air supérieure à $70\%$ sur les 48h, le fauchage est **À Éviter (Raison : Séchage lent)**.
3.  **OK :** Sinon (aucune des conditions ci-dessus n'est remplie), le fauchage est **Fauchage Recommandé**.
4.  Affichez la conclusion : **Fauchage Recommandé** ou **À Éviter (Raison : Pluie / Séchage lent)**.
```json
{
  "conseil_sechage": "Fauchage Recommandé",
  "justification": "Moins de 30h de forte humidité et aucune pluie prévue."
}
```

<details>
<summary>💡 Indice 1 (URL et Paramètres)</summary>
L'URL de base pour les prévisions est `https://api.open-meteo.com/v1/forecast`. Vous devrez utiliser le paramètre `hourly` et la limite de temps `forecast_days=2`.
</details>

<details>
<summary>💡 Indice 2 (Clés de la donnée)</summary>
Les clés pour les données horaires sont `rain` ou `precipitation` et `relative_humidity_2m`.
</details>

<details>
<summary>💡 Indice 3 (Logique Python)</summary>
Vous pouvez utiliser une boucle `for` simple et des compteurs pour évaluer le nombre d'heures concernées par un risque.
</details>


---

## 3. Acte III : L'API Risque Faons (Biodiversité)

Votre binôme (API Fille 3, pour le groupe de 4 binômes) est chargé d'évaluer le **risque faunistique**. La fauche est une cause majeure de mortalité des faons de chevreuil qui se cachent dans les hautes herbes au printemps.

Ce modèle utilise des données **simulées** basées sur des critères **écologiques** pour créer un score de risque pondéré.

#### Règle de Modélisation du Risque Faons

L'API doit calculer un **score de risque final sur une échelle de 1 à 10** en combinant trois critères :

1.  **Période de Risque (Base) :** La période de mise bas des faons est la plus critique.
    * **Niveau 1 (Faible) :** En dehors de la période critique. (Score de base : 2)
    * **Niveau 2 (Moyen) :** Début ou fin de période (ex: 15-31 mai / 21-30 juin). (Score de base : 5)
    * **Niveau 3 (Élevé) :** Pleine période de mise bas (ex: 1er-20 juin). (Score de base : 8)
2.  **Voisinage (Multiplicateur) :** La proximité d'un habitat augmente le risque.
    * Parcelle bordée de **Forêt / Haies** : Multiplieur **x 1.5**
    * **Champ ouvert** : Multiplieur **x 1.0**
3.  **Décalage Saisonnier (Ajustement) :** Une année froide décale la mise bas.
    * Si **Année précédente froide** (simulé par `annee_froide=True`) : Décalage de **+ 7 jours** pour toutes les bornes de la Période de Risque.


L'API mère attend un score et un conseil précis :

```json
{
  "risque_faon_niveau": 9.5, // Score de 1 à 10
  "conseil_faune": "Fauche à haut risque - Utiliser un système d'effarouchement",
  "justification": "Pleine période de risque (8) multiplié par la proximité de la forêt (x1.5)."
}
```

---

---

## 4. Acte IV : L'API Mère de Décision (Le Synthétiseur)

Votre binôme (API Mère - B1) est responsable de l'API finale : celle qui prend la décision de faucher ou non. Cette API doit non seulement utiliser les données de ses "filles" (DDC, Météo, Faon) mais aussi intégrer une **nouvelle API externe** pour une donnée agronomique non-climatique.

#### Donnée Externe Supplémentaire : Le Sol

Pour enrichir la décision, vous allez intégrer une API externe du projet **ISRIC World Soil Information** pour obtenir la **texture du sol** (ex: sableux, limoneux, argileux) de la parcelle.

**Rôle de la donnée Sol :** Elle ne fait pas l'objet d'un Veto dans ce TP, mais elle doit impérativement être affichée dans le **résultat final** pour apporter un contexte agronomique et une justification complète.

#### Logique de Décision Finale

L'API Mère doit prendre la décision selon les règles strictes suivantes (Logique de Veto) :

1.  **Veto Météo :** Si l'API Météo Séchage renvoie **différent** de **"Fauchage Recommandé"** (c'est-à-dire Pluie ou Séchage Lent), la décision finale est **NON (Risque Météo)**.
2.  **Veto Qualité/Maturité :** Si l'API DDC renvoie un `statut_maturite` **différent** de **"ATTEINTE"**, la décision finale est **NON (Maturité non atteinte)**.
3.  **Veto Faune :** Si l'API Risque Faons renvoie un `risque_faon_niveau` **$> 7.0$**, la décision finale est **NON (Risque Faune Élevé)**.
4.  **Décision OK :** Si aucune des conditions de Veto n'est remplie, la décision finale est **OUI (Conditions Optimales)**.

#### Contrat JSON de l'API Mère

Cette API est la réponse finale au client. Elle doit indiquer la décision et résumer les facteurs considérés. **Notez l'inclusion du `type_sol` dans la justification et les facteurs.**

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
* **Documentation de Requests :** [Requests Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/)
* **Une liste d'APIs publiques amusantes :** [Public APIs](https://github.com/public-apis/public-apis)
