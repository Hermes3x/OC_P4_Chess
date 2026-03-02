from views.report_view import ReportView


class ReportController:
    """Contrôleur dédié à la gestion et à l'affichage des rapports."""

    def __init__(self, db_controller_instance):
        """Initialise le contrôleur avec sa propre vue et l'accès à la base de données."""
        self.view = ReportView()
        self.db_controller = db_controller_instance

    def run(self):
        """Boucle principale du menu des rapports.

        Affiche le menu de choix, récupère l'entrée utilisateur depuis la vue,
        et redirige vers la méthode de traitement appropriée.
        """
        while True:
            choice = self.view.display_rapport_choice()

            if choice == "1":
                self.all_players_alphabetic_sort()
            elif choice == "2":
                self.all_tournaments()
            elif choice == "3":
                self.specific_tournament()
            elif choice == "4":
                self.tournament_players()
            elif choice == "5":
                self.matchs_and_rounds()
            elif choice == "6":
                break
            else:
                self.view.display_error(5)

    def all_players_alphabetic_sort(self):
        """Gère l'affichage de tous les joueurs d'un fichier par ordre alphabétique."""
        available_files = self.db_controller.get_available_players_files()

        if not available_files:
            self.view.display_error(1)
            return

        chosen_filename = self.view.display_file_selection_menu(available_files, 1)

        if not chosen_filename:
            return

        self.db_controller.set_players_file(chosen_filename)

        players = self.db_controller.load_players_from_json()
        sorted_players = sorted(players, key=lambda p: p.last_name)
        self.view.display_players_sorted_list(sorted_players)

    def all_tournaments(self):
        """Gère l'affichage de la liste complète de tous les tournois enregistrés."""
        tournaments_list = self.db_controller.load_all_tournaments()
        self.view.display_tournaments_list(tournaments_list)

    def specific_tournament(self):
        """Demande la sélection d'un tournoi précis et affiche ses informations générales."""
        available_files = self.db_controller.get_available_tournaments_files()

        if not available_files:
            return

        chosen_filename = self.view.display_file_selection_menu(available_files, 2)

        if not chosen_filename:
            return

        full_path = f"data/tournaments/{chosen_filename}"
        tournament_obj = self.db_controller.load_tournament(full_path)

        if tournament_obj:
            self.view.specific_tournament_info(tournament_obj)
        else:
            self.view.display_error(2)

    def tournament_players(self):
        """Affiche les joueurs participant à un tournoi spécifique, par ordre alphabétique."""

        # 1. Vérifier qu'un fichier de joueurs est bien chargé en mémoire
        if not self.db_controller.players_file:
            available_players = self.db_controller.get_available_players_files()

            if not available_players:
                self.view.display_error(1)
                return

            chosen_players_filename = self.view.display_file_selection_menu(available_players, 1)

            if not chosen_players_filename:
                return

            self.db_controller.set_players_file(chosen_players_filename)

        # 2. Demander la sélection du tournoi
        available_tournaments_files = self.db_controller.get_available_tournaments_files()

        if not available_tournaments_files:
            self.view.display_error(1)
            return

        chosen_tournament_filename = self.view.display_file_selection_menu(available_tournaments_files, 2)

        if not chosen_tournament_filename:
            return

        # 3. Chargement et traitement
        tournament_full_path = f"data/tournaments/{chosen_tournament_filename}"
        tournament = self.db_controller.load_tournament(tournament_full_path)

        if tournament:
            players = tournament.tournament_players
            sorted_players = sorted(players, key=lambda p: p.last_name.lower())
            self.view.display_tournament_players(tournament, sorted_players)

        else:
            self.view.display_error(2)

    def matchs_and_rounds(self):
        """Affiche l'historique complet des rounds et matchs d'un tournoi."""
        if not self.db_controller.players_file:
            available_players = self.db_controller.get_available_players_files()

            if not available_players:
                self.view.display_error(1)
                return

            chosen_players_filename = self.view.display_file_selection_menu(available_players, 1)

            if not chosen_players_filename:
                return

            self.db_controller.set_players_file(chosen_players_filename)

        available_tournament_files = self.db_controller.get_available_tournaments_files()
        if not available_tournament_files:
            self.view.display_error(1)
            return

        user_choice = self.view.display_file_selection_menu(available_tournament_files, 2)

        if not user_choice:
            return

        full_path = f"data/tournaments/{user_choice}"
        selected_tournament = self.db_controller.load_tournament(full_path)

        if not selected_tournament:
            self.view.display_error(2)
            return

        self.view.display_tournament_rounds_and_matchs(selected_tournament)
