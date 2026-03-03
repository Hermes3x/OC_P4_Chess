import datetime


class TournamentView:
    """Gère l'interface utilisateur console pour la gestion des tournois."""

    # Dictionnaire pour les messages d'erreur
    ERROR_MESSAGES = {
        1: "\nAucun fichier de joueurs trouvé !",
        2: "\nFormat de date invalide",
        3: "\nImpossible d'ouvrir le fichier sélectionné ",
        4: "\nErreur lors de la sauvegarde",
        5: "\nÉlément introuvable",
        6: "\n❌ L'ID '{}' n'existe pas dans la base de données.",
        7: "\n❌ Le joueur {} est introuvable.",
        8: "\n❌ Le joueur {} est déjà inscrit au tournoi",
        9: "\n❌ Format de saisie invalide"
        }

    EVENT_MESSAGES = {
        1: "\nSauvegarde réussie !",
        2: "\n💾 Tournoi '{}' sauvegardé avec succès.",
        3: "\nhargement réussi : {} joueurs récupérés.",
        4: "\nTournoi '{}' chargé avec succès !",
        5: "\nLe tournoi est prêt. Début des rounds.",
        6: "\n📝 Nouveau tournoi détecté. Veuillez enregistrer les joueurs.",
        7: "\n✅ {} a été ajouté au tournoi.",
        8: "\n🚀 Tournoi {} est créé avec succès",
        9: "\n✅ Round {} terminé et sauvegardé."
    }

    # Dictionnaire pour les titres des menus de sélection de fichiers
    FILE_MENU_PROMPTS = {
        1: "\n📂 Veuillez choisir le fichier de joueurs à charger :",
        2: "\n📂 Veuillez choisir le tournoi à charger :",
        3: "\n📂 Pour charger le tournoi, veuillez d'abord sélectionner le fichier de joueurs de référence :"
    }

    def display_events(self, code, dynamic_data=""):
        """Affiche un message d'information ou de confirmation.
        Args:
            code (int): Clé du message dans EVENT_MESSAGES.
            dynamic_data (str, optionnel): Donnée à insérer dans le message (remplace '{}')"""

        # Récupération du message (avec fallback si code inconnu)
        raw_message = self.EVENT_MESSAGES.get(code, "Événement enregistré.")

        # Injection de la variable dynamique dans le message
        # Si la phrase n'a pas d'accolades, .format() ignore l'action sans planter.
        final_message = raw_message.format(dynamic_data)

        print(f"--- ✅ INFO : {final_message} ---")

    def display_error(self, code, dynamic_data=""):
        """Affiche un message d'erreur standardisé.
        Args:
            code (int): Clé du message dans ERROR_MESSAGES"""

        # Récupération de l'erreur (avec fallback si code inconnu)
        message = self.ERROR_MESSAGES.get(code, "Erreur inconnue")
        final_message = message.format(dynamic_data)
        print(f"--- ❌ ERREUR : {final_message} ---")

    def get_tournament_data(self):
        """Récupère les informations initiales pour créer un tournoi.
        Returns:
            dict: Les données saisies par l'utilisateur (nom, lieu, date, etc.)"""

        print("Veuillez renseigner les informations du tournoi")
        name = input("Nom du tournoi : ")
        place = input("Lieu : ")
        date = self.get_valid_date("Date (jj/mm/aaaa) : ")

        # Le nombre de rounds est fixé à 4 par défaut selon le cahier des charges
        rounds = 4
        note = input("Note / description : ")

        return {"name": name,
                "place": place,
                "date": date,
                "round_qty": rounds,
                "note": note,
                }

    def get_valid_date(self, prompt):
        """Demande une date à l'utilisateur jusqu'à ce que le format soit valide.
        Args:
            prompt (str): Le message affiché lors de la saisie (input)
        Returns:
            str: La date valide au format jj/mm/aaaa"""

        while True:
            # .strip() évite que des espaces accidentels ne fassent planter la validation
            date_saisie = input(prompt).strip()
            try:
                # Vérifie que la chaîne correspond exactement au format jj/mm/aaaa
                datetime.datetime.strptime(date_saisie, "%d/%m/%Y")
                return date_saisie
            except ValueError:
                self.display_error(2, date_saisie)

    def display_tournament_header(self, tournament_name):
        """Affiche le titre principal du menu de gestion d'un tournoi.
        Args:
            tournament_name (str): Le nom du tournoi en cours"""
        print(f"\n--- ♟️ GESTION : {tournament_name} ---")

    def display_registration_in_progress(self, current_count, max_players):
        """Affiche le ratio de remplissage du tournoi pendant l'inscription."""
        print(f"\nℹ️ Inscription en cours... ({current_count}/{max_players})")

    def display_registration_status(self, current_count, max_players):
        """Rappelle le nombre de joueurs actuellement inscrits."""
        print(f"Nombre de joueurs inscrits : {current_count} / {max_players}")

    def display_registration_paused(self):
        """Notifie que le tournoi n'est pas plein et retourne au menu principal."""
        print("\n⚠️ Inscription mise en pause. Retour au menu principal...")

    def display_tournament_ready(self, actual_round, rounds_qty):
        """"Confirme que le tournoi a ses 8 joueurs et est prêt à être joué."""
        print(f"✅ Tournoi prêt ! Round : {actual_round} / {rounds_qty}")

    def display_tournament_play_menu(self):
        """Affiche le sous-menu de gestion d'un tournoi actif."""
        print("1. Jouer le prochain round")
        print("2. Voir le classement provisoire")
        print("3. Quitter et revenir au menu principal")

    def display_file_selection_menu(self, file_list, prompt_code=1):
        """Affiche une liste de fichiers numérotée et gère la sélection de l'utilisateur.
        Args:
            file_list (list): Liste des noms de fichiers à afficher.
            prompt_code (int): Clé du dictionnaire FILE_MENU_PROMPTS. Par défaut 1 (joueurs).
        Returns:
            str ou None: Le nom du fichier choisi, ou None si annulation/erreur"""
        prompt_message = self.FILE_MENU_PROMPTS.get(prompt_code, "Choisissez un fichier :")

        print(f"{prompt_message}")

        # enumerate(..., start=1) permet d'afficher une liste commençant par 1 au lieu de 0
        for i, filename in enumerate(file_list, start=1):
            print(f"{i} - {filename}")

        print("0 - Annuler")

        while True:
            user_input = input("Votre choix (numéro) : ").strip()

            # Gestion de l'annulation rapide
            if user_input == "0" or not user_input:
                return None

            try:
                choice = int(user_input)
                if 1 <= choice <= len(file_list):
                    # choice - 1 : adapte la saisie utilisateur à l'index de la liste Python
                    return file_list[choice - 1]

                self.display_error(5)
            except ValueError:
                self.display_error(6)

    def choose_player_search_method(self):
        """Affiche les options pour ajouter un joueur au tournoi.
        Returns:
            str: Le numéro de l'option choisie par l'utilisateur"""
        print("\n" + "="*40)
        print("♟️ SELECTION DE JOUEUR ♟️")
        print("="*40)
        print("1. Par ID exact (ex: AB12345)")
        print("2. Par nom complet (ex: Dupont Florent)")
        print("3. Par début de nom (ex: DU)")
        print("4. Ajouter un nouveau joueur")
        print("5. Annuler")
        print("-"*40)
        return input("Votre choix (1-4) : ").strip()

    def get_match_score(self, match):
        """Demande la saisie du résultat pour un match spécifique.
        Args:
            match (Match): Objet contenant le tuple (Joueur1, Joueur2).
        Returns:
            tuple: (Joueur gagnant ou None si égalité, score à attribuer)"""
        p1 = match.players_pair[0]
        p2 = match.players_pair[1]

        print(f"Saisie du score : {p1.first_name} {p1.last_name} ({p1.national_chess_id}) vs "
              f"{p2.first_name} {p2.last_name} ({p2.national_chess_id})")
        print("1 : Victoire J1 | 2 : Victoire J2 | 0 : Match nul")

        while True:
            choice = input("Résultat (1, 2 ou 0) : ").strip()
            if choice == "1":
                return p1, 1.0
            elif choice == "2":
                return p2, 0.0
            elif choice == "0":
                return None, 0.5
            else:
                print("❌ Choix invalide.")

    def select_player_id(self):
        """Demande la saisie d'un ID National pour la recherche de joueur."""
        return input("Renseignez l'ID du joueur à ajouter au tournoi (ex: AB12345) : "
                     "\nPour terminer laissez vide et appuyez sur Entrée")

    def select_player_name(self):
        """Demande la saisie du nom complet pour la recherche de joueur."""
        return input("Renseignez le nom complet du joueur à ajouter au tournoi (ex: Dupont Florent)"
                     "\nPour terminer laissez vide et appuyez sur Entrée")

    def select_players_starting_with(self):
        """Demande la saisie des premières lettres pour la recherche partielle de joueur."""
        return input("Renseignez le début de nom (ex: DU) :"
                     "\nPour terminer laissez vide et appuyez sur Entrée")

    def display_players_list_selection(self, players_name_start_list):
        """Affiche les résultats d'une recherche filtrée pour forcer un choix unique.
        Args:
            players_name_start_list (list): Liste des objets Player correspondant à la recherche.
        Returns:
            int: L'index (base 0) du joueur sélectionné dans la liste"""
        print(f"🔎 {len(players_name_start_list)} joueurs trouvés :")
        for i, player in enumerate(players_name_start_list, start=1):
            print(f"{i} - {player.first_name} {player.last_name}")
        while True:
            try:
                choosen_player = int(input("Sélectionnez le numéro du joueur à ajouter au tournoi :")) - 1
                if choosen_player in range(len(players_name_start_list)):
                    return choosen_player
                print("❌ Numéro invalide, réessayez.")
            except ValueError:
                print("❌ Veuillez entrer un chiffre.")

    def get_new_player_info(self):
        """"Demande les informations nécessaires à la création manuelle d'un joueur.
        Returns:
            dict: Les attributs du nouveau joueur saisis par l'utilisateur"""
        print("---Ajout d'un nouveau joueur---")
        first_name = input("Prénom :")
        last_name = input("Nom :")
        birth_date = input("Date de naissance : ")
        chess_id = input("ID Chess (AB12345) : ")
        return {
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "national_chess_id": chess_id
            }

    def display_tournament_creation(self, tournament):
        """Confirme l'instanciation initiale d'un nouveau tournoi."""
        print(f"\n🚀 Tournoi {tournament.name} est créé avec "
              f"{len(tournament.tournament_players)} joueurs.")

    def display_round_matchs(self, round_obj):
        """Affiche l'ensemble des paires de joueurs pour un tour donné."""
        print(f"\n--- Matchs du round {round_obj.rounds_id} ---")
        for match in round_obj.matchs:
            print(f"⚔️ {match}")
        print("-" * 40)

    def display_round_start(self, new_round):
        """Annonce l'ouverture d'un nouveau round."""
        print(f"\n🔵 Lancement du Round {new_round.rounds_id}")

    def display_final_ranking(self, tournament_obj):
        """Affiche le classement final du tournoi trié par points et par nom."""
        print("\n--- 🏆 Classement 🏆 ---")

        # Le lambda trie d'abord par score décroissant (-players_scores),
        # puis par ordre alphabétique (last_name) en cas d'égalité.
        tournament_obj.tournament_players.sort(
            key=lambda p: (-tournament_obj.players_scores[p.national_chess_id],
                           p.last_name))
        for i, player in enumerate(tournament_obj.tournament_players, start=1):
            print(f"{i}. {player.first_name} {player.last_name} "
                  f"{tournament_obj.players_scores[player.national_chess_id]}"
                  f"pts")

    def display_tournament_end(self, tournament):
        """Annonce visuellement la clôture définitive du tournoi."""
        print(f"\n🏆 🏁 LE TOURNOI {tournament.name} TERMINÉ ! 🏁 🏆")
