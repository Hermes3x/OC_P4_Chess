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
                pass  # A faire plus tard (Matchs d'un tournoi)
            elif choice == "6":
                # On quitte la boucle du rapport pour revenir au MainController
                break
            else:
                print("Choix invalide, veuillez réessayer.")

    def tournament_players(self):
        tournament_input = self.view.ask_specific_tounrmanent()
        tournament_full_path = f"data/tournaments/{tournament_input}.json"
        selected_tournament = self.db_controller.load_tournament(tournament_full_path)  # on a le droit de faire çà : self.db_controller.load_tournament(self.view.ask_specific_tounrmanent())
        tournament_players = selected_tournament.tournament_players
        sorted_tournament_players = sorted(tournament_players, key=lambda p: p.last_name.lower())
        self.view.display_players_sorted_list(sorted_tournament_players)

    def all_players_alphabetic_sort(self):
        players = self.db_controller.load_players_from_json()
        sorted_players = sorted(players, key=lambda p: p.last_name)
        self.view.display_players_sorted_list(sorted_players)

    def all_tournaments(self):
        tournaments_list = self.db_controller.load_all_tournaments()
        self.view.display_tournaments_list(tournaments_list)

    def specific_tounament(self):
        tournament_filename = self.view.ask_specific_tounrmanent()
        full_path = f"data/tournaments/{tournament_filename}.json"
        tournament_obj = self.db_controller.load_tournament(full_path)
        if tournament_obj:
            self.view.specific_tournament_info(tournament_obj)
        else:
            self.view.display_error("Tournoi introuvable ou fichier corrompu.")
