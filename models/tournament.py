from models.round import Round


class Tournament:
    def __init__(self, name, place, date, rounds_qty, note):
        self.name = name
        self.place = place
        self.date = date
        self.rounds_qty = 4
        self.actual_round = 0
        self.rounds_list = []
        self.tournament_players = []
        self.note = note

    def add_player(self, player):
        self.tournament_players.append(player)

    def create_round(self):
        if len(self.rounds_list) > 0:
            last_round = self.rounds_list[-1]
            if last_round.end_date is None:
                print(f"Le round {self.actual_round} n'est pas terminé")
                return None

        if len(self.rounds_list) >= self.rounds_qty:
            print("Le tournoi est terminé")
            return None

        print(f"🚀 Lancement du Round {self.actual_round + 1}...")

        self.tournament_players.sort(key=lambda p: (-p.score, p.last_name))
        self.actual_round += 1
        current_round = Round(self)
        current_round.create_matchs()
        self.rounds_list.append(current_round)

        return current_round

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
            "note": self.note
            }
