from models.matchs import Match


class Rounds:
    def __init__(self, rounds_players_sorted_list):
        self.rounds_id = 1
        self.round_players_sorted_list = (
            rounds_players_sorted_list)
        self.matchs = []

    def create_matchs(self):
        for i in range(0, len(self.round_players_sorted_list), 2):
            match = Match(self.round_players_sorted_list[i],
                          self.round_players_sorted_list[i+1])
            self.matchs.append(match)
        return self.matchs

    def __str__(self):
        return "\n".join(str(match) for match in self.matchs)
