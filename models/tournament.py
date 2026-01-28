from models.round import Round


class Tournament:
    def __init__(self, name, place, date, rounds_qty, note):
        self.id = 0
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
        if len(self.rounds_list) < self.rounds_qty:
            self.tournament_players.sort(key=lambda p: (-p.score, p.last_name))
            current_round = Round(self)
            current_round.create_matchs()

            self.rounds_list.append(current_round)
            self.actual_round += 1

            return current_round

    def __str__(self):
        return (f'Le tournoi {self.name} '
                f'se déroulera à {self.place} '
                f'le {self.date} '
                f'et se jouera en {self.rounds_qty} rounds')
