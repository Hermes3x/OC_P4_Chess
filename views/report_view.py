class ReportView:
    def display_rapport_choice(self):
        print("\n--- 📊 MENU RAPPORTS 📊 ---")
        print("1 - Liste de tous les joueurs (alphabétique)")
        print("2 - Liste de tous les tournois")
        print("3 - Nom et dates d’un tournoi donné")
        print("4 - Liste des joueurs d'un tournoi (alphabétique)")
        print("5 - Liste tours/matchs d'un tournoi")
        print("6 - Retour menu principal")  # Toujours utile !

        return input("Veuillez choisir le rapport à éditer : ")

    def display_tournament_rounds_and_matchs(self, tournament):
        print(f"\n--- ⚔️ MATCHS & ROUNDS : {tournament.name} ---")

        if not tournament.rounds_list:
            print("Aucun round joué pour le moment.")
            input("Appuyez sur Entrée...")
            return

        for round_obj in tournament.rounds_list:
            print(f"\n🔵 Round {round_obj.rounds_id}")

            print(f"   Début : {round_obj.start_date} | Fin : {round_obj.end_date}")

            for match in round_obj.matchs:
                p1, p2 = match.players_pair
                s1, s2 = match.player1_score, match.player2_score
                print(f"   🔸 {p1.last_name} {p1.national_chess_id} ({s1}) vs {p2.last_name} {p2.national_chess_id} ({s2})")
            
        print("\n-------------------------------------------")
        input("Appuyez sur Entrée pour revenir au menu...")

    def display_file_selection_menu(self, file_list, prompt_message="Choisissez un fichier :"):
        print(prompt_message)
        for i, filename in enumerate(file_list, start=1):
            print(f"{i} - {filename}")

        print("0 - Annuler")

        while True:
            user_input = input("Votre choix (numéro) : ").strip()

            if user_input == "0":
                return None
            
            try:
                choice = int(user_input)
                if 1 <= choice <= len(file_list):
                    return file_list[choice - 1]
                print("❌ Numéro invalide.")
            except ValueError:
                print("❌ Veuillez entrer un chiffre.")

    def display_players_sorted_list(self, players_sorted_list):
        print("\n--- LISTE DES JOUEURS (Tri Alphabétique) ---")
        for player in players_sorted_list:
            print(f"{player.last_name} {player.first_name} - ID National : {player.national_chess_id}")

        print("\n-------------------------------------------")
        input("Appuyez sur Entrée pour revenir au menu...")

    def display_tournaments_list(self, tournaments_list):
        print("\n--- LISTE DE TOUS LES TOURNOIS ---")

        if not tournaments_list:
            print("Aucun tournoi trouvé")
        else:
            for tournament in tournaments_list:
                print(f"🏆 {tournament.date} - {tournament.name} - Lieu : {tournament.place}"
                      f"{tournament.note}")
                print(f"   📅 Début : {tournament.date} | Fin : {tournament.end_date}")
                print("-----------------------------------")

        input("Appuyez sur Entrée pour revenir au menu...")

    def specific_tournament_info(self, tournament):
        print(f"\n--- INFORMATIONS DU TOURNOI {tournament.name} ---")
        print(f"{tournament.name} - Date de début : {tournament.date} ")
        input("Appuyez sur Entrée pour revenir au menu...")

    def display_error(self, message):
        print(f"❌ ERREUR : {message}")
        input("Appuyer sur Entrée...")

    def display_tournament_players(self, tournament, sorted_tournament_players):
        print(f"\n--- LISTE DES JOUEURS (Tri Alphabétique) DU TOURNOI : ---"
              f"\n--- {tournament.name} {tournament.date} {tournament.place}")

        for player in sorted_tournament_players:
            print(f"- {player.last_name} {player.first_name} {player.national_chess_id}")
