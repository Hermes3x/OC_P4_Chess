from controllers.database_controller import DatabaseController
from views.base_view import MainMenuView
from views.tournament_view import TournamentView
from models.tournament import Tournament
from models.player import Player
from models.round import Round
from models.match import Match
import random
import datetime


class MainController:
    def __init__(self):
        self.menu_view = MainMenuView()
        self.tournament_view = TournamentView()
        self.db_controller = DatabaseController()

    def run(self):
        running = True

        while running:
            user_choice = self.menu_view.display_main_menu()

            if user_choice == "1":
                data = self.tournament_view.get_tournament_data()
                tournament = Tournament(
                    name=data["name"],
                    place=data["place"],
                    date=data["date"],
                    rounds_qty=data["round_qty"],
                    note=data["note"],
                )
                print(f"Tournoi {tournament.name} créé avec succé")
                self.db_controller.save_tournament_to_json(tournament)

                get_tournament_players_from_json = (
                    self.tournament_view.get_tournament_players_from_json())

                if get_tournament_players_from_json == "Y":
                    player_lists = self.db_controller.load_players_from_json()
                    for player in player_lists:
                        tournament.add_player(player)
                else:
                    new_players = []
                    while True:
                        user_response = (
                            self.tournament_view.ask_add_player_manually())
                        if user_response == "n":
                            break

                        player_data = (
                            self.tournament_view.get_new_player_info())
                        new_player = Player(
                            first_name=player_data["first_name"],
                            last_name=player_data["last_name"],
                            birth_date=player_data["birth_date"],
                            national_chess_id=player_data["national_chess_id"],
                            score=0
                            )
                        tournament.add_player(new_player)
                        new_players.append(new_player)
                    self.db_controller.save_players_to_json(new_players)

                print(f"\n🚀 Lancement du tournoi avec "
                      f"{len(tournament.tournament_players)} joueurs")
                self.db_controller.save_tournament_to_json(tournament)

                round1 = tournament.create_round()
                print("\n📋 Lancement des matchs du Round 1 :")
                for match in round1.matchs:
                    p1, p2 = match.players_pair
                    match.draw_color()
                    match.score(random.choice([p1, p2, None]))
                round1.close_round()
                self.tournament_view.display_round_matchs(round1)
                self.db_controller.save_tournament_to_json(tournament)

                round2 = tournament.create_round()
                print("\n📋 Lancement des matchs du Round 2 :")
                for match in round2.matchs:
                    p1, p2 = match.players_pair
                    match.draw_color()
                    match.score(random.choice([p1, p2, None]))
                round2.close_round()
                self.tournament_view.display_round_matchs(round2)
                self.db_controller.save_tournament_to_json(tournament)

                round3 = tournament.create_round()
                print("\n📋 Lancement des matchs du Round 3 :")
                for match in round3.matchs:
                    p1, p2 = match.players_pair
                    match.draw_color()
                    match.score(random.choice([p1, p2, None]))
                round3.close_round()
                self.tournament_view.display_round_matchs(round3)
                self.db_controller.save_tournament_to_json(tournament)

                round4 = tournament.create_round()
                print("\n📋 Lancement des matchs du Round 4 :")
                for match in round4.matchs:
                    p1, p2 = match.players_pair
                    match.draw_color()
                    match.score(random.choice([p1, p2, None]))
                round4.close_round()
                tournament.end_date = datetime.date.today()
                self.tournament_view.display_round_matchs(round4)
                self.tournament_view.display_final_ranking(tournament)
                self.db_controller.save_tournament_to_json(tournament)

            elif user_choice == "2":
                print(">>> TODO: Lancer le chargement de tournoi")
                filename = self.tournament_view.choose_tournament_json()
                full_path_filename = f"data/tournaments/{filename}.json"
                tournament_to_load = self.db_controller.load_tournament(full_path_filename)
                if tournament_to_load:
                    print(f"✅ {tournament_to_load} !")

            elif user_choice == "3":
                print(">>> TODO: Afficher les rapports")  # choisir quel rapport
            elif user_choice == "4":
                print("Au revoir !")
                running = False

            else:
                print("Choix invalide, veuillez réessayer.")
