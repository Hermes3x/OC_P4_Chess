import datetime


class TournamentView:
    """Gère l'interface utilisateur console pour la gestion des tournois."""

    def get_tournament_data(self):
        """Récupère les informations de base pour la création d'un tournoi."""
        print("Veuillez renseigner les informations du tournoi")
        name = input("Nom du tournoi : ")
        place = input("Lieu : ")
        date = self.get_valid_date("Date (jj/mm/aaaa) : ")
        rounds = 4  # Fixé à 4 selon les spécifications métier
        note = input("Note / description : ")

        return {"name": name,
                "place": place,
                "date": date,
                "round_qty": rounds,
                "note": note,
                }

    def get_valid_date(self, prompt):
        """Boucle de saisie jusqu'à obtenir une date valide au format jj/mm/aaaa."""
        while True:
            date_saisie = input(prompt).strip()
            try:
                datetime.datetime.strptime(date_saisie, "%d/%m/%Y")
                return date_saisie
            except ValueError:
                self.display_error(f"❌Format de {date_saisie} invalide")

    def display_events(self, message):
        """Affiche un message d'événement général."""
        print(f"\n📢 {message}")

    def display_tournament_menu(self, message):
        """Affiche l'en-tête du menu du tournoi."""
        print(f"\n{message}")

    def display_error(self, message):
        """Affiche un message d'erreur formaté."""
        print(f"❌ ERREUR : {message}")

    def display_nb_added_players(self, message):
        """Affiche l'état d'avancement du remplissage des joueurs (ex: 3/8)."""
        print(f"📊 {message}")

    def display_file_selection_menu(self, file_list, prompt_message="Choisissez un fichier :"):
        """Affiche une liste de fichiers JSON et retourne le fichier sélectionné."""
        print(prompt_message)
        for i, filename in enumerate(file_list, start=1):
            print(f"{i} - {filename}")

        print("0 - Annuler")

        while True:
            user_input = input("Votre choix (numéro) : ").strip()

            if user_input == "0" or not user_input:
                return None

            try:
                choice = int(user_input)
                if 1 <= choice <= len(file_list):
                    return file_list[choice - 1]
                print("❌ Numéro invalide.")
            except ValueError:
                print("❌ Entrée invalide : veuillez saisir un chiffre.")

    def choose_player_search_method(self):
        """Affiche le menu de sélection de la méthode de recherche d'un joueur."""
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
        """Demande les résultats du match à l'utilisateur via les index du tuple."""
        p1 = match.players_pair[0]
        p2 = match.players_pair[1]

        print(f"\nSaisie du score : {p1.last_name} vs {p2.last_name}")
        print("1 : Victoire J1 | 2 : Victoire J2 | 0 : Match nul")

        while True:
            choice = input("Résultat (1, 2 ou 0) : ").strip()
            if choice == "1":
                return p1, 1.0  # On retourne le joueur gagnant pour la méthode match.score()
            elif choice == "2":
                return p2, 0.0  # On retourne le joueur gagnant
            elif choice == "0":
                return None, 0.5  # None signifie match nul pour ta méthode match.score()
            else:
                print("❌ Choix invalide.")

    def select_player_id(self):
        """Invite à saisir un identifiant national d'échecs."""
        print("Renseignez l'ID du joueur à ajouter au tournoi")
        return input("ID du joueur (ex: AB12345) : "
                     "\nPour terminer laissez vide et appuyez sur Entrée")

    def display_player_id_not_found(self, invalid_id):
        """Signale qu'aucun joueur ne possède cet ID dans la base."""
        print(f"❌ L'ID '{invalid_id}' n'existe pas dans la base de données.")

    def select_player_name(self):
        """Invite à saisir le nom complet d'un joueur."""
        print("Renseignez le nom complet du joueur à ajouter au tournoi")
        return input("Nom complet (ex: Dupont Florent)"
                     "\nPour terminer laissez vide et appuyez sur Entrée")

    def select_players_starting_with(self):
        """Invite à saisir les premières lettres d'un nom."""
        print("Renseignez le début de nom (ex: DU)")
        return input("Le nom commence par :"
                     "\nPour terminer laissez vide et appuyez sur Entrée")

    def display_players_list_selection(self, players_name_start_list):
        """Affiche les résultats d'une recherche filtrée et retourne l'index choisi."""
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

    def display_player_name_not_found(self, invalid_name):
        """Signale que le joueur n'a pas été trouvé"""
        print(f"❌ Le joueur {invalid_name} est introuvable.")

    def display_player_added(self, player):
        """Confirme l'ajout réussi d'un joueur au tournoi."""
        print(f"✅ {player.first_name} {player.last_name} a été ajouté au tournoi.")

    def display_player_ever_added(self, invalid_player):
        """Signale qu'un joueur est déjà présent dans la liste des participants."""
        print(f"❌ Le joueur {invalid_player.first_name} {invalid_player.last_name} {invalid_player.national_chess_id} "
              f"est déjà inscrit au tournoi")

    def get_new_player_info(self):
        """Formulaire de création manuelle d'un nouveau joueur."""
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

    def choose_tournament_json(self):
        """Affiche la liste des fichiers tournoi disponibles."""
        json_name = input("📂 Veuillez saisir le nom du fichier à charger : ")
        return json_name

    def display_tournament_creation(self, tournament):
        """Affiche la confirmation de création du tournoi."""
        print(f"\n🚀 Tournoi {tournament.name} est créé avec "
              f"{len(tournament.tournament_players)} joueurs.")

    def display_tournament_loaded(self, tournament):
        """Confirme le chargement d'un tournoi depuis un fichier."""
        print(f"✅ {tournament.name} chargé !")

    def display_round_matchs(self, round_obj):
        """Affiche la liste des matchs générés pour un tour spécifique."""
        print(f"\n--- Matchs du round {round_obj.rounds_id} ---")
        for match in round_obj.matchs:
            print(f"⚔️ {match}")
        print("-" * 40)

    def display_round_start(self, new_round):
        """Annonce le début d'un nouveau tour."""
        print(f"\n🔵 Lancement du Round {new_round.rounds_id}")

    def display_round_matchs_saving(self, new_round):
        """Confirme la clôture et la sauvegarde d'un round."""
        print(f"✅ Round {new_round.rounds_id} terminé et sauvegardé.")

    def display_final_ranking(self, tournament_obj):
        """Affiche le tableau final des scores trié par points."""
        print("\n--- 🏆 Classement final 🏆 ---")
        tournament_obj.tournament_players.sort(
            key=lambda p: (-tournament_obj.players_scores[p.national_chess_id],
                           p.last_name))
        for i, player in enumerate(tournament_obj.tournament_players, start=1):
            print(f"{i}. {player.first_name} {player.last_name} "
                  f"{tournament_obj.players_scores[player.national_chess_id]}"
                  f"pts")

    def display_tournament_end(self, tournament):
        """Affiche le message de fin de tournoi."""
        print(f"\n🏆 🏁 LE TOURNOI {tournament.name} TERMINÉ ! 🏁 🏆")
