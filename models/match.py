import random


class Match:
    def __init__(self, player1, player2):
        self.players_pair = (player1, player2)
        self.player1_color = None
        self.player2_color = None
        self.colors = ["white", "Black"]
        self.player1_score = 0
        self.player2_score = 0
        self.match = ([player1, self.player1_score],
                      [player2, self.player2_score])

    def draw_color(self):
        random.shuffle(self.colors)
        self.player1_color = self.colors[0]
        self.player2_color = self.colors[1]
        return (f'J1 est {self.player1_color}'
                f' J2 est {self.player2_color}')

    def score(self, winner):
        if self.players_pair[0] == winner:
            self.player1_score = 1.0
            self.player2_score = 0.0
        elif self.players_pair[1] == winner:
            self.player1_score = 0.0
            self.player2_score = 1.0
        else:
            self.player1_score = 0.5
            self.player2_score = 0.5

        self.players_pair[0].score += self.player1_score
        self.players_pair[1].score += self.player2_score

        self.match = ([self.players_pair[0], self.player1_score],
                      [self.players_pair[1], self.player2_score])
        return f'Scores du match {self.player1_score} - {self.player2_score}'

    def __str__(self):
        p1, p2 = self.players_pair
        return (f'Match {p1.first_name} vs {p2.first_name} | '
                f'Résultat : {self.player1_score}-{self.player2_score}')
