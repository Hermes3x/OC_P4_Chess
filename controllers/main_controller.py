from controllers.database_controller import DatabaseController
from controllers.reports_controller import ReportController
from views.base_view import MainMenuView
from views.tournament_view import TournamentView
from views.report_view import ReportView
from models.tournament import Tournament
from models.player import Player
import datetime


class MainController:
    """Contrôleur principal gérant les transitions entre vues, modèles et contrôleurs secondaires."""

    def __init__(self):
        """Initialise les vues et les contrôleurs secondaires."""
        self.menu_view = MainMenuView()
        self.tournament_view = TournamentView()
        self.db_controller = DatabaseController()
        self.report_view = ReportView()

    def run_tournament_menu(self, tournament):
        """Gère le menu interne d'un tournoi (Play, Classement, Quitter)."""
        while True:
            current_count = len(tournament.tournament_players)
            max_players = tournament.rounds_qty * 2

            self.tournament_view.display_tournament_menu(f"\n--- ♟️ GESTION : {tournament.name} ---")
            self.tournament_view.display_tournament_menu(
                f"Nombre de joueurs inscrits : {current_count} / {max_players}")

            # Étape d'inscription des joueurs
            if current_count < max_players:
                if current_count == 0:
                    self.tournament_view.display_tournament_menu(
                        "📝 Nouveau tournoi détecté. Veuillez enregistrer les joueurs.")
                else:
                    self.tournament_view.display_tournament_menu(
                        f"ℹ️ Inscription en cours... ({current_count}/{max_players})")

                self.choose_player(tournament)

                # Vérification compte joueurs après l'ajout
                if len(tournament.tournament_players) < max_players:
                    self.tournament_view.display_tournament_menu(
                        "\n⚠️ Inscription mise en pause. Retour au menu principal...")
                    break

                continue

            # Menu de jeu une fois le tournoi complet
            else:
                self.tournament_view.display_tournament_menu(
                    f"✅ Tournoi prêt ! Round : {tournament.actual_round} / {tournament.rounds_qty}")
                self.tournament_view.display_tournament_menu("1. Jouer le prochain round")
                self.tournament_view.display_tournament_menu("2. Voir le classement provisoire")
                self.tournament_view.display_tournament_menu("3. Quitter et revenir au menu principal")

                choice = input("Votre choix : ")

                # Joueur le round suivant
                if choice == "1":
                    self.play_round(tournament)

                    if tournament.actual_round == tournament.rounds_qty:
                        tournament.end_date = str(datetime.date.today())
                        if self.db_controller.save_tournament_to_json(tournament) is True:
                            self.tournament_view.display_events(f"💾 Tournoi sauvegardé : {tournament}")
                        else:
                            self.tournament_view.display_error("Error")
                        self.tournament_view.display_tournament_end(tournament)
                        self.tournament_view.display_final_ranking(tournament)

                # Afficher le classement
                elif choice == "2":
                    self.tournament_view.display_final_ranking(tournament)

                # Quitter
                elif choice == "3":
                    break

    def choose_player(self, tournament):
        """Gère l'ajout de joueurs au tournoi.
        permet l'utilisation de différentes méthodes d'ajout.
        S'arrête quand le tournoi est plein ou sur annulation manuelle."""
        available_files = self.db_controller.get_available_players_files()

        # Vérifie la présence du fichier JSON joueurs
        if not available_files:
            self.tournament_view.display_error("Aucun fichier de joueurs trouvé !")
            return

        # Sélection du fichier JSON joueurs
        chosen_filename = self.tournament_view.display_file_selection_menu(
            available_files, "📂 Veuillez choisir le fichier de joueurs à charger :")

        if not chosen_filename:
            return

        self.db_controller.set_players_file(chosen_filename)
        # On stocke les IDs déjà présents pour éviter les doublons
        forbidden_ids = {p.national_chess_id for p in tournament.tournament_players}
        max_players = tournament.rounds_qty * 2

        # Boucle de remplissage du tournoi et de contrôle du nombre de joueurs
        while len(tournament.tournament_players) < max_players:
            choice = self.tournament_view.choose_player_search_method()

            # Annuler / Terminer
            if choice == "5":
                break

            chosen_player = None

            # OPTION 1 : Recherche par ID National
            if choice == "1":
                id_input = self.tournament_view.select_player_id()
                if id_input:
                    chosen_player = self.db_controller.find_player_by_id(id_input)
                    if not chosen_player:
                        self.tournament_view.display_player_id_not_found(id_input)

            # OPTION 2 : Recherche par Nom exact
            elif choice == "2":
                name_input = self.tournament_view.select_player_name()
                if name_input:
                    found = self.db_controller.find_player_by_name(name_input)
                    if found:
                        idx = self.tournament_view.display_players_list_selection(found)
                        chosen_player = found[idx]
                    else:
                        self.tournament_view.display_player_name_not_found(name_input)

            # OPTION 3 : Recherche par Début du nom
            elif choice == "3":
                start_input = self.tournament_view.select_players_starting_with()
                if start_input:
                    found = self.db_controller.find_players_name_start_with(start_input)
                    if found:
                        idx = self.tournament_view.display_players_list_selection(found)
                        chosen_player = found[idx]
                    else:
                        self.tournament_view.display_player_name_not_found(start_input)

            # OPTION 4 : Création Manuelle d'un nouveau joueur et mise à jour du fichier JSON joueurs
            elif choice == "4":
                new_data = self.tournament_view.get_new_player_info()

                if new_data:
                    # Création de l'objet Player
                    chosen_player = Player(**new_data)

                    # Mise à jour de la base de données
                    if not self.db_controller.update_global_players_to_json([chosen_player]):
                        self.tournament_view.display_error("Fichier player introuvable")
                    else:
                        self.tournament_view.display_events("💾 Sauvegarde réussie")

            # Finalisation de l'ajout de joueurs au tournoi
            if chosen_player:
                if chosen_player.national_chess_id in forbidden_ids:
                    self.tournament_view.display_player_ever_added(chosen_player)
                else:
                    tournament.add_player(chosen_player)
                    forbidden_ids.add(chosen_player.national_chess_id)
                    self.tournament_view.display_player_added(chosen_player)

                    # Mise à jour du compteur
                    count = len(tournament.tournament_players)
                    self.tournament_view.display_nb_added_players(f"({count}/{max_players} joueurs).")

                    # Sauvegarde
                    if self.db_controller.save_tournament_to_json(tournament):
                        self.tournament_view.display_events(f"💾 Tournoi sauvegardé : {tournament.name}")
                    else:
                        self.tournament_view.display_error("Erreur lors de la sauvegarde du tournoi.")

        return

    def play_round(self, tournament):
        """Gère le déroulement d'un round : paires, scores et clôture."""
        if tournament.actual_round >= tournament.rounds_qty:
            self.tournament_view.display_tournament_end(tournament)
            return

        # 1. Création
        new_round = tournament.create_round()
        self.tournament_view.display_round_start(new_round)

        # 2. Matchs
        for match in new_round.matchs:
            match.draw_color()
            winner, _ = self.tournament_view.get_match_score(match)
            match.score(winner)

        # 3. Clôture du round
        new_round.close_round()
        tournament.update_players_scores_from_round(new_round)

        # 4. Affichage des résultats et sauvegarde
        self.tournament_view.display_round_matchs(new_round)
        if self.db_controller.save_tournament_to_json(tournament):
            self.tournament_view.display_events(f"💾 Tournoi sauvegardé : {tournament.name}")
        else:
            self.tournament_view.display_error("Erreur lors de la sauvegarde du round.")
        self.tournament_view.display_round_matchs_saving(new_round)

    def run(self):
        """Point d'entrée principal : affiche le menu de démarrage d'un tournoi."""
        running = True
        while running:
            user_choice = self.menu_view.display_main_menu()

            # Créer un tournoi
            if user_choice == "1":
                # Informations du tournoi
                data = self.tournament_view.get_tournament_data()
                tournament = Tournament(
                    name=data['name'],
                    place=data["place"],
                    date=data["date"],
                    rounds_qty=data["round_qty"],
                    note=data["note"],
                    )

                self.run_tournament_menu(tournament)

            # Charger un tournoi
            elif user_choice == "2":
                # Sélection du fichier joueur
                if not self.db_controller.players_file:
                    available_players = self.db_controller.get_available_players_files()
                    if not available_players:
                        self.tournament_view.display_error(
                            "Impossible de charger le tournoi : Aucun fichier de joueurs trouvé !"
                        )
                        continue  # Ajout d'un continue pour éviter de tenter de charger un tournoi sans joueurs

                    players_filename = self.tournament_view.display_file_selection_menu(
                        available_players,
                        "📂 Pour charger le tournoi, veuillez d'abord sélectionner le fichier de joueurs de référence :"
                    )

                    if not players_filename:
                        continue

                    if self.db_controller.set_players_file(players_filename) is False:
                        self.tournament_view.display_error(f"Impossible d'ouvrir le fichier {players_filename}")
                        continue

                    # On charge et on vérifie la présence du fichier joueurs
                    if self.db_controller.load_players_from_json() is True:
                        self.tournament_view.display_events(
                            f"📂 Chargement réussi : {len(available_players)} joueurs récupérés."
                        )

                # Sélection du fichier tournoi
                available_tournaments = self.db_controller.get_available_tournaments_files()

                if not available_tournaments:
                    self.tournament_view.display_error("Aucun tournoi sauvegardé.")
                    continue

                filename = self.tournament_view.display_file_selection_menu(
                    available_tournaments, "📂 Veuillez choisir le tournoi à charger :"
                )

                if not filename:
                    continue

                full_path = f"data/tournaments/{filename}"
                tournament = self.db_controller.load_tournament(full_path)

                if tournament:
                    self.tournament_view.display_events(f"📂 Tournoi '{tournament.name}' chargé avec succès !")
                    self.tournament_view.display_tournament_loaded(tournament)

                    # Vérification des joueurs orphelins (ID absent de la DB)
                    if hasattr(tournament, 'missing_players') and tournament.missing_players:
                        for p_id in tournament.missing_players:
                            self.tournament_view.display_error(
                                f"Le joueur avec l'ID {p_id} est introuvable dans la base globale."
                            )

                    self.run_tournament_menu(tournament)
                else:
                    # Ici, le 'tournament' est None, donc on affiche un message d'erreur explicite
                    self.tournament_view.display_error(f"❌ Erreur : Impossible de charger le fichier {filename}")

            # RAPPORTS
            elif user_choice == "3":
                report_controller = ReportController(self.db_controller)
                report_controller.run()

            # QUITTER
            elif user_choice == "4":
                running = False
