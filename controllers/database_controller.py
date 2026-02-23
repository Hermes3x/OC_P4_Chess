from models.player import Player
from models.tournament import Tournament
import json
import os


class DatabaseController:
    def __init__(self):
        self.players_file = None
        self.players_cache = []

    def get_available_players_files(self):
        directory = "data/players"
        if not os.path.exists(directory):
            return []
        return [f for f in os.listdir(directory) if f.endswith(".json")]

    def get_available_tournaments_files(self):
        directory = "data/tournaments"
        if not os.path.exists(directory):
            return []
        return [f for f in os.listdir(directory) if f.endswith(".json")]

    def set_players_file(self, json_players_filename):
        if not json_players_filename.endswith(".json"):
            json_players_filename += ".json"

        full_path_json_players_filename = os.path.join(
            "data/players", json_players_filename)

        if not os.path.exists(full_path_json_players_filename):
            return False

        self.players_file = full_path_json_players_filename
        self.players_cache = self.load_players_from_json()
        return True

    def find_player_by_id(self, target_id):
        # On cherche directement dans le cache mémoire
        for player in self.players_cache:
            if player.national_chess_id == target_id:
                return player

        return None

    def find_player_by_name(self, target_name):
        found_players = []
        target = target_name.lower()
        for player in self.players_cache:
            full_name = f"{player.last_name} {player.first_name}".lower()
            if target == full_name:
                found_players.append(player)

        return found_players

    def find_players_name_start_with(self, target_name_start):
        found_players = []

        target = target_name_start.lower()
        for player in self.players_cache:
            full_name = f"{player.last_name} {player.first_name}".lower()
            if full_name.startswith(target):
                found_players.append(player)

        return found_players

    def save_players_to_json(self, players_list):
        if not self.players_file:
            return False

        serialized_players = []
        for player in players_list:
            serialized_players.append(player.to_dict())

        os.makedirs(os.path.dirname(self.players_file), exist_ok=True)

        with open(self.players_file, 'w') as file:
            json.dump(serialized_players, file, indent=4)

    def load_players_from_json(self):
        if not self.players_file or not os.path.exists(self.players_file):
            return []

        with open(self.players_file, 'r') as file:
            try:
                players_data = json.load(file)
            except json.JSONDecodeError:
                return []

        loaded_players = []
        for data in players_data:
            player_obj = Player.from_dict(data)
            loaded_players.append(player_obj)

        return loaded_players

    def update_global_players_to_json(self, tournament_players):
        if not self.players_file:
            return

        existing_ids = [player.national_chess_id for player in self.players_cache]
        updated = False

        for player in tournament_players:
            if player.national_chess_id not in existing_ids:
                self.players_cache.append(player)
                updated = True

        if updated:
            self.save_players_to_json(self.players_cache)

    def save_tournament_to_json(self, tournament):
        try:
            clean_name = tournament.name.replace(" ", "_").lower()
            filename = f"data/tournaments/{clean_name}.json"

            data = tournament.to_dict()

            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            return True  # <--- INDISPENSABLE pour que le MainController sache que ça a marché
        except Exception as e:
            print(f"Erreur lors de l'écriture : {e}")
            return False  # <--- Indique l'échec au contrôleur

    def load_tournament(self, filename):
        if not os.path.exists(filename):
            return None

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        tournament = Tournament(
            data['name'], data['place'], data['date'],
            data['round_qty'], data['note'], data.get('end_date')
        )
        tournament.actual_round = data.get('actual_round', 0)

        players_map = {p.national_chess_id: p for p in self.players_cache}

        # On crée une liste vide directement DANS l'objet tournoi
        tournament.missing_players = []

        for player_id in data['players_ids']:
            if player_id in players_map:
                tournament.add_player(players_map[player_id])
            else:
                # On stocke dans l'objet tournoi au lieu de faire un print
                tournament.missing_players.append(player_id)

        self._load_rounds(tournament, data['rounds_list'], players_map)

        return tournament  # ON NE RENVOIE PLUS DE TUPLE, JUSTE L'OBJET

    def load_all_tournaments(self):
        tournaments = []
        directory = "data/tournaments"

        if not os.path.exists(directory):
            return []

        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                file_path = os.path.join(directory, filename)
                tournament = self.load_tournament(file_path)
                if tournament:
                    tournaments.append(tournament)

        return tournaments

    def _load_rounds(self, tournament, rounds_data, players_map):
        from models.round import Round
        from models.match import Match

        for round_dict in rounds_data:
            round_obj = Round(tournament)

            # CORRECTION : Sécurité sur le split pour éviter le crash si format différent
            r_id_str = str(round_dict['round_id'])
            if ' ' in r_id_str:
                round_obj.rounds_id = int(r_id_str.split(' ')[1])
            else:
                round_obj.rounds_id = int(r_id_str)

            round_obj.start_date = round_dict['start_date']
            round_obj.end_date = round_dict['end_date']

            for match_data in round_dict['matchs']:
                id1, score1, color1 = match_data[0]
                id2, score2, color2 = match_data[1]

                p1 = players_map.get(id1)
                p2 = players_map.get(id2)

                if p1 and p2:
                    match_obj = Match(p1, p2)
                    match_obj.player1_score = score1
                    match_obj.player2_score = score2
                    match_obj.player1_color = color1
                    match_obj.player2_color = color2

                    if p1.national_chess_id in tournament.players_scores:
                        tournament.players_scores[p1.national_chess_id] += score1
                    if p2.national_chess_id in tournament.players_scores:
                        tournament.players_scores[p2.national_chess_id] += score2

                    round_obj.matchs.append(match_obj)

            tournament.rounds_list.append(round_obj)
            tournament.actual_round = round_obj.rounds_id
