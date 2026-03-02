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
        """Génère les matchs du round sans aucun doublon via backtracking."""
        players_pool = self.tournament_players.copy()

        def backtrack_pairing(unpaired_players):
            if not unpaired_players:
                return []

            p1 = unpaired_players[0]

            for i in range(1, len(unpaired_players)):
                p2 = unpaired_players[i]

                if p2.national_chess_id not in p1.opponents:
                    remaining = unpaired_players[1:i] + unpaired_players[i+1:]

                    result = backtrack_pairing(remaining)

                    if result is not None:
                        return [(p1, p2)] + result

            return None

        valid_pairs = backtrack_pairing(players_pool)

        if valid_pairs is None:
            print("Attention : Impossible de générer des paires 100% inédites. Forçage du classement...")
            valid_pairs = []
            while len(players_pool) >= 2:
                valid_pairs.append((players_pool.pop(0), players_pool.pop(0)))

        for p1, p2 in valid_pairs:
            match = Match(p1, p2)
            match.draw_color()
            self.matchs.append(match)

            p1.add_opponent(p2)
            p2.add_opponent(p1)

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
            'round_id': self.rounds_id,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date) if self.end_date else None,
            'matchs': [match.to_dict() for match in self.matchs]
            }
