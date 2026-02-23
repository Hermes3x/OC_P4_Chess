from views.report_view import ReportView


class ReportController:

    def __init__(self, db_controller_instance):
        self.view = ReportView()
        self.db_controller = db_controller_instance

    def run(self):
        while True:
            choice = self.view.display_rapport_choice()

            if choice == "1":
                self.all_players_alphabetic_sort()
            elif choice == "2":
                self.all_tournaments()
            elif choice == "3":
                self.specific_tounament()
            elif choice == "4":
                self.tournament_players()
            elif choice == "5":
                self.matchs_and_rounds()
            elif choice == "6":
                # On quitte la boucle du rapport pour revenir au MainController
                break
            else:
                print("Choix invalide, veuillez réessayer.")

    def all_players_alphabetic_sort(self):
        """vérifie / demande : charger un fichier"""
        available_files = self.db_controller.get_available_players_files()

        if not available_files:
            self.view.display_error("Aucun fichier de joueurs trouvé dans data/players !")
            return

        chosen_filename = self.view.display_file_selection_menu(available_files, "Fichiers de joueurs disponibles : ")

        if not chosen_filename:
            return

        self.db_controller.set_players_file(chosen_filename)

        players = self.db_controller.load_players_from_json()
        sorted_players = sorted(players, key=lambda p: p.last_name)
        self.view.display_players_sorted_list(sorted_players)

    def all_tournaments(self):
        tournaments_list = self.db_controller.load_all_tournaments()
        self.view.display_tournaments_list(tournaments_list)

    def specific_tounament(self):
        available_files = self.db_controller.get_available_tournaments_files()

        if not available_files:
            return

        chosen_filename = self.view.display_file_selection_menu(available_files)

        if not chosen_filename:
            return

        full_path = f"data/tournaments/{chosen_filename}"
        tournament_obj = self.db_controller.load_tournament(full_path)

        if tournament_obj:
            self.view.specific_tournament_info(tournament_obj)
        else:
            self.view.display_error("Tournoi introuvable ou fichier corrompu.")

    def tournament_players(self):

        if not self.db_controller.players_file:
            available_players = self.db_controller.get_available_players_files()

            if not available_players:
                self.view.display_error("Aucun fichier joueurs disponible")
                return

            chosen_players_filename = self.view.display_file_selection_menu(available_players,
                                                                            "Fichiers de joueurs disponibles : ")

            if not chosen_players_filename:
                return

            self.db_controller.set_players_file(chosen_players_filename)

        available_tournaments_files = self.db_controller.get_available_tournaments_files()

        if not available_tournaments_files:
            self.view.display_error("Aucun tournoi trouvé.")
            return

        chosen_tournament_filename = self.view.display_file_selection_menu(available_tournaments_files)

        if not chosen_tournament_filename:
            return

        tournament_full_path = f"data/tournaments/{chosen_tournament_filename}"
        tournament = self.db_controller.load_tournament(tournament_full_path)

        if tournament:
            players = tournament.tournament_players
            sorted_players = sorted(players, key=lambda p: p.last_name.lower())
            self.view.display_tournament_players(tournament, sorted_players)

        else:
            self.view.display_error("Erreur de chargement du tournoi.")

    def matchs_and_rounds(self):
        if not self.db_controller.players_file:
            available_players = self.db_controller.get_available_players_files()

            if not available_players:
                self.view.display_error("Aucun fichier joueurs disponible")
                return

            chosen_players_filename = self.view.display_file_selection_menu(available_players,
                                                                            "Fichiers de joueurs disponibles : ")

            if not chosen_players_filename:
                return

            self.db_controller.set_players_file(chosen_players_filename)

        available_tournament_files = self.db_controller.get_available_tournaments_files()
        if not available_tournament_files:
            self.view.display_error("Aucun fichier trouvé")

        user_choice = self.view.display_file_selection_menu(available_tournament_files)

        if not user_choice:
            return

        full_path = f"data/tournaments/{user_choice}"
        selected_tournament = self.db_controller.load_tournament(full_path)

        if not selected_tournament:
            self.view.display_error("Erreur de chargement du tournoi.")
            return

        self.view.display_tournament_rounds_and_matchs(selected_tournament)
