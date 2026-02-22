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
        """Gère l'ajout de joueurs au tournoi jusqu'à ce qu'il soit plein ou annulé."""
        available_files = self.db_controller.get_available_players_files()

        if not available_files:
            self.tournament_view.display_error("Aucun fichier de joueurs trouvé !")
            return

        chosen_filename = self.tournament_view.display_file_selection_menu(
            available_files, "📂 Veuillez choisir le fichier de joueurs à charger :")

        if not chosen_filename:
            return 

        self.db_controller.set_players_file(chosen_filename)
        forbidden_ids = {p.national_chess_id for p in tournament.tournament_players}
        max_players = tournament.rounds_qty * 2

        # La boucle principale gère elle-même le compteur
        while len(tournament.tournament_players) < max_players:
            choice = self.tournament_view.choose_player_search_method()

            if choice == "5": # Annuler / Terminer
                break

            chosen_player = None

            # --- OPTION 1 : ID ---
            if choice == "1":
                id_input = self.tournament_view.select_player_id()
                if id_input:
                    chosen_player = self.db_controller.find_player_by_id(id_input)
                    if not chosen_player:
                        self.tournament_view.display_player_id_not_found(id_input)

            # --- OPTION 2 : NOM ---
            elif choice == "2":
                name_input = self.tournament_view.select_player_name()
                if name_input:
                    found = self.db_controller.find_player_by_name(name_input)
                    if found:
                        idx = self.tournament_view.display_players_list_selection(found)
                        chosen_player = found[idx]
                    else:
                        self.tournament_view.display_player_name_not_found(name_input)

            # --- OPTION 3 : DÉBUT DE NOM ---
            elif choice == "3":
                start_input = self.tournament_view.select_players_starting_with()
                if start_input:
                    found = self.db_controller.find_players_name_start_with(start_input)
                    if found:
                        idx = self.tournament_view.display_players_list_selection(found)
                        chosen_player = found[idx]
                    else:
                        self.tournament_view.display_player_name_not_found(start_input)

            # --- OPTION 4 : MANUEL ---
            elif choice == "4":
                new_data = self.tournament_view.get_new_player_info()
                if new_data:
                    # On crée l'objet Player dynamiquement
                    chosen_player = Player(**new_data)
                    self.db_controller.update_global_players_to_json([chosen_player])

            # --- LOGIQUE D'AJOUT COMMUNE ---
            if chosen_player:
                if chosen_player.national_chess_id in forbidden_ids:
                    self.tournament_view.display_player_ever_added(chosen_player)
                else:
                    tournament.add_player(chosen_player)
                    forbidden_ids.add(chosen_player.national_chess_id)
                    self.tournament_view.display_player_added(chosen_player)
                    
                    # Mise à jour de la vue sur le compte actuel
                    count = len(tournament.tournament_players)
                    self.tournament_view.display_nb_added_players(f"({count}/{max_players} joueurs).")
                    
                    # Sauvegarde en temps réel
                    self.db_controller.save_tournament_to_json(tournament)

        return

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
            current_count = len(tournament.tournament_players)
            max_players = tournament.rounds_qty * 2

            print(f"\n--- ♟️ GESTION : {tournament.name} ---")
            print(f"Nombre de joueurs inscrits : {current_count} / {max_players}")

            # ÉTAPE 1 : Vérification du remplissage
            if current_count < max_players:
                if current_count == 0:
                    print("📝 Nouveau tournoi détecté. Veuillez enregistrer les joueurs.")
                else:
                    print(f"ℹ️ Inscription en cours... ({current_count}/{max_players})")
                
                # On lance l'ajout de joueurs
                self.choose_player(tournament)

                # Vérification après l'ajout
                if len(tournament.tournament_players) < max_players:
                    print("\n⚠️ Inscription mise en pause. Retour au menu principal...")
                    break 

                continue  # Relance la boucle pour passer à l'étape 2 (le menu de jeu)

            # ÉTAPE 2 : Menu de gestion une fois complet
            else:
                # On ne nettoie l'écran ou on n'affiche le menu que si c'est prêt
                print(f"✅ Tournoi prêt ! Round : {tournament.actual_round} / {tournament.rounds_qty}")
                print("1. Jouer le prochain round")
                print("2. Voir le classement provisoire")
                print("3. Quitter et revenir au menu principal")

                choice = input("Votre choix : ")

                if choice == "1":
                    self.play_round(tournament)

                    # Si c'était le dernier round, on finalise
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

                self.run_tournament_menu(tournament)

            elif user_choice == "2":  # CHARGER TOURNOI
                if not self.db_controller.players_file:
                    available_players = self.db_controller.get_available_players_files()
                    if not available_players:
                        self.tournament_view.display_error("Impossible de charger le tournoi : Aucun fichier de joueurs trouvé !")

                    players_filename = self.tournament_view.display_file_selection_menu(
                        available_players, "📂 Pour charger le tournoi, veuillez d'abord sélectionner le fichier de joueurs de référence :")
                    
                    if not players_filename:
                        continue

                    self.db_controller.set_players_file(players_filename)

                available_tournaments = self.db_controller.get_available_tournaments_files()

                if not available_tournaments:
                    self.tournament_view.display_error("Aucun tournoi sauvegardé.")
                    continue

                filename = self.tournament_view.display_file_selection_menu(
                    available_tournaments, "📂 Veuillez choisir le tournoi à charger :")

                if not filename:
                    continue

                full_path = f"data/tournaments/{filename}"
                tournament = self.db_controller.load_tournament(full_path)

                if tournament:
                    self.tournament_view.display_tournament_loaded(tournament)
                    self.run_tournament_menu(tournament)

            elif user_choice == "3":  # RAPPORTS
                report_controller = ReportController(self.db_controller)
                report_controller.run()

            elif user_choice == "4":  # QUITTER
                running = False
