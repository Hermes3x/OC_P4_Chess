class TournamentView:
    def get_tournament_data(self):
        print("Veuillez renseigner les informations du tournoi")
        name = input("Nom du tournoi : ")
        place = input("Lieu : ")
        date = input("Date (jj/mm/aaaa) : ")
        rounds = 4  # on fixe à 4 pour coller à l’énoncé
        note = input("Note / description : ")

        return {"name": name,
                "place": place,
                "date": date,
                "round_qty": rounds,
                "note": note,
                }
    
    def display_error(self, message):
        print(f"❌ ERREUR : {message}")

    def display_nb_added_players(self, message):
        print(f"📊 {message}")

    def display_file_selection_menu(self, file_list, prompt_message="Choisissez un fichier :"):
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
                print("❌ Veuillez entrer un chiffre.")

    def choose_players_json(self):
        json_name = input("📂 Veuillez saisir le nom du fichier à charger pour sélectionner les joueurs : ")
        return json_name

    def choose_player_search_method(self):
        """Demande à l'utilisateur comment il veut chercher un joueur."""
        print("\n" + "="*40)
        print("♟️ SELECTION DE JOUEUR ♟️")
        print("="*40)
        print("1. Par ID exact (ex: AB12345)")
        print("2. Par nom complet (ex: Dupont Florent)")
        print("3. Par début de nom (ex: DU)")
        print("4. Ajouter un nouveau joueur")
        print("5. Annuler")
        print("-"*40)
        choice = input("Votre choix (1-4) : ").strip()
        return choice

    def select_player_id(self):
        print("Renseignez l'ID du joueur à ajouter au tournoi")
        return input("ID du joueur (ex: AB12345) : "
                     "\nPour terminer laissez vide et appuyez sur Entrée")
        
    def display_player_id_not_found(self, invalid_id):
        print(f"❌ Le joueur d'ID '{invalid_id}' est introuvable.")

    def select_player_name(self):
        print("Renseignez le nom complet du joueur à ajouter au tournoi")
        return input("Nom complet (ex: Dupont Florent)"
                     "\nPour terminer laissez vide et appuyez sur Entrée")

    def select_players_starting_with(self):
        print("Renseignez le début de nom (ex: DU)")
        return input("Le nom commence par :"
                     "\nPour terminer laissez vide et appuyez sur Entrée")

    def display_players_list_selection(self, players_name_start_list):
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
                print("❌ Vous devez entrer un chiffre.")

    def display_player_name_not_found(self, invalid_name):
        print(f"❌ Le joueur {invalid_name} est introuvable.")

    def display_player_added(self, player):
        print(f"✅ {player.first_name} {player.last_name} a été ajouté au tournoi.")

    def display_player_ever_added(self, invalid_player):
        print(f"Le joueur {invalid_player.first_name} {invalid_player.last_name} {invalid_player.national_chess_id} "
              f"est déjà inscrit au tournoi")

    def ask_add_player_manually(self):
        add_player = input("Souhaitez vous ajouter un joueur manuellement ? Y/n")

        return add_player

    def get_new_player_info(self):
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
        json_name = input("📂 Veuillez saisir le nom du fichier à charger : ")
        return json_name

    def display_tournament_creation(self, tournament):
        print(f"\n🚀 Tournoi {tournament.name} est créé avec "
              f"{len(tournament.tournament_players)} joueurs.")

    def display_tournament_loaded(self, tournament):
        print(f"✅ {tournament.name} chargé !")

    def display_round_matchs(self, round_obj):
        print(f"\n--- Matchs du round {round_obj.rounds_id} ---")
        for match in round_obj.matchs:
            print(f"{match}")
        print("-----------------------------------")

    def display_round_start(self, new_round):
        print(f"\n🔵 Lancement du Round {new_round.rounds_id}")

    def display_round_matchs_saving(self, new_round):
        print(f"✅ Round {new_round.rounds_id} terminé et sauvegardé.")

    def display_final_ranking(self, tournament_obj):
        print("\n--- 🏆 Classement final 🏆 ---")
        tournament_obj.tournament_players.sort(
            key=lambda p: (-tournament_obj.players_scores[p.national_chess_id],
                           p.last_name))
        for i, player in enumerate(tournament_obj.tournament_players, start=1):
            print(f"{i}. {player.first_name} {player.last_name} "
                  f"{tournament_obj.players_scores[player.national_chess_id]}"
                  f"pts")
    
    def display_tournament_end(self, tournament):
        print(f"\n🏆 LE TOURNOI {tournament.name} TERMINÉ ! 🏆")
