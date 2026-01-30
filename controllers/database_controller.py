from models.player import Player
from models.tournament import Tournament
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
    
    def save_tournament_to_json(self, tournament):
        clean_name = tournament.name.replace(" ", "_").lower()
        filename = f"data/tournaments/{clean_name}.json"

        data = tournament.to_dict()

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        
        print(f"💾 Tournoi sauvegardé : {filename}")
    
    def load_tournament(self, filename):
        if not os.path.exists(filename):
            print(f"❌ Fichier introuvable : {filename}")
            return None
        
        with open(filename, 'r') as file:
            data = json.load(file)

        all_players = self.load_players_from_json()
        players_map = {p.national_chess_id: p for p in all_players}

        tournament = Tournament(
            name=data['name'],
            place=data['place'],
            date=data['date'],
            rounds_qty=data['round_qty'],
            note=data['note']
        )

        #  tournament.id = data['id']

        for player_id in data['players_ids']:
            if player_id in players_map:
                tournament.add_player(players_map[player_id])
            else:
                print(f"⚠️ Joueur {player_id} introuvable dans la base globale !")

        self._load_rounds(tournament, data['rounds_list'], players_map)

        print(f"✅ Tournoi '{tournament.name}' chargé avec succès !")
        return tournament
    
    def _load_rounds(self, tournament, rounds_data, players_map):
        from models.round import Round
        from models.match import Match

        for round_dict in rounds_data:
            round_obj = Round(tournament)
            round_obj.rounds_id = int(round_dict['round_id'].split(' ')[1])
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

                    p1.score += score1
                    p2.score += score2

                    round_obj.matchs.append(match_obj)

            tournament.rounds_list.append(round_obj)
            tournament.actual_round = round_obj.rounds_id
