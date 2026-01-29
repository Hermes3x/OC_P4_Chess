from models.player import Player
import json
import os


class DatabaseController:
    def __init__(self):
        self.players_file = "data/players/players.json"
        #  self.tournament_file = "data/tournament/"

    def save_players_to_json(self, players_list):
        serialized_players = []
        for player in players_list:
            serialized_players.append(player.to_dict())

        os.makedirs(os.path.dirname(self.players_file), exist_ok=True)

        with open(self.players_file, 'w') as file:
            json.dump(serialized_players, file, indent=4)

        print(f'💾 Sauvegarde réussie : {len(players_list)} '
              f'joueurs enregistrés')

    def load_players_from_json(self):
        if not os.path.exists(self.players_file):
            return []

        with open(self.players_file, 'r') as file:
            players_data = json.load(file)

        loaded_players = []
        for data in players_data:
            player_obj = Player.from_dict(data)
            loaded_players.append(player_obj)

        print(f"📂 Chargement réussi : {len(loaded_players)} joueurs récupérés.")
        return loaded_players
