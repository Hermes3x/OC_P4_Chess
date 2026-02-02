from models.match import Match
import datetime


class Round:
    def __init__(self, tournament, start_date=None):
        self.tournament = tournament
        self.tournament_players = tournament.tournament_players
        self.rounds_id = tournament.actual_round
        self.matchs = []
        if start_date is None:
            self.start_date = datetime.datetime.now()
        else:
            self.start_date = start_date
        self.end_date = None

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
            match.draw_color()
            self.matchs.append(match)
            p1.add_opponent(opponent)
            opponent.add_opponent(p1)

    def close_round(self):
        all_finished = all((m.player1_score + m.player2_score)
                           > 0
                           for m in self.matchs)
        if not all_finished:
            return

        self.end_date = datetime.datetime.now()
        return

    def __str__(self):
        match_str = "\n".join(str(match) for match in self.matchs)
        return f'Date de démarrage : {self.date}\n{match_str}'

    def to_dict(self):
        return {
            'round_id': f"Round {self.rounds_id}",
            'start_date': str(self.start_date),
            'end_date': str(self.end_date) if self.end_date else None,
            'matchs': [match.to_dict() for match in self.matchs]
            }
