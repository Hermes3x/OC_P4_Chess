# ♟️ Chess Tournament Manager

Logiciel de gestion de tournois d'échecs (système suisse) en ligne de commande.

## 📝 Fonctionnalités

* **Gestion des tournois** : Création, sauvegarde et chargement automatique.
* **Base de données** : Gestion des joueurs via fichiers JSON.
* **Algorithme Suisse** : Génération automatique des paires pour chaque round sans redondance.
* **Rapports** : Génération de classements et listes de joueurs/tournois.

## ⚙️ Installation

**1. Cloner le dépôt :**
```bash
git clone https://github.com/Hermes3x/OC_P4_Chess.git
cd OC_P4_Chess
```

**2. Créer et activer l'environnement virtuel :**

Pour Windows :
```bash
python -m venv env
env\Scripts\activate
```

Pour Mac et Linux :
```bash
python3 -m venv env
source env/bin/activate
```

**3. Installer les dépendances :**
```bash
pip install -r requirements.txt
```

## 🚀 Exécution

Lancez le script principal à la racine du projet (assurez-vous que l'environnement virtuel est toujours activé) :

```bash
python main.py
```
*(Sur Mac/Linux, il se peut que vous deviez utiliser `python3 main.py`)*

## 🖥️ Aperçu du Menu Principal

Au démarrage, vous devriez voir l'affichage suivant :

```text
========================================
       ♟️  GESTIONNAIRE DE TOURNOI  ♟️
========================================
1. Créer un nouveau tournoi
2. Charger un tournoi existant
3. Accéder aux rapports
4. Quitter
----------------------------------------
Votre choix (1-4) :
```


## Générer un rapport Flake8 (HTML)

Ce projet utilise `flake8` et son extension `flake8-html` pour vérifier la qualité du code et le respect des conventions PEP 8. 

Pour générer un nouveau rapport, ouvrez votre terminal, placez-vous à la racine du projet et exécutez la commande suivante :

```bash
flake8 --format=html --htmldir=flake8_rapport
