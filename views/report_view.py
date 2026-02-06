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
                print(f"🏆 {tournament.name} - Lieu : {tournament.place}")
                print(f"   📅 Début : {tournament.date} | Fin : {tournament.end_date}")
                print("-----------------------------------")

        input("Appuyez sur Entrée pour revenir au menu...")

    def ask_specific_tounrmanent(self):
        return input("Saissez le nom du fichier à charger :")

    def specific_tournament_info(self, tournament):
        print(f"\n--- INFORMATIONS DU TOURNOI {tournament.name} ---")
        print(f"{tournament.name} - Date de début : {tournament.date} ")
        input("Appuyez sur Entrée pour revenir au menu...")

    def display_error(self, message):
        print(f"❌ ERREUR : {message}")
        input("Appuyer sur Entrée...")
