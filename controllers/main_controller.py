from controllers.database_controller import DatabaseController
from controllers.reports_controller import ReportController
from views.base_view import MainMenuView
from views.tournament_view import TournamentView
from views.report_view import ReportView
from models.tournament import Tournament
from models.player import Player
import random
import datetime


class MainController:
    def __init__(self):
        self.menu_view = MainMenuView()
        self.tournament_view = TournamentView()
        self.db_controller = DatabaseController()
        self.report_view = ReportView()

    def choose_player(self, tournament):
        """Choix du joueur"""
        file_choice = self.tournament_view.choose_players_json()
        is_valid_file_choice = self.db_controller.set_players_file(file_choice)
        if not is_valid_file_choice:
            return

        player_selection_choice = (
            self.tournament_view.choose_player_search_method())
        
        forbidden_players_ids_to_add = {p.id for p in tournament.tournament_players}
        final_selection = []

        if player_selection_choice == "1":
            # input retournée par utilisateur
            while True:
                chosen_id = self.tournament_view.select_player_id()
                if not chosen_id:
                    break

                chosen_player = self.db_controller.find_player_by_id(chosen_id)

                if chosen_player is None:
                    self.tournament_view.display_player_id_not_found(chosen_id)

                elif chosen_player.id in forbidden_players_ids_to_add:
                    self.tournament_view.display_player_ever_added(chosen_player)

                else:
                    final_selection.append(chosen_player)
                    forbidden_players_ids_to_add.add(chosen_player.id)
                    self.tournament_view.display_player_added(chosen_player)

            return final_selection

        elif player_selection_choice == "2":
            while True:
                name_input = self.tournament_view.select_player_name()
                if not name_input:
                    break

                found_players = self.db_controller.find_player_by_name(
                    name_input)
                
                if not found_players:
                    self.tournament_view.display_player_name_not_found(
                        name_input)

                else:
                    chosen_index = self.tournament_view.display_players_list_selection(found_players)
                    chosen_player = found_players[chosen_index]

                    if chosen_player.id in forbidden_players_ids_to_add:
                        self.tournament_view.display_player_ever_added(chosen_player)

                    else:
                        final_selection.append(chosen_player)
                        forbidden_players_ids_to_add.add(chosen_player.id)
                        self.tournament_view.display_player_added(chosen_player)

            return final_selection

        elif player_selection_choice == "3":
            while True:
                name_start_input = self.tournament_view.select_players_starting_with()
                if not name_start_input:
                    break

                found_players_name_start = self.db_controller.find_players_name_start_with(name_start_input)

                if not found_players_name_start:
                    self.tournament_view.display_player_name_not_found(
                        name_start_input)

                else:
                    chosen_player_index = self.tournament_view.display_players_list_selection(
                        found_players_name_start)
                    chosen_player = found_players_name_start[chosen_player_index]

                    if chosen_player.id not in forbidden_players_ids_to_add:
                        final_selection.append(chosen_player)
                        forbidden_players_ids_to_add.add(chosen_player.id)
                        self.tournament_view.display_player_added(chosen_player)

                    else:
                        self.tournament_view.display_player_ever_added(chosen_player)

            return final_selection

        elif player_selection_choice == "4":
            while True:
                new_player_data = self.tournament_view.get_new_player_info()

                if not new_player_data:
                    break

                elif new_player_data in forbidden_players_ids_to_add:
                    self.tournament_view.display_player_ever_added(new_player_data)

                else:
                    new_player_obj = Player(**new_player_data)
                    final_selection.append(new_player_obj)

            return final_selection

    def play_round(self, tournament):
        """Joue UN seul round (celui en cours)"""
        if tournament.actual_round >= tournament.rounds_qty:
            self.tournament_view.display_tournament_end(tournament)
            return

        # 1. Création du round (les paires sont faites dans create_round)
        new_round = tournament.create_round()
        self.tournament_view.display_round_start(new_round)

        # 2. Déroulement des matchs
        for match in new_round.matchs:
            match.draw_color()
            # SCORING ALEATOIRE (Pour test rapide) - À remplacer par manuel plus tard
            p1, p2 = match.players_pair
            winner = random.choice([p1, p2, None])
            match.score(winner)

        # 3. Fin du round
        new_round.close_round()
        tournament.update_players_scores_from_round(new_round)

        # 4. Affichage et Sauvegarde
        self.tournament_view.display_round_matchs(new_round)
        self.db_controller.save_tournament_to_json(tournament)
        self.tournament_view.display_round_matchs_saving(new_round)

    def run_tournament_menu(self, tournament):
        """Sous-menu pour gérer un tournoi spécifique"""
        while True:
            print(f"\n--- ♟️ GESTION : {tournament.name} ---")
            print(f"Round : {tournament.actual_round} / {tournament.rounds_qty}")
            print("1. Jouer le prochain round")
            print("2. Voir le classement provisoire")
            print("3. Quitter et revenir au menu principal")

            choice = input("Votre choix : ")

            if choice == "1":
                self.play_round(tournament)

                # Si c'était le dernier round, on affiche la fin
                if tournament.actual_round == tournament.rounds_qty:
                    tournament.end_date = str(datetime.date.today())
                    self.db_controller.save_tournament_to_json(tournament)
                    self.tournament_view.display_tournament_end(tournament)
                    self.tournament_view.display_final_ranking(tournament)

            elif choice == "2":
                self.tournament_view.display_final_ranking(tournament)

            elif choice == "3":
                break

    def run(self):
        running = True
        while running:
            user_choice = self.menu_view.display_main_menu()

            if user_choice == "1":
                data = self.tournament_view.get_tournament_data()
                tournament = Tournament(
                    name=data['name'],
                    place=data["place"],
                    date=data["date"],
                    rounds_qty=data["round_qty"],
                    note=data["note"],
                    )

                players_list = self.choose_player(tournament)

                if players_list:
                    for player in players_list:
                        tournament.add_player(player)

                self.db_controller.save_tournament_to_json(tournament)
                self.db_controller.update_global_players_to_json(tournament.tournament_players)
                self.tournament_view.display_tournament_creation(tournament)

                self.run_tournament_menu(tournament)

            elif user_choice == "2":  # CHARGER TOURNOI
                filename = self.tournament_view.choose_tournament_json()
                full_path = f"data/tournaments/{filename}.json"
                tournament = self.db_controller.load_tournament(full_path)

                if tournament:
                    self.tournament_view.display_tournament_loaded(tournament)
                    self.run_tournament_menu(tournament)

            elif user_choice == "3":  # RAPPORTS
                report_controller = ReportController(self.db_controller)
                report_controller.run()

            elif user_choice == "4":  # QUITTER
                running = False
