# ♟️ Chess Tournament Manager

Logiciel de gestion de tournois d'échecs (système suisse) en ligne de commande.

## 📝 Fonctionnalités

* **Gestion des tournois** : Création, sauvegarde et chargement automatique.
* **Base de données** : Gestion des joueurs via fichiers JSON.
* **Algorithme Suisse** : Génération automatique des paires pour chaque round.
* **Rapports** : Génération de classements et listes de joueurs.

## ⚙️ Installation

1. **Cloner le dépôt** :
```bash
git clone https://github.com/Hermes3x/OC_P4_Chess.git

```


2. **Créer l'environnement virtuel** :
```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

```


3. **Installer les dépendances** :
```bash
pip install -r requirements.txt

```



## 🚀 Exécution

Lancez le script principal à la racine du projet :

```bash
python main.py

```

## 🖥️ Aperçu du Menu Principal

Au démarrage, vous devez voir l'affichage suivant :

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

---