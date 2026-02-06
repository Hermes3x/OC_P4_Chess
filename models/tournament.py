from models.round import Round
from models.player import Player
import random


class Tournament:
    def __init__(self, name, place, date, rounds_qty, note, end_date=None, players_scores=None):
        self.name = name
        self.place = place
        self.date = date
        self.rounds_qty = 4
        self.actual_round = 0
        self.rounds_list = []
        self.tournament_players = []
        self.note = note
        self.end_date = end_date
        if players_scores is None:
            self.players_scores = {}
        else:
            self.players_scores = players_scores

    def add_player(self, player):
        self.tournament_players.append(player)
        if player.national_chess_id not in self.players_scores:
            self.players_scores[player.national_chess_id] = 0.0

    def create_round(self):
        if len(self.rounds_list) > 0:
            last_round = self.rounds_list[-1]
            if last_round.end_date is None:
                print(f"Le round {self.actual_round} n'est pas terminé")
                return None

        if len(self.rounds_list) >= self.rounds_qty:
            print("Le tournoi est terminé")
            return None

        self.actual_round += 1

        if self.actual_round == 1:
            random.shuffle(self.tournament_players)
        else:
            self.tournament_players.sort(key=lambda p: (-self.players_scores[p.national_chess_id], p.last_name))

        current_round = Round(self)
        current_round.create_matchs()
        self.rounds_list.append(current_round)

        return current_round
    
    def update_players_scores_from_round(self, round_obj):
        for match in round_obj.matchs:
            p1, p2 = match.players_pair

            if p1.national_chess_id in self.players_scores:
                self.players_scores[p1.national_chess_id] += match.player1_score
            if p2.national_chess_id in self.players_scores:
                self.players_scores[p2.national_chess_id] += match.player2_score

    def __str__(self):
        return (f'Le tournoi {self.name} '
                f'se déroulera à {self.place} '
                f'le {self.date} '
                f'et se jouera en {self.rounds_qty} rounds')

    def to_dict(self):
        return {
            "name": self.name,
            "place": self.place,
            "date": self.date,
            "round_qty": self.rounds_qty,
            "rounds_list": [round.to_dict()
                            for round in
                            self.rounds_list],
            "players_ids": [p.national_chess_id
                            for p in
                            self.tournament_players],
            "note": self.note,
            "end_date": self.end_date,
            }
