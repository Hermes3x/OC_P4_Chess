from models.match import Match
import datetime


class Round:
    def __init__(self, tournament, date=None):
        self.tournament = tournament
        self.tournament_players = tournament.tournament_players
        # self.rounds_id = 1
        self.end_date = None
        self.matchs = []
        if date is None:
            self.date = datetime.date.today()
        else:
            self.date = date

    def create_matchs(self):
        players_pool = self.tournament_players.copy()

        while len(players_pool) >= 2:
            p1 = players_pool.pop(0)
            opponent = None

            for i in range(len(players_pool)):
                candidate = players_pool[i]
                if candidate.national_chess_id not in p1.opponents:
                    opponent = players_pool.pop(i)
                    break
            if opponent is None:
                opponent = players_pool.pop(0)

            match = Match(p1, opponent)
            self.matchs.append(match)
            p1.add_opponent(opponent)
            opponent.add_opponent(p1)

    def __str__(self):
        match_str = "\n".join(str(match) for match in self.matchs)
        return f'Date de démarrage : {self.date}\n{match_str}'
