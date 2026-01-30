from controllers.database_controller import DatabaseController
from views.base_view import MainMenuView
from views.tournament_view import TournamentView
from models.tournament import Tournament

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
                    rounds_qty=["round_qty"],
                    note=["note"],
                )
                print(f"Tournoi {tournament.name} créé avec succé")
                self.db_controller.save_tournament_to_json(tournament)

            elif user_choice == "2":
                print(">>> TODO: Lancer le chargement de tournoi") #  doit pouvoir choisir quel tournoi
            elif user_choice == "3":
                print(">>> TODO: Afficher les rapports")  #  choisir quel rapport
            elif user_choice == "4":
                print("Au revoir !")
                running = False

            else:
                print("Choix invalide, veuillez réessayer.")
