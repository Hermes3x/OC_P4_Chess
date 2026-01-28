class PlayersManager:
    def __init__(self):
        self.tournament_players = []

    def add_tournament_players(self, player):
        self.tournament_players.append(player)

    def score_sorted_tournament_players(self):
        self.tournament_players.sort(key=lambda p: (-p.score, p.last_name))

    def __str__(self):
        lines = []
        for player in self.tournament_players:
            lines.append(f'{player.last_name} {player.first_name} '
                         f'{player.national_chess_id} {player.score}')
        return "\n".join(lines)
